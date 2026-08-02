# License Posture

Pjario Staltman is permissively licensed under the repository's [MIT License](../LICENSE).

## Scope

- The core Pjario workflow, the bundled `Pevie Hischer/` frontend profile, examples, templates, tools, tests, and exported Agent Skill artifacts share the MIT license.
- People may use, copy, modify, publish, distribute, sublicense, and sell copies subject to the license notice and disclaimer.
- The repository does not grant rights to third-party product names, trademarks, or dependencies referenced by the documentation.

## Packaging Decision

Pevie Hischer remains in this repository as a companion profile. It shares core conventions, proof tooling, and the public-ready gate, so keeping it bundled makes the package easier to evaluate and adopt atomically. A split should happen only if the profiles develop independent release cycles or incompatible audiences.

## Decision Record

- Reuse posture: permissive open source.
- License: MIT.
- Bundling: core plus Pevie Hischer in one repository.
- Exported skills: same MIT license as the source repository.
- Security reports: GitHub private vulnerability reporting.
- Reviewed: 2026-08-01.
