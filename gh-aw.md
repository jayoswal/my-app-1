# GH-AW Update Workflow

Use this process after changing `.github/workflows/readme-sync-on-main-merge.md`.

## 1) Edit the source workflow

Update:

- `.github/workflows/readme-sync-on-main-merge.md`

## 2) Recompile lock file

Do not edit the lock file by hand. Regenerate it:

```bash
gh aw compile readme-sync-on-main-merge
# or in this environment:
/tmp/gh-aw compile readme-sync-on-main-merge
```

If you add new restricted secrets in frontmatter (for example `FOUNDRY_API_KEY`), run:

```bash
gh aw compile readme-sync-on-main-merge --approve
# or:
/tmp/gh-aw compile readme-sync-on-main-merge --approve
```

## 3) Review the changes

```bash
git diff .github/workflows/readme-sync-on-main-merge.md .github/workflows/readme-sync-on-main-merge.lock.yml .gitattributes
```

## 4) .gitattributes rule

Usually `.gitattributes` does not need to change each time.  
Keep this line present once:

```text
.github/workflows/*.lock.yml linguist-generated=true merge=ours
```

## Nuance

- If you only changed markdown body instructions, recompiling is usually not required.
- If you changed frontmatter (`on`, `permissions`, `engine`, `network`, `tools`, `safe-outputs`, etc.), recompiling is required.

## What Can Be Added to readme-sync-on-main-merge.md

This section is specifically for `.github/workflows/readme-sync-on-main-merge.md`.

### Already present in that file

- `engine.id: copilot`
- `engine.model: gpt-5.3-codex`
- `engine.env.COPILOT_PROVIDER_BASE_URL`
- `engine.env.COPILOT_MODEL`
- `engine.env.COPILOT_PROVIDER_API_KEY`
- `engine.env.COPILOT_PROVIDER_WIRE_API: responses`
- `network.allowed` with `defaults` and Azure hostname

### Addable BYOK fields (optional)

Add only when needed:

- `engine.env.COPILOT_PROVIDER_BEARER_TOKEN`
- `engine.env.COPILOT_PROVIDER_TYPE` (`openai`, `azure`, `anthropic`)
- `engine.env.COPILOT_PROVIDER_MODEL_ID`
- `engine.env.COPILOT_PROVIDER_WIRE_MODEL`
- `engine.env.COPILOT_PROVIDER_MAX_PROMPT_TOKENS`
- `engine.env.COPILOT_PROVIDER_MAX_OUTPUT_TOKENS`
- `engine.args` (CLI args injected before prompt)
- `engine.auth` with OIDC (if switching from key auth)
- `permissions.id-token: write` (required when `engine.auth.type: github-oidc`)

For custom endpoint fallback:
- `engine.env.GITHUB_COPILOT_BASE_URL` can be added, but if `engine.api-target` is also set, `engine.api-target` wins.

### Copy-paste variants for readme-sync-on-main-merge.md

Current API-key variant:

```yaml
engine:
  id: copilot
  model: gpt-5.3-codex
  env:
    COPILOT_PROVIDER_BASE_URL: https://aipoc-foundry-openai.openai.azure.com/openai/v1
    COPILOT_MODEL: gpt-5.3-codex
    COPILOT_PROVIDER_API_KEY: ${{ secrets.FOUNDRY_API_KEY }}
    COPILOT_PROVIDER_WIRE_API: responses

network:
  allowed:
    - defaults
    - aipoc-foundry-openai.openai.azure.com
```

API key + advanced optional knobs:

```yaml
engine:
  id: copilot
  model: gpt-5.3-codex
  env:
    COPILOT_PROVIDER_BASE_URL: https://aipoc-foundry-openai.openai.azure.com/openai/v1
    COPILOT_MODEL: gpt-5.3-codex
    COPILOT_PROVIDER_API_KEY: ${{ secrets.FOUNDRY_API_KEY }}
    COPILOT_PROVIDER_WIRE_API: responses
    # COPILOT_PROVIDER_TYPE: azure
    # COPILOT_PROVIDER_MODEL_ID: gpt-5.3-codex
    # COPILOT_PROVIDER_WIRE_MODEL: gpt-5.3-codex
    # COPILOT_PROVIDER_MAX_PROMPT_TOKENS: "128000"
    # COPILOT_PROVIDER_MAX_OUTPUT_TOKENS: "4096"
    # GITHUB_COPILOT_BASE_URL: https://your-copilot-router.example.com
  # args: ["--add-dir", "/workspace", "--verbose"]

network:
  allowed:
    - defaults
    - aipoc-foundry-openai.openai.azure.com
```

Bearer-token variant (instead of API key):

```yaml
engine:
  id: copilot
  model: gpt-5.3-codex
  env:
    COPILOT_PROVIDER_BASE_URL: https://aipoc-foundry-openai.openai.azure.com/openai/v1
    COPILOT_MODEL: gpt-5.3-codex
    COPILOT_PROVIDER_BEARER_TOKEN: ${{ secrets.FOUNDRY_BEARER_TOKEN }}
    COPILOT_PROVIDER_WIRE_API: responses
```

OIDC/Entra variant (instead of API key):

```yaml
permissions:
  contents: read
  pull-requests: read
  id-token: write

engine:
  id: copilot
  model: gpt-5.3-codex
  auth:
    type: github-oidc
  env:
    COPILOT_PROVIDER_BASE_URL: https://aipoc-foundry-openai.openai.azure.com/openai/v1
    COPILOT_MODEL: gpt-5.3-codex
    COPILOT_PROVIDER_WIRE_API: responses
```

Codex engine variant for Azure/custom endpoint:

```yaml
engine:
  id: codex
  model: gpt-4o
  env:
    OPENAI_BASE_URL: https://my-azure-endpoint.openai.azure.com/openai/deployments/gpt-4o
    OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_API_KEY }}

network:
  allowed:
    - github.com
    - my-azure-endpoint.openai.azure.com
```

### Important rules

- Do not edit `.lock.yml` manually; always compile after frontmatter changes.
- For Copilot BYOK mode, set `COPILOT_PROVIDER_BASE_URL` and `COPILOT_MODEL`.
- Use either `COPILOT_PROVIDER_API_KEY` or `COPILOT_PROVIDER_BEARER_TOKEN` unless intentionally preferring bearer token.
- For Codex custom endpoint mode, use `OPENAI_BASE_URL` and `OPENAI_API_KEY` instead of `COPILOT_PROVIDER_*`.
- Keep the Azure hostname in `network.allowed`.
- With `/openai/v1` style, no `api-version` field is needed in this workflow config.

### Error mapping and quick checks

If you see:
- `400 status code (no body)`
- `managed identity endpoint returned 403 Forbidden`
- blocked domain `169.254.169.254`

Check:
1. `FOUNDRY_API_KEY` exists in GitHub Actions secrets and is non-empty.
2. The run context has access to secrets (forked PR restrictions can block secrets).
3. `COPILOT_PROVIDER_BASE_URL` points to `/openai/v1` on the correct Azure resource.
4. `network.allowed` includes the provider hostname.
5. `engine.model` matches the intended Azure deployment/model identifier.
