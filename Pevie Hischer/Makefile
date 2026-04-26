.PHONY: review-packet check-planning-brief validate-examples test

review-packet:
	python3 "Pevie Hischer/tools/review-packet.py" --output "Pevie Hischer/.review-packet.md"

check-planning-brief:
	@if [ -n "$(PLAN)" ]; then \
		python3 "Pevie Hischer/tools/check-planning-brief.py" --ticket "$(TICKET)" --planning-brief "$(PLAN)"; \
	else \
		python3 "Pevie Hischer/tools/check-planning-brief.py" --ticket "$(TICKET)"; \
	fi

validate-examples:
	python3 "Pevie Hischer/tools/check-planning-brief.py" --ticket "Pevie Hischer/examples/trivial-ticket.md"
	python3 "Pevie Hischer/tools/check-planning-brief.py" --ticket "Pevie Hischer/examples/non-trivial-ticket.md" --planning-brief "Pevie Hischer/examples/planning-brief.md"

test:
	python3 -m unittest discover -s "Pevie Hischer/tests" -p "test_*.py"
