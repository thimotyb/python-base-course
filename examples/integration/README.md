# Integration examples

Questa cartella raccoglie esempi di integrazione che usano il materiale del corso come sorgente dati.

## MuleSoft order sync

L'esempio principale è una applicazione MuleSoft che:

1. legge gli ordini da un database SQLite locale;
2. trasforma i dati con DataWeave;
3. scrive una vista tabellare su Google Sheets;
4. costruisce un documento da caricare in SharePoint.

## Stato del repo

Nel progetto Python Base l'esempio M3 attuale espone gli ordini in memoria, non in un database SQLite.
Per questo motivo qui trovi uno schema SQLite seedabile che replica la stessa forma dati dell'esempio M3 e può essere usato come base per l'integrazione MuleSoft.

## Struttura

- `sqlite/`: schema e dati di partenza per il database demo
- `mulesoft/order-sync-app/`: scaffold dell'app MuleSoft
- `mock-microsoft-graph/`: mock locale che risponde come endpoint SharePoint/Graph

## Flusso previsto

1. Query SQLite sugli ordini e sulle righe ordine.
2. Normalizzazione del payload in un modello unico.
3. Trasformazione DataWeave verso:
   - righe tabellari per Google Sheets;
   - contenuto documento per SharePoint.
4. Invio ai connettori Google Sheets e Microsoft Graph.
5. In alternativa, invio al mock locale `mock-microsoft-graph/` per test senza tenant reale.

## Prerequisiti esterni

Questo esempio presuppone:

- Anypoint Studio o un runtime Mule compatibile;
- credenziali Google Sheets;
- credenziali Microsoft Graph / SharePoint, oppure il mock locale incluso nel repo;
- un database SQLite locale creato dallo schema in `sqlite/`.
