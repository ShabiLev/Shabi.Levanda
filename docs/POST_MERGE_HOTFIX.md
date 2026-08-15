# Post-merge CI hotfix

The `main` push quality gate exposed a timing-sensitive Playwright assertion after the mobile menu was resized to desktop width. The production code already resets the menu via `matchMedia`; the test now waits for that asynchronous browser event before asserting the final state.

Release remains blocked until this hotfix passes CI and is merged.
