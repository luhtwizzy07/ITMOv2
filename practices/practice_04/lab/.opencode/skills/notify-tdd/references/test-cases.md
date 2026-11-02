# Cases for Notify Mini

Use tests/test_baseline.py for isolation: clear service.subscribers in setUp.

- A: empty state; sorted trimmed names; duplicates; a returned list can be changed
  without changing service.subscribers; a later call sees later subscriptions.
- B: existing and absent names; repeated removal; trimmed name; empty/whitespace
  rejection without mutation; removing one name preserves others; listing after
  removal and subscribing again still work.

Call the public function and assert its result and observable state. Avoid
tests tied to a particular implementation (discard versus remove, for example).
For RED, assert that the new function exists before calling it. Missing code
is then a useful failure rather than an import error. An unrelated exception,
a skipped suite, zero tests or a broken baseline must not count as RED.

The helper discovers only the selected feature suite and baseline, captures
unittest results and emits JSON with test counts and assertion messages.
Do not treat an exit code alone as evidence that the intended behaviour failed.
