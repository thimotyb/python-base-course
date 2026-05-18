# Python Base

Repository con materiali del corso Python Base, sito statico e notebook di supporto.

## Avviare il sito in locale

Da root del repository:

```bash
python3 -m http.server 8000 --directory site
```

Poi apri nel browser:

```text
http://localhost:8000
```

In alternativa puoi servire direttamente la cartella `site`:

```bash
cd site
python3 -m http.server 8000
```

## Avviare i notebook in locale con Jupyter

Se non usi Colab, puoi aprire i notebook localmente con Jupyter:

```bash
jupyter notebook
```

oppure:

```bash
jupyter lab
```

Avvia il comando dalla root del repository e poi apri dal browser il file `.ipynb` che ti interessa.

Notebook presenti nel repository:

- `REST_request_example.ipynb`
- `examples/m3-keycloak-client-credentials/notebook/M3-Keycloak-JWT-Demo.ipynb`

## Notebook linkato in M1

Nel capitolo M1 c’è un link a un notebook su Colab. Se non vuoi usare Colab:

1. apri il link del notebook nel browser;
2. scarica il file `.ipynb` in locale oppure copia il contenuto in un nuovo notebook;
3. avvia Jupyter nella cartella del repository;
4. apri il notebook scaricato da Jupyter.

Questo approccio vale anche per altri notebook esterni che vuoi eseguire in locale invece che su Colab.
