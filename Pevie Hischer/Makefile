.PHONY: review-packet check-planning-brief check-design-context design-lint design-lint-examples validate-examples test

DESIGN ?= DESIGN.md
DESIGN_MD_VERSION ?= 0.4.0

review-packet:
	python3 "Pevie Hischer/tools/review-packet.py" --output "Pevie Hischer/.review-packet.md"

check-planning-brief:
	@if [ -n "$(PLAN)" ]; then \
		python3 "Pevie Hischer/tools/check-planning-brief.py" --ticket "$(TICKET)" --planning-brief "$(PLAN)"; \
	else \
		python3 "Pevie Hischer/tools/check-planning-brief.py" --ticket "$(TICKET)"; \
	fi

check-design-context:
	python3 "Pevie Hischer/tools/check-design-context.py" --design "$(DESIGN)"

design-lint: check-design-context
	npx -y @google/design.md@$(DESIGN_MD_VERSION) lint "$(DESIGN)"

design-lint-examples:
	$(MAKE) -f "Pevie Hischer/Makefile" design-lint DESIGN="Pevie Hischer/build-system/templates/DESIGN.md"
	$(MAKE) -f "Pevie Hischer/Makefile" design-lint DESIGN="Pevie Hischer/examples/DESIGN.md"
	$(MAKE) -f "Pevie Hischer/Makefile" design-lint DESIGN="Pevie Hischer/examples/golden-workflow/DESIGN.md"

validate-examples:
	python3 "Pevie Hischer/tools/check-design-context.py" --design "Pevie Hischer/build-system/templates/DESIGN.md"
	python3 "Pevie Hischer/tools/check-design-context.py" --design "Pevie Hischer/examples/DESIGN.md"
	python3 "Pevie Hischer/tools/check-design-context.py" --design "Pevie Hischer/examples/golden-workflow/DESIGN.md"
	python3 "Pevie Hischer/tools/check-planning-brief.py" --ticket "Pevie Hischer/examples/trivial-ticket.md"
	python3 "Pevie Hischer/tools/check-planning-brief.py" --ticket "Pevie Hischer/examples/non-trivial-ticket.md" --planning-brief "Pevie Hischer/examples/planning-brief.md"
	python3 "Pevie Hischer/tools/check-planning-brief.py" --ticket "Pevie Hischer/examples/golden-workflow/ticket.md" --planning-brief "Pevie Hischer/examples/golden-workflow/planning-brief.md"

test:
	python3 -m unittest discover -s "Pevie Hischer/tests" -p "test_*.py"
