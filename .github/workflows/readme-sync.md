---
emoji: 📖
description: Keeps README.md in sync with the API after every PR merge to main from feat/*, fix/*, hotfix/*, or bugfix/* branches.
on:
  pull_request:
    types: [closed]
    branches: [main]
if: github.event.pull_request.merged == true
engine: copilot/gpt-5.4-mini
permissions:
  contents: read
  pull-requests: read
  issues: read
tools:
  github:
    mode: gh-proxy
    toolsets: [default]
safe-outputs:
  create-pull-request:
    branch-prefix: "gh-aw/README-sync-"
    preserve-branch-name: true
    base-branch: "main"
    allowed-files:
      - "README.md"
    draft: false
    auto-close-issue: false
---

# README Sync

## Task

Pull request #${{ github.event.pull_request.number }} targeting `main` was just merged.

### Step 1 — Check the source branch (whitelist gate)

Run the following command to get the head branch name:

```bash
gh pr view ${{ github.event.pull_request.number }} --json headRefName --jq '.headRefName'
```

The workflow must only proceed for PRs from these branch patterns: `feat/*`, `fix/*`, `hotfix/*`, `bugfix/*`.

- If the head branch **does NOT** start with one of those prefixes, call `noop` immediately with explanation: "Source branch does not match the whitelisted patterns (feat/*, fix/*, hotfix/*, bugfix/*). Skipping README sync."
- If it **does** match, continue to the next steps.

### Step 2 — Read the source

Examine `main.py` in full to identify:
- All HTTP route handlers (`@app.get`, `@app.post`, `@app.put`, `@app.patch`, `@app.delete`) with their exact URL paths, HTTP methods, and response types.
- The FastAPI app version string (from `FastAPI(version=...)` or any version constant).

### Step 3 — Read the current README

Read `README.md` to understand what is already documented.

### Step 4 — Determine if an update is needed

The README must contain exactly these sections in this order:

```
### Python Version
<version string>

### Run Command
`<the command to start the server>`

### API Endpoints
#### <HTTP METHOD> <path>
<brief description>

**Example Request**
\`\`\`bash
curl -X <METHOD> http://localhost:8000<path>
\`\`\`

**Example Response**
\`\`\`json
{ ... }
\`\`\`
```

One `####` sub-section per endpoint, heading in the form `#### GET /health`. Example requests must be realistic `curl` commands. Example responses must match the actual return type from `main.py`.

### Step 5 — Act

- If the README is **already accurate and complete**, call `noop` with a brief explanation.
- Otherwise, write the updated `README.md` and open a pull request with branch name `readme-sync-pr-${{ github.event.pull_request.number }}` and title `docs: sync README with API (PR #${{ github.event.pull_request.number }})`.

## Safe Outputs

- Use `create-pull-request` to open the README update PR targeting `main`.
- Use `noop` with a brief explanation when skipping (branch not whitelisted) or when no changes are needed.
