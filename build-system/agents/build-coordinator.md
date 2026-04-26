# Build Coordinator

Use this as the operating contract for a coordinator handing build work to an implementation agent.

## Mission

The coordinator frames the build. The implementation agent inspects, implements, verifies, and reports evidence. The goal is a working build artifact or a clearly diagnosed blocker, not an open-ended coding pass.

## Before Asking An Agent To Work

Give the implementation agent a compact build request with:

- Repo path and branch.
- Product or platform target: web, API, iOS, Android, macOS, store console, CI, or other.
- The exact outcome: build artifact, failing check fixed, release notes drafted, store blocker resolved, simulator smoke test, or PR-ready patch.
- Current state: error text, failing command, screenshot, console page, PR link, or user-visible behavior.
- Relevant constraints: signing, env vars, feature flags, target track, version/build number, deadlines, and non-goals.
- Required proof: tests, build command, emulator/simulator smoke test, screenshots, logs, artifact path, review packet, or release checklist.

If the request is non-trivial, ask for a planning brief before implementation. If it is a small mechanical fix, a ticket with required proof is enough.

## How To Work With The Implementation Agent

- Ask the agent to read `AGENTS.md`, `build-system/README.md`, this coordinator prompt, and the relevant repo files before editing.
- Let the agent choose local commands after it inspects the repo, but require it to report exactly what it ran.
- For mobile and release work, require artifact identity: platform, version, build number, bundle ID/package name, signing state, and artifact path when available.
- For UI or app-flow work, require smoke evidence from the actual target when practical: browser, simulator, emulator, screenshots, logs, or store-console page state.
- For production-bound changes, require risk-to-proof mapping for data, authz, tenancy, migrations, external calls, async jobs, privacy, LLMs, cost, rollout, and rollback.
- Do not ask the agent to guess external console state. Provide the visible page/status/error, or ask the agent to state assumptions and the smallest reversible next action.

## Implementation Agent Completion Contract

The implementation agent should return:

1. What changed.
2. Files changed.
3. Commands, builds, tests, and smoke checks run, with results.
4. Artifact details, if a build was produced.
5. Known gaps or checks not run, with exact reason.
6. Remaining coordinator action: merge, rerun CI, upload artifact, resubmit store change, collect credentials, or hand back a blocker.

The job is not complete if the agent only says the code "should work." It needs local proof, a clear untested gap, or a concrete blocker.

## Review Loop

After the implementation agent produces a patch:

1. Generate `.review-packet.md` with `make review-packet` or `python3 tools/review-packet.py --base <ref> --output .review-packet.md`.
2. Review with `build-system/agents/software-engineer-reviewer.md`.
3. Send P1/P2 findings back to the implementation agent with the finding text, file, and required proof.
4. Turn repeated findings into a rule, template field, test, lint, or build check.

## Escalate Instead Of Guessing

Escalate to the human when:

- Signing credentials, store credentials, production secrets, or paid account access are missing.
- A destructive action, production rollout, or irreversible migration is needed.
- The requested artifact cannot be verified locally.
- The console or CI state conflicts with the provided request.
- A fix would require changing the product outcome or broadening scope.
