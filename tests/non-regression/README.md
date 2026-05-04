# Non-regression Locks

When a module is finalized, create a lock that freezes:
- required key texts
- required image references (`<img src=...>`)
- required links

Regression checks also enforce the baseline module UI and structure on every `site/chapters/chapter-*.html` page:
- the left outline navigation is present
- the page keeps a two-level heading hierarchy (`h2` + `h3`, no deeper levels)
- heading numbering is validated
- the shared JS/CSS still exposes the injected language, theme, print, and top controls

## Create or update a lock

```bash
cd /home/thimoty/git/python-base
python3 scripts/non_regression_guard.py lock site/chapters/chapter-01.html --id M1
python3 scripts/non_regression_guard.py lock site/chapters/chapter-02.html --id M2
python3 scripts/non_regression_guard.py lock site/chapters/chapter-03.html --id M3
```

## Run checks

```bash
cd /home/thimoty/git/python-base
python3 scripts/non_regression_guard.py check
```

Check one module only:

```bash
python3 scripts/non_regression_guard.py check --id M1
```

## Workflow

1. Complete module content.
2. Confirm module is final.
3. Run `lock` for that module.
4. Run `check` after every change or in CI to detect regressions.
