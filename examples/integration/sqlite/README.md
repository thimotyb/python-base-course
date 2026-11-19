# SQLite demo database

Questa cartella contiene lo schema SQL per un database demo degli ordini.

L'esempio usa la stessa struttura logica del servizio ordini M3:

- ordine
- righe ordine

## Creazione del database locale

Se hai `sqlite3` installato, puoi creare il database così:

```bash
sqlite3 orders.db < seed_orders.sql
```

Poi la Mule app può puntare a `orders.db` per leggere gli ordini.

## Tabelle

- `orders`: testata ordine
- `order_lines`: righe ordine
