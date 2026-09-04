from __future__ import annotations

import argparse
import asyncio
import getpass
import json
import os
from pathlib import Path
import shutil
import sys

from . import __version__
from .config import PROVIDER_ENV, Settings, load_env_file, write_local_env
from .providers import provider_plan
from .runner import BuildRunner
from .sandboxd import SandboxdClient, opencode_auth_bundle
from .security import scan_repo


def root_from_args(args) -> Path:
    return Path(getattr(args, "root", None) or Path.cwd()).resolve()


def _print_json(obj) -> None:
    print(json.dumps(obj, indent=2, sort_keys=True, default=str))


def _secret_from_args(value: str | None, env_name: str | None, prompt: str, required: bool = True) -> str:
    if value:
        return value
    if env_name:
        found = os.getenv(env_name, "")
        if found:
            return found
        if required:
            raise SystemExit(f"Environment variable {env_name} is not set")
        return ""
    if not sys.stdin.isatty():
        if required:
            raise SystemExit(f"{prompt} must be supplied via --api-key-env/--api-key in non-interactive mode")
        return ""
    value = getpass.getpass(prompt)
    if required and not value:
        raise SystemExit("A non-empty secret is required")
    return value


def cmd_configure(args) -> int:
    root = root_from_args(args)
    root.mkdir(parents=True, exist_ok=True)
    env_name = PROVIDER_ENV.get(args.provider, f"{args.provider.upper()}_API_KEY")
    api_key = _secret_from_args(args.api_key, args.api_key_env, f"{args.provider} API key: ")

    plan = provider_plan(args.provider)
    effective_builder = args.builder_agent or plan.builder_agent
    updates = {
        "AGENTBUILD_PROVIDER": args.provider,
        "AGENTBUILD_ORCHESTRATOR_MODEL": args.model,
        "SANDBOXD_DEFAULT_AGENT": effective_builder,
        env_name: api_key,
    }
    if args.builder_model is not None:
        updates["SANDBOXD_BUILDER_MODEL"] = args.builder_model
    if args.sandboxd_url:
        updates["SANDBOXD_URL"] = args.sandboxd_url

    # Only ask for/store the sandboxd bearer when the caller supplied one or when
    # credential synchronization needs authenticated control-plane access.
    sandboxd_token = args.sandboxd_token or (os.getenv(args.sandboxd_token_env, "") if args.sandboxd_token_env else "")
    if args.sync_builder and not sandboxd_token and not os.getenv("SANDBOXD_API_TOKEN") and sys.stdin.isatty():
        sandboxd_token = getpass.getpass("sandboxd API token (leave blank only if sandboxd auth is disabled): ")
    if sandboxd_token:
        updates["SANDBOXD_API_TOKEN"] = sandboxd_token

    path = write_local_env(root, updates)
    print(f"Wrote local secrets/config to {path} (mode 0600 where supported).")
    print(f"Aether provider credential: {env_name}")
    print(f"Recommended builder: {plan.builder_agent}; selected builder: {effective_builder}; one-key mode: {plan.one_key_builder_mode}")

    if args.sync_builder:
        # Make newly-written values visible to Settings.load in this process.
        for k, v in updates.items():
            os.environ[k] = v
        settings = Settings.load(root)
        client = SandboxdClient(settings.sandboxd_url, settings.sandboxd_token)

        async def sync():
            if effective_builder == "opencode":
                # OpenCode supports many underlying providers through auth.json. Import
                # the provider credential bundle rather than misusing its own API-key slot.
                return await client.import_agent_credentials("opencode", opencode_auth_bundle(args.provider, api_key))
            if effective_builder == "claude-code" and args.provider == "anthropic":
                return await client.connect_agent_api_key("claude-code", api_key)
            raise RuntimeError(
                f"Cannot safely map provider {args.provider!r} to builder {effective_builder!r} with one key; "
                "configure the builder separately with `agentbuild builder-auth`."
            )

        try:
            asyncio.run(sync())
            print("Builder credential connected control-plane-side; it is not copied into build sandboxes.")
        except Exception as exc:
            print(f"Builder credential sync failed: {exc}", file=sys.stderr)
            print("Your provider is still configured for Aether. See docs/PROVIDERS.md for builder alternatives.", file=sys.stderr)
            return 2
    return 0


