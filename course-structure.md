# Course Structure

- Course name: Corso Python Base
- Audience: Partecipanti con conoscenze informatiche di base
- Language: Italiano primary; English via on-page Google Translate switch
- Output format: Static interactive course website
- Theme: Python Base

## Modules

| Module | Title | Output Artifact | Source Files | Notes |
| --- | --- | --- | --- | --- |
| M1 | Fondamenti di Python | `site/chapters/chapter-01.html` | `CONTENTS.md`, `resources/appunti_erogazioni.docx` | Introduzione, ambiente, oggetti, container, stringhe, funzioni, moduli ed eccezioni |
| M2 | Strutture dati, logica e file | `site/chapters/chapter-02.html` | `CONTENTS.md`, `resources/appunti_erogazioni.docx` | NumPy, Pandas, indexing, filtering, grouping, I/O, BigQuery e visualizzazione |
| M3 | API, JSON e integrazione con Python | `site/chapters/chapter-03.html` | `CONTENTS.md` | API REST, metodi HTTP, JSON, requests, parsing, errori, autenticazione, sicurezza, FastAPI e notebook di supporto |

## Source Inventory

| Source File | Type | Used In Modules | Notes |
| --- | --- | --- | --- |
| `CONTENTS.md` | course outline | `M1, M2, M3` | Canonical outline for the course |
| `resources/appunti_erogazioni.docx` | source notes | `M1, M2` | Appunti delle due erogazioni, con figure e link da integrare |
| `../agents-course/site/` | reference website | site layout and shared behavior | Structural and visual reference only |

## Mapping Rules

- Keep one module page per module under `site/chapters/`.
- Keep module code stable (`M1` to `M3`) for the first course version.
- Update this file whenever modules are split, merged, renamed, or expanded.
- Keep `CONTENTS.md` aligned with the website navigation.
