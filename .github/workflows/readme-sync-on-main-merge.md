---
emoji: 📘
name: README Sync On Main Merge
description: Update README.md when a PR is merged into main and open a follow-up PR with README changes when needed.
on:
  pull_request:
    types: [closed]
    branches: [main]
    forks: ["*"]
permissions:
  contents: read
  pull-requests: read
if: ${{ github.event.pull_request.merged == true }}
strict: true
engine:
  id: copilot
  model: self-learning-gpt-5.1-chat
  env:
    COPILOT_PROVIDER_BASE_URL: https://aipoc-foundry-openai.openai.azure.com/openai/v1
    COPILOT_PROVIDER_API_KEY: ${{ secrets.FOUNDRY_API_KEY }}
    COPILOT_PROVIDER_TYPE: azure
    COPILOT_PROVIDER_MODEL_ID: self-learning-gpt-5.1-chat
    COPILOT_PROVIDER_WIRE_API: responses
network:
  allowed:
    - defaults
    - aipoc-foundry-openai.openai.azure.com
tools:
  github:
    mode: gh-proxy
    toolsets: [context, repos, pull_requests]
safe-outputs:
  create-pull-request:
    title-prefix: "[docs] "
    branch-prefix: "docs/readme-sync/"
    base-branch: "main"
    draft: false
    if-no-changes: "ignore"
    allowed-base-branches: [main]
    allowed-files:
      - "README.md"
---

# README Sync On Main Merge

## Task

You are triggered only when a pull request targeting `main` is closed. Continue only if the pull request was merged.

Analyze the current repository code and make `README.md` accurate and up to date. Focus on these sections:

- Pre-Requisite
- Endpoints
- Steps to Run the app

Use code as source of truth and regenerate those sections when needed. Keep wording concise and practical.

## Rules

- Modify only `README.md`.
- Keep existing useful README content outside these sections whenever possible.
- If `README.md` is already accurate, call `noop` with a short reason.
- If updates are needed, produce one `create_pull_request` safe output targeting `main`.
- Use a clear PR title and explain what changed in the PR body.

## Safe Outputs

- `create_pull_request`
- `noop`
