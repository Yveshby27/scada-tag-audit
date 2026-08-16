# .githooks/

Repo-tracked git hooks. POSIX shell (bash), portable across Linux/macOS/Windows
(git-bash on Windows).

## Activate

Once per clone:

```bash
git config core.hooksPath .githooks
```

Verify:

```bash
git config --get core.hooksPath   # should print: .githooks
```

## Files

- `pre-commit` — cross-artifact consistency gate. Localize the SOURCE/PEER
  slots inside the script for your project's tracked-artifact coupling.

## Bypass

Only when the hook genuinely doesn't apply (typo, rename, comment):

```bash
git commit --no-verify
```

Investigating a hook failure is preferred over bypassing.

## Windows note

`git commit` runs hooks through git-bash regardless of shell (PowerShell,
VSCode, etc.). Bash-by-design is fine.
