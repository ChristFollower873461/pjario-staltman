# QA Plan

## Critical User Journeys

- Coordinator creates an implementation prompt from a build request.
- Implementation agent reports proof using the completion-report shape.
- Reviewer gets a packet with the changes under review.

## Automated Checks

- `make validate-examples`
- `make check-proof TICKET=examples/golden-workflow/ticket.md QA=examples/golden-workflow/qa-plan.md PR=examples/golden-workflow/pr-note.md COMPLETION=examples/golden-workflow/completion-report.md`
- `make public-ready`

## Manual Checks

- Inspect `make kickoff-build REQUEST=examples/golden-workflow/build-request.md` output for clear LLM/AI implementation context.
- Confirm proof notes mention privacy scan coverage and rollback path.
- Confirm Oh Shucksenburg technical debt notes describe maintainability impact.

## Failure Cases

- Missing LLM/AI proof should fail proof checking.
- Missing privacy evidence should fail proof checking.
- Missing technical debt/maintainability evidence should fail proof checking.
- Missing rollback evidence should fail proof checking.

## Evidence To Attach

- Terminal output from validation commands.
- GitHub Actions success after push.
- Review packet generation result.

## Not Tested

- Host-app-specific lint, build, deploy, or load tests because this package has no host app stack.
