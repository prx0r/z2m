.PHONY: setup doctor test verify build run direct artifact clean install-aether install-sandboxd bootstrap

PYTHON ?= python3
VENV ?= .venv

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -U pip
	$(VENV)/bin/pip install -e '.[mcp,dev]'
	@test -f .env.local || cp .env.example .env.local
	@chmod 600 .env.local 2>/dev/null || true
	@echo "Setup complete. Run: source .venv/bin/activate"

bootstrap: setup install-aether install-sandboxd
	@echo "Bootstrap complete. Read docs/ACTIVATION.md"

doctor:
	$(VENV)/bin/agentbuild doctor

test:
	$(VENV)/bin/pytest -q

verify:
	./scripts/package_verify.sh

build:
	$(VENV)/bin/agentbuild build "$(BLUEPRINT)"

direct:
	$(VENV)/bin/agentbuild build "$(BLUEPRINT)" --mode direct

run:
	$(VENV)/bin/agentbuild build "$(BLUEPRINT)" --mode aether

artifact:
	$(VENV)/bin/agentbuild artifact --output "$(OUT)"

install-aether:
	./scripts/install_aether.sh

install-sandboxd:
	./scripts/install_sandboxd.sh

clean:
	rm -rf .venv .pytest_cache .agentbuild/runs .agentbuild/exports build dist *.egg-info
