.PHONY: review-packet test check-planning-brief validate-examples doctor kickoff export-skill public-ready pevie-test pevie-review-packet pevie-validate-examples pevie-design-lint test-all

PROFILE ?= both
MODE ?= package
OUT ?= .dist/pjario-staltman-skill

review-packet:
	python3 tools/review-packet.py --include-untracked --output .review-packet.md

test:
	python3 -m unittest discover -s tests -p "test_*.py"

pevie-test:
	python3 -m unittest discover -s "Pevie Hischer/tests" -p "test_*.py"

pevie-review-packet:
	$(MAKE) -f "Pevie Hischer/Makefile" review-packet

validate-examples:
	python3 tools/check-planning-brief.py --ticket examples/trivial-ticket.md
	python3 tools/check-planning-brief.py --ticket examples/non-trivial-ticket.md --planning-brief examples/planning-brief.md

pevie-validate-examples:
	$(MAKE) -f "Pevie Hischer/Makefile" validate-examples

pevie-design-lint:
	$(MAKE) -f "Pevie Hischer/Makefile" design-lint-examples

doctor:
	python3 tools/doctor.py --mode "$(MODE)" --profile "$(PROFILE)" --public-ready

kickoff:
	@if [ -z "$(TICKET)" ]; then \
		echo "TICKET is required"; \
		exit 2; \
	fi
	python3 tools/kickoff.py --profile "$(if $(filter both,$(PROFILE)),core,$(PROFILE))" --ticket "$(TICKET)" $(if $(PLAN),--planning-brief "$(PLAN)") $(if $(DESIGN),--design "$(DESIGN)")

export-skill:
	python3 tools/export-skill.py --output "$(OUT)" --force

test-all: test pevie-test validate-examples pevie-validate-examples

public-ready: test-all pevie-design-lint doctor
	git diff --check
	tmpdir="$$(mktemp -d)"; $(MAKE) export-skill OUT="$$tmpdir/pjario-staltman"
	$(MAKE) review-packet
	$(MAKE) pevie-review-packet
	rm -f .review-packet.md "Pevie Hischer/.review-packet.md"

check-planning-brief:
	@if [ -n "$(PLAN)" ]; then \
		python3 tools/check-planning-brief.py --ticket "$(TICKET)" --planning-brief "$(PLAN)"; \
	else \
		python3 tools/check-planning-brief.py --ticket "$(TICKET)"; \
	fi
