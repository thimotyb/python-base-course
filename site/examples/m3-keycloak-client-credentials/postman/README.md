# Postman playbook

This folder contains a collection that reproduces the full flow step by step against the M3 Orders API.

## Setup

1. Start the example with `docker compose up --build`.
2. Import the environment file.
3. Import the collection file.
4. Select the `M3 Keycloak JWT demo` environment.

## Step by step

1. Run `01 - Get access token`.
2. Check that the response contains `access_token`.
3. Run `02 - List orders`.
4. Check that the response contains at least one order and that `order_id` is stored.
5. Run `03 - Get order detail`.
6. Run `04 - Create order`.
7. Check that the new order id is stored in `created_order_id`.
8. Run `05 - Get created order lines`.

## What the collection does

- It requests a token from Keycloak with `client_credentials`.
- It stores the token in a collection variable.
- It lists the existing orders.
- It reads one order detail.
- It creates a new order with header and lines.
- It reads back the lines of the created order.
