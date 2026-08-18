# Genie Space Deployment Guide

## 🎯 Current Status

### DEV Workspace ✅
- **Space Created:** Retail Analytics Starter Space
- **Space ID:** `01f19a1eb2471ac1a7e433dcc10355f8`
- **URL:** https://dbc-9e376111-e24d.cloud.databricks.com/genie/rooms/01f19a1eb2471ac1a7e433dcc10355f8
- **Catalog:** retail_ai3_dev
- **Warehouse:** Serverless Starter Warehouse

### PROD Workspace ⏳
- **Status:** Needs manual creation
- **Target Catalog:** retail_ai3
- **Warehouse:** (use existing or create new)

## 🚫 Why GitHub Actions Failed (401 Error)

**Root Cause:**
Genie API `/api/2.0/genie/spaces` (POST - create space) requires special authentication that Personal Access Tokens don't provide.

**What Works:**
- ✅ Reading existing spaces (GET /api/2.0/genie/spaces)
- ✅ Using Genie from workspace UI
- ✅ Databricks SDK read operations (w.genie.get_space, list_spaces)

**What Doesn't Work:**
- ❌ Creating spaces via API with PAT
- ❌ GitHub Actions with regular tokens

## ✅ Recommended Deployment Approach

### Option 1: Manual Space Creation (CURRENT)

**For each workspace (DEV/PROD):**

1. **Open Genie UI**
   - Go to workspace → Genie
   - Click "Create Space"

2. **Configure Space**
   - **Name:** Retail Analytics Starter Space
   - **Description:** (use from genie/space_config.json)
   - **Warehouse:** Select any serverless warehouse
   - **Add Tables:**
     - For DEV: `retail_ai3_dev.gold.*`
     - For PROD: `retail_ai3.gold.*`
   
3. **Add Starter Questions**
   Copy from `genie/space_config.json` → `starter_questions`

4. **Add Benchmark Questions** (optional)
   Copy from `genie/space_config.json` → `benchmark_questions`

5. **Save Space ID**
   - Note the Space ID from URL
   - Update in deployment config

### Option 2: Future - Service Principal

When Service Principal is available:
1. Create SP with Genie permissions
2. Update GitHub secrets to use SP credentials
3. Use OAuth token generation in workflow

### Option 3: Terraform (if available)

```hcl
resource "databricks_sql_genie_space" "retail_analytics" {
  display_name = "Retail Analytics Starter Space"
  description  = "..."
  warehouse_id = "5b8e2cea7c9d6bbf"
  
  table_identifiers = [
    "retail_ai3.gold.customer_service_summary",
    "retail_ai3.gold.product_wise_revenue",
    "retail_ai3.gold.top_customers"
  ]
}
```

## 📋 Manual Deployment Checklist

### DEV Workspace ✅
- [x] Space created
- [x] Tables added (retail_ai3_dev.gold.*)
- [x] Starter questions added
- [x] Benchmark questions added
- [x] Space ID documented

### PROD Workspace
- [ ] Create Space in UI
- [ ] Add tables (retail_ai3.gold.*)
- [ ] Copy starter questions
- [ ] Copy benchmark questions
- [ ] Document Space ID
- [ ] Update README with PROD Space URL

## 🔄 What CI/CD Can Do (Future)

Even without creating spaces, CI/CD could potentially:
- Update space configuration
- Sync table lists
- Update descriptions
- Manage benchmark questions

*(Requires investigation of UPDATE endpoints)*

## 📚 Configuration Reference

All configuration is stored in:
- **Space config:** `genie/space_config.json`
- **Tables schema:** `genie/uc_tables_schema.json`
- **Starter questions:** 3 questions (Ukrainian)
- **Benchmark questions:** 8 questions (UA/EN)

## 🔗 Quick Links

**DEV:**
- Space: https://dbc-9e376111-e24d.cloud.databricks.com/genie/rooms/01f19a1eb2471ac1a7e433dcc10355f8
- Catalog: https://dbc-9e376111-e24d.cloud.databricks.com/explore/data/retail_ai3_dev

**PROD:**
- Workspace: https://dbc-91a4ccf2-831f.cloud.databricks.com
- (Create space and add URL here)

## 💡 Summary

**Current Approach:**
1. Create Genie Spaces **manually** in each workspace (one-time setup)
2. Use GitHub repo to **document configuration** and keep it versioned
3. When/if Databricks adds Service Principal support for Genie API, migrate to automated CI/CD

**Benefits:**
- ✅ Works immediately (no auth issues)
- ✅ Full control in UI
- ✅ Configuration still versioned in Git
- ✅ Can be automated later when API support improves
