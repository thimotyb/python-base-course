# Integration examples

Questa è la copia pubblicabile dell'esempio `examples/integration/`.
La sorgente di verità resta nella cartella `examples/`.

## MuleSoft order sync

L'esempio principale è una applicazione MuleSoft che:

1. legge gli ordini da un database SQLite locale;
2. trasforma i dati con DataWeave;
3. scrive una vista tabellare su Google Sheets;
4. costruisce un documento da caricare in SharePoint.

## Struttura

- `sqlite/`: schema e dati di partenza per il database demo
- `mulesoft/order-sync-app/`: scaffold dell'app MuleSoft
- `mock-microsoft-graph/`: mock locale che risponde come endpoint SharePoint/Graph

## Prerequisiti esterni

Questo esempio presuppone:

- Anypoint Studio o un runtime Mule compatibile;
- credenziali Google Sheets;
- credenziali Microsoft Graph / SharePoint;
- credenziali Microsoft Graph / SharePoint, oppure il mock locale incluso nel repo;
- un database SQLite locale creato dallo schema in `examples/integration/sqlite/`.
