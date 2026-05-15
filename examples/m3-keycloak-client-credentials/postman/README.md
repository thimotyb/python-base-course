# Postman playbook

This folder contains a collection that reproduces the full flow step by step.

## Setup

1. Start the example with `docker compose up --build`.
2. Import the environment file.
3. Import the collection file.
4. Select the `M3 Keycloak JWT demo` environment.

## Step by step

1. Run `01 - Get access token`.
2. Check that the response contains `access_token`.
3. Run `02 - Call protected endpoint`.
4. Confirm the API returns `Access granted`.

## What the collection does

- It requests a token from Keycloak with `client_credentials`.
- It stores the token in a collection variable.
- It reuses the token in the protected API call.

