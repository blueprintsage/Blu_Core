# Blu Core Setup

status: active
owner: repository-governance
last_reviewed: 2026-08-05

## From the Git bundle

```bash
git clone Blu_Core_v0.1.0-bootstrap_2026-08-05.bundle Blu_Core
cd Blu_Core
git log --oneline --decorate --graph --all
```

Add the remote you create:

```bash
git remote add origin <REMOTE_URL>
git push -u origin main
```

## From the source ZIP

Extract the ZIP, then:

```bash
cd Blu_Core
git init -b main
git add .
git commit -m "chore(repo): import Blu Core bootstrap"
git remote add origin <REMOTE_URL>
git push -u origin main
```

The Git bundle is preferred because it preserves the prepared bootstrap commit
history.

## Verification

```bash
git status --short
git diff --check
sha256sum -c kernel/golden/v0.22.0/SHA256SUMS
```
