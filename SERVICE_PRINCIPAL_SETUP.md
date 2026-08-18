# Service Principal Setup for Genie Space Deployment

## Problem: 401 Error with Personal Access Token

Genie API may not accept Personal Access Tokens for Space creation in CI/CD context.

## Solution Options

### Option 1: Use OAuth Token (TEMPORARY FIX)

Try creating a new token with all scopes:

1. Databricks → Settings → Developer → Access Tokens
2. **Generate New Token**
3. **Comment:** "Genie Space CI/CD"
4. **Lifetime:** 90 days
5. Copy and update GitHub Secrets

### Option 2: Use Service Principal (PRODUCTION)

Contact your Databricks admin to create a Service Principal.

Required permissions:
- Workspace User access
- USE CATALOG on retail_ai3, retail_ai3_dev
- SELECT on gold schema tables

### Option 3: Manual Deployment (INTERIM)

Deploy Genie Space manually in each workspace until Service Principal is ready.
