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
  # Enable only for Entra/OIDC auth mode.
  # id-token: write
if: ${{ github.event.pull_request.merged == true }}
strict: true
engine:
  id: copilot
  model: gpt-5.1
  # Optional CLI arguments injected before prompt.
  # args: ["--add-dir", "/workspace", "--verbose"]
  # Optional OIDC auth mode. If enabled, omit COPILOT_PROVIDER_API_KEY.
  # auth:
  #   type: github-oidc
  env:
    COPILOT_PROVIDER_BASE_URL: https://aipoc-foundry-openai.openai.azure.com/openai/v1
    # Required in Copilot BYOK mode; keep aligned with engine.model/deployment.
    COPILOT_MODEL: gpt-5.1
    COPILOT_PROVIDER_API_KEY: ${{ secrets.FOUNDRY_API_KEY }}
    COPILOT_PROVIDER_WIRE_API: responses
    # Optional bearer token alternative (takes precedence over API key).
    # COPILOT_PROVIDER_BEARER_TOKEN: ${{ secrets.FOUNDRY_BEARER_TOKEN }}
    # Optional explicit provider type: openai (default), azure, anthropic.
    # COPILOT_PROVIDER_TYPE: azure
    # Optional wire model/deployment override when it differs from engine.model.
    # COPILOT_PROVIDER_MODEL_ID: gpt-5.1
    # Optional alternative to COPILOT_PROVIDER_MODEL_ID.
    # COPILOT_PROVIDER_WIRE_MODEL: gpt-5.1
    # Optional token limits.
    # COPILOT_PROVIDER_MAX_PROMPT_TOKENS: "128000"
    # COPILOT_PROVIDER_MAX_OUTPUT_TOKENS: "4096"
    # Optional fallback endpoint for Copilot API routing.
    # If both this and engine.api-target are set, engine.api-target wins.
    # GITHUB_COPILOT_BASE_URL: https://your-copilot-router.example.com
network:
  allowed:
    - defaults
    # Keep explicit provider hostname allow-listed for threat-detection and BYOK runs.
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