def cmd_doctor(args) -> int:
    settings = Settings.load(root_from_args(args))
    checks: list[tuple[str, bool, str]] = []
    checks.append(("python>=3.11", sys.version_info >= (3, 11), sys.version.split()[0]))
    checks.append(("git", shutil.which("git") is not None, shutil.which("git") or "missing"))
    checks.append(("docker", shutil.which("docker") is not None, shutil.which("docker") or "missing"))
    aether = shutil.which("aether")
    checks.append(("aether", aether is not None, aether or "missing (only required for --mode aether)"))
    key_ok = bool(settings.provider_key)
    checks.append((settings.provider_env, key_ok, "set" if key_ok else "missing (only required for Aether mode)"))
    secret_hits = scan_repo(settings.root)
    checks.append(("secret-scan", not secret_hits, "clean" if not secret_hits else f"potential secrets in {secret_hits}"))
    try:
        healthy = asyncio.run(SandboxdClient(settings.sandboxd_url, settings.sandboxd_token).health())
    except Exception:
        healthy = False
    checks.append(("sandboxd", healthy, settings.sandboxd_url))

    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name:28} {detail}")
    blocking = [name for name, ok, _ in checks if not ok and name in {"python>=3.11", "sandboxd", "secret-scan"}]
    if settings.mode == "aether" and not aether:
        blocking.append("aether")
    if settings.mode == "aether" and not key_ok:
        blocking.append(settings.provider_env)
    return 1 if blocking else 0


def cmd_builder_auth(args) -> int:
    settings = Settings.load(root_from_args(args))
    client = SandboxdClient(settings.sandboxd_url, settings.sandboxd_token)

    async def do():
        if args.import_file:
            return await client.import_agent_credentials(args.agent, Path(args.import_file).read_text())
        key = _secret_from_args(args.api_key, args.api_key_env, f"{args.agent} API key: ")
        return await client.connect_agent_api_key(args.agent, key)

    _print_json(asyncio.run(do()))
    return 0


def cmd_build(args) -> int:
    settings = Settings.load(root_from_args(args))
    if args.mode:
        settings.mode = args.mode
    if args.builder_agent:
        settings.builder_agent = args.builder_agent
    if args.builder_model is not None:
        settings.builder_model = args.builder_model
    runner = BuildRunner(settings)
    if settings.mode == "direct":
        receipt = asyncio.run(runner.run_direct(args.blueprint))
    elif settings.mode == "aether":
        receipt = runner.run_aether(args.blueprint)
    else:
        raise SystemExit(f"Unknown mode: {settings.mode}")
    _print_json({k: getattr(receipt, k) for k in receipt.__slots__})
    return 0 if receipt.release_passed else 3


def cmd_runs(args) -> int:
    root = root_from_args(args)
    base = root / ".agentbuild" / "runs"
    if not base.exists():
        print("No runs yet.")
        return 0
    for p in sorted(base.glob("*/release-receipt.json"), reverse=True):
        try:
            data = json.loads(p.read_text())
            print(
                f"{data.get('run_id')}  mode={data.get('mode')}  pass={data.get('release_passed')}  "
                f"preview={data.get('preview_url','')}  artifact={data.get('artifact_path','')}"
            )
        except Exception:
            print(p)
    return 0



