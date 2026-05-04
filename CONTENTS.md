# Corso Python Base

## Obiettivo del corso

Fornire le basi del linguaggio Python e introdurre, a livello teorico e pratico, il funzionamento delle API REST e la gestione di dati JSON con Python, preparando i partecipanti a interagire con servizi esterni in modo consapevole.

Al termine del corso i partecipanti saranno in grado di:

- Scrivere script Python di base.
- Comprendere e utilizzare le principali strutture dati.
- Leggere e scrivere file.
- Capire cosa sono le API REST.
- Effettuare chiamate API con Python.
- Gestire dati JSON in modo strutturato.

## Prerequisiti

- Conoscenze di informatica di base.

## Contenuti

### 1. Fondamenti di Python

#### 1.1 Introduzione a Python

- Perché usare Python.
- Casi d'uso reali.
- Notebook e ambiente di sviluppo.
- Jupyter, Colab e IDLE.

#### 1.2 Installazione ed esecuzione

- Installare Python.
- Esecuzione di uno script.
- Bytecode e Python Virtual Machine (PVM).
- IDE e ambiente di sviluppo.
- IDLE.
- Distribuzioni: Anaconda e Miniconda.
- Editor: Visual Studio Code.
- Librerie e installazione con `pip`.

#### 1.3 Prime istruzioni

- `print()`.
- `input()`.
- `help()`, `dir()`, `type()`, `callable()`, `repr()`.

#### 1.4 Sintassi e strutture base

- Indentazione e blocchi di codice.
- Variabili.
- Commenti.
- Tipi di dato numerici.
- Operatori.
- Python come calcolatrice.
- Stack, heap, riferimenti e garbage collection.

#### 1.5 Stringhe

- Unicode.
- Metodi principali.
- Costruzione delle stringhe.
- Indicizzazione delle stringhe.
- Formattazione con `format()`.

#### 1.6 Container e funzioni

- Liste, tuple, set e dizionari.
- Mutabilita e immutabilita.
- Funzioni come oggetti.
- Argomenti posizionali, keyword e default.
- Lambda, `enumerate()` e `zip()`.

#### 1.7 Moduli ed eccezioni

- Importazione di moduli.
- Libreria standard e librerie esterne.
- Gestione delle eccezioni con `try` / `except`.

### 2. Strutture dati, logica e file

#### 2.1 Strutture dati fondamentali

- Liste.
- Metodi principali delle liste.
- Tuple.
- Dizionari.
- Metodi dei dizionari.
- Ordinamento delle chiavi nei dizionari.
- Insiemi (`set`).
- Accesso per indice e per etichetta.

#### 2.2 Controllo del flusso

- `if`, `elif`, `else`.
- Cicli `for`.
- Cicli `while`.
- Comprehension.
- Pattern ad accumulo e filtri booleani.

#### 2.3 Gestione dei file

- Lettura di file.
- Scrittura di file.
- Introduzione ai file strutturati.
- File di testo, CSV e formati strutturati.

#### 2.4 Funzioni

- Definizione di funzioni.
- Scope.
- Passaggio dei parametri.
- Parametri opzionali.
- Valori restituiti.

#### 2.5 Moduli ed eccezioni

- Importazione di moduli.
- Gestione delle eccezioni con `try` / `except`.

#### 2.6 NumPy

- ndarray, shape, dtype e broadcasting.
- Creazione di array.
- Tipi numerici controllati.
- Limiti del calcolo in memoria.

#### 2.7 Pandas

- Series e DataFrame.
- Indexing con `loc` e `iloc`.
- Filtering e slicing.
- Grouping, visualizzazione e I/O.
- BigQuery, Dask e Plotly.

### 3. API, JSON e integrazione con Python

#### 3.1 Concetti teorici sulle API

- Cos'è un'API.
- API come interfaccia tra sistemi.
- Perché si usano le API.

#### 3.2 Introduzione alle API REST

- Architettura REST.
- Concetti chiave:
  - Endpoint.
  - Risorsa.
  - Request.
  - Response.

#### 3.3 Metodi HTTP

- `GET`.
- `POST`.
- `PUT`.
- `DELETE`.

#### 3.4 Formato JSON

- Cos'è il formato JSON.
- Struttura del formato JSON.
- Differenze tra JSON e dizionari Python.

#### 3.5 API e JSON con Python

- Introduzione alla libreria `requests`.
- Effettuare una chiamata API con Python.
- Request `GET`.
- Lettura della response.

#### 3.6 Gestione del JSON

- Parsing JSON in dizionari e liste Python.
- Accesso ai dati.

#### 3.7 Gestione errori nelle chiamate API

- Gestione degli errori nelle chiamate API.

#### 3.8 Tipi Python per FastAPI

- Type hints e annotazioni.
- Tipi semplici.
- Tipi generici: liste, tuple, set, dizionari.
- Union, valori opzionali e `None`.
- Classi come tipi, Pydantic e annotazioni con metadati.
- Tipi usati da FastAPI per validazione e documentazione.

#### 3.9 Concorrenza e `async` / `await`

- Codice asincrono.
- Coroutine.
- `async` / `await`.
- Concorrenza e I/O.
- Uso in FastAPI.

#### 3.10 Variabili di ambiente

- Creare e usare le variabili di ambiente.
- Lettura delle variabili di ambiente in Python.
- Tipi e validazione.
- `PATH`.

#### 3.11 Ambienti virtuali

- Creare un progetto.
- Creare un ambiente virtuale.
- Attivare l'ambiente virtuale.
- Verificare che l'ambiente virtuale sia attivo.
- `pip`, `.gitignore`, installazione e avvio del programma.
- Perché servono gli ambienti virtuali.

#### 3.12 Cenni avanzati

- Autenticazione API: concetti base.
- Buone pratiche.
- Limiti e sicurezza.

#### 3.13 Notebook di supporto

- `Importing_data_with_pandas.ipynb`: caricamento dati con Pandas e DataFrame.
- `REST_request_example.ipynb`: esempio di request REST, response e parsing JSON.

#### 3.14 FastAPI

- Installazione di FastAPI.
- First Steps.
- Path Parameters e Query Parameters.
- Request Body e JSON Compatible Encoder.
- Handling Errors e Response Model.
- Dependencies e Security.

## Note organizzative

- Lingua del corso: italiano.
- Livello: base.
- Taglio: teorico e pratico.
- Pubblico previsto: partecipanti con competenze informatiche di base.
