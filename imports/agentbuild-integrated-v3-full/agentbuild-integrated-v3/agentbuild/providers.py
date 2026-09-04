from __future__ import annotations

from dataclasses import dataclass

from .config import PROVIDER_ENV
from .sandboxd import opencode_auth_bundle


@dataclass(frozen=True)
class ProviderPlan:
    provider: str
    aether_env: str
    builder_agent: str
    one_key_builder_mode: str
    notes: str


def provider_plan(provider: str) -> ProviderPlan:
    env = PROVIDER_ENV.get(provider, f"{provider.upper()}_API_KEY")
    if provider == "anthropic":
        return ProviderPlan(provider, env, "claude-code", "api-key", "The same Anthropic API key can be connected to sandboxd's Claude Code lane.")
    if provider in {"openrouter", "openai", "deepseek", "gemini", "fireworks", "moonshot", "zai"}:
        return ProviderPlan(
            provider, env, "opencode", "opencode-import",
            "Aether uses the provider directly. For the sandboxd OpenCode lane, import an OpenCode auth bundle; provider support depends on the installed OpenCode version. If not connected, sandboxd can still use OpenCode's keyless free tier.",
        )
    return ProviderPlan(provider, env, "opencode", "none", "Use Aether directly and configure the sandboxd builder separately.")


def builder_credentials(provider: str, api_key: str) -> tuple[str, str]:
    plan = provider_plan(provider)
    if plan.one_key_builder_mode == "api-key":
        return plan.builder_agent, api_key
    if plan.one_key_builder_mode == "opencode-import":
        return plan.builder_agent, opencode_auth_bundle(provider, api_key)
    raise ValueError(f"No one-key builder mapping for provider {provider}")
