---
name: notify-tdd
description: Implement Notify Mini subscriber features with a checked RED/GREEN cycle that distinguishes assertion failures from broken tests and preserves the baseline contract.
---

# Notify TDD

Load this skill for a new subscriber feature in this lab. Read
[references/test-cases.md](references/test-cases.md) before choosing cases.

1. Read docs/requirements.md and add behavioural tests for the requested feature.
   If the new public function does not exist, assert hasattr(service, name)
   before invoking it, so missing functionality is an assertion failure.
2. Run `python3 .opencode/skills/notify-tdd/scripts/phase.py red a` (or `b`).
   The gate accepts RED only when baseline tests pass and feature tests contain
   assertion failures, with no import/runtime errors and no skipped tests.
   Read the reported failing cases; fix broken tests before implementing code.
3. Implement the smallest change consistent with the contract and style guide.
4. Run the same command with `green`. It requires a passing baseline and feature
   suite. Run `sh scripts/check.sh all` to detect interactions with other features.
5. Report actual test counts and results, then inspect the diff. The gate does
   not edit files, accept a commit, or replace review of whether tests are useful.
