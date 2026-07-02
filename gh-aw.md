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
