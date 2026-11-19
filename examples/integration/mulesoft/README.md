# MuleSoft order sync

Scaffold di una applicazione MuleSoft che legge gli ordini da SQLite, applica DataWeave e pubblica i dati su Google Sheets e Microsoft Graph.

## Obiettivo

Mostrare un flusso di integrazione end to end:

1. sorgente dati locale su SQLite;
2. trasformazione con DataWeave;
3. persistenza su Google Sheets;
4. generazione di un documento destinato a SharePoint tramite Microsoft Graph.

## Cartella applicativa

- `order-sync-app/`: progetto MuleSoft

## Apertura in Anypoint Studio

Apri direttamente la cartella:

```text
/home/thimoty/git/python-base/examples/integration/mulesoft/order-sync-app
```

Se Studio chiede il tipo di progetto, usa l'import di un progetto Maven esistente.

## Flussi previsti

- `read-orders-from-sqlite`: query sugli ordini e sulle righe
- `transform-orders-for-google-sheets`: vista tabellare per il foglio
- `transform-orders-for-sharepoint`: documento o payload file per SharePoint
- `push-to-google-sheets`: invio al connettore Google Sheets
- `push-to-sharepoint`: invio al connettore Microsoft Graph o al mock locale

## Note pratiche

Il repository non include credenziali o configurazioni reali dei connettori.
I file qui dentro servono come punto di partenza per un progetto MuleSoft da completare in Anypoint Studio.