def cmd_artifact(args) -> int:
    root = root_from_args(args)
    base = root / ".agentbuild" / "runs"
    if args.run_id:
        receipt_path = base / args.run_id / "release-receipt.json"
    else:
        receipts = sorted(base.glob("*/release-receipt.json"), key=lambda p: p.stat().st_mtime, reverse=True) if base.exists() else []
        if not receipts:
            print("No build receipts found.", file=sys.stderr)
            return 2
        receipt_path = receipts[0]
    if not receipt_path.exists():
        print(f"Run receipt not found: {receipt_path}", file=sys.stderr)
        return 2
    data = json.loads(receipt_path.read_text())
    artifact = data.get("artifact_path") or str(receipt_path.parent / "workspace.zip")
    src = Path(artifact)
    if not src.is_absolute():
        src = (root / src).resolve()
    if not src.exists():
        print(f"Workspace artifact not found: {src}", file=sys.stderr)
        return 2
    out = Path(args.output or f"{data.get('run_id','agentbuild')}-workspace.zip").resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, out)
    print(out)
    return 0


def cmd_plan(args) -> int:
    p = provider_plan(args.provider)
    _print_json({
        "provider": p.provider,
        "aether_env": p.aether_env,
        "builder_agent": p.builder_agent,
        "one_key_builder_mode": p.one_key_builder_mode,
        "notes": p.notes,
    })
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agentbuild", description="Aether + sandboxd autonomous application factory")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("configure", help="Store provider/control-plane configuration without committing secrets")
    c.add_argument("--root", default=".")
    c.add_argument("--provider", required=True)
    c.add_argument("--model", required=True, help="Aether model id, e.g. openrouter:xiaomi/mimo-v2.5")
    c.add_argument("--api-key", default=None, help="Provider key (interactive prompt is safer; this can enter shell history)")
    c.add_argument("--api-key-env", default=None, help="Read provider key from an existing environment variable")
    c.add_argument("--builder-agent", choices=["opencode", "claude-code"], default="")
    c.add_argument("--builder-model", default=None, help="OpenCode uses provider/model; Claude Code uses its supported model alias/id")
    c.add_argument("--sandboxd-url", default="")
    c.add_argument("--sandboxd-token", default="", help="sandboxd bearer (interactive/env is safer)")
    c.add_argument("--sandboxd-token-env", default=None)
    c.add_argument("--sync-builder", action="store_true", help="Also connect/import the provider credential into sandboxd where supported")
    c.set_defaults(func=cmd_configure)

    d = sub.add_parser("doctor", help="Verify local control-plane prerequisites")
    d.add_argument("--root", default=".")
    d.set_defaults(func=cmd_doctor)

    b = sub.add_parser("build", help="Build from a blueprint file or inline prompt")
    b.add_argument("blueprint")
    b.add_argument("--root", default=".")
    b.add_argument("--mode", choices=["aether", "direct"])
    b.add_argument("--builder-agent", choices=["opencode", "claude-code"], default="")
    b.add_argument("--builder-model", default=None)
    b.set_defaults(func=cmd_build)

    ba = sub.add_parser("builder-auth", help="Connect a coding-agent credential to sandboxd")
    ba.add_argument("--root", default=".")
    ba.add_argument("--agent", choices=["opencode", "claude-code"], required=True)
    g = ba.add_mutually_exclusive_group(required=False)
    g.add_argument("--api-key")
    g.add_argument("--api-key-env")
    g.add_argument("--import-file")
    ba.set_defaults(func=cmd_builder_auth)

    r = sub.add_parser("runs", help="List build receipts")
    r.add_argument("--root", default=".")
    r.set_defaults(func=cmd_runs)


    ar = sub.add_parser("artifact", help="Copy a run's exported project ZIP to a convenient path")
    ar.add_argument("run_id", nargs="?", default="", help="Run id; defaults to latest run")
    ar.add_argument("--root", default=".")
    ar.add_argument("--output", default="")
    ar.set_defaults(func=cmd_artifact)

    pp = sub.add_parser("provider-plan", help="Show the one-key wiring plan for a provider")
    pp.add_argument("provider")
    pp.set_defaults(func=cmd_plan)
    return p


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
