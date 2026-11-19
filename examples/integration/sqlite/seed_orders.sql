PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_lines;
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer TEXT NOT NULL,
  order_date TEXT NOT NULL,
  status TEXT NOT NULL
);

CREATE TABLE order_lines (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  sku TEXT NOT NULL,
  description TEXT NOT NULL,
  quantity INTEGER NOT NULL,
  unit_price REAL NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id)
);

INSERT INTO orders (id, customer, order_date, status) VALUES
  (1001, 'Acme SRL', '2026-05-10', 'confirmed'),
  (1002, 'Beta Spa', '2026-05-12', 'draft');

INSERT INTO order_lines (id, order_id, sku, description, quantity, unit_price) VALUES
  (1, 1001, 'PEN-001', 'Blue pen', 10, 1.2),
  (2, 1001, 'NBK-010', 'Notebook A4', 5, 3.5),
  (3, 1002, 'USB-128', 'USB drive 128GB', 2, 12.0);
