# Retail Analytics - Databricks CI/CD Project

Automated deployment of Retail Analytics Genie Space across multiple Databricks workspaces using GitHub Actions.

## 📁 Project Structure

```
retail-analytics_new/
├── .github/workflows/       # GitHub Actions CI/CD workflows
│   ├── validate.yml        # PR validation
│   ├── deploy-dev.yml      # DEV deployment
│   └── deploy-prod.yml     # PROD deployment
├── genie/
│   ├── space_config.json   # Genie Space configuration
│   └── uc_tables_schema.json # Unity Catalog tables schema
├── scripts/
│   └── deploy_genie_space.py # Genie Space deployment script
├── databricks.yml           # Databricks Asset Bundle config
└── README.md
```

## 🚀 Environments

| Environment | Workspace | Catalog |
|------------|-----------|---------|
| **DEV** | `dbc-9e376111-e24d.cloud.databricks.com` | `retail_ai3_dev` |
| **PROD** | `dbc-91a4ccf2-831f.cloud.databricks.com` | `retail_ai3` |

## 📊 Genie Space Components

**Tables:**
* `retail_ai3.gold.customer_service_summary` - Customer service issues summary
* `retail_ai3.gold.product_wise_revenue` - Revenue by product
* `retail_ai3.gold.top_customers` - Top customers by spending

**Features:**
* 3 starter questions (Ukrainian)
* 8 benchmark questions (Ukrainian + English)
* Bilingual support (Ukrainian/English)

## ⚙️ Setup Instructions

### 1. GitHub Secrets Configuration

Add the following secrets in your GitHub repository:
**Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Value | Description |
|------------|-------|-------------|
| `DEV_DATABRICKS_HOST` | `https://dbc-9e376111-e24d.cloud.databricks.com` | DEV workspace URL |
| `DEV_DATABRICKS_TOKEN` | `dapi...` | DEV workspace token |
| `PROD_DATABRICKS_HOST` | `https://dbc-91a4ccf2-831f.cloud.databricks.com` | PROD workspace URL |
| `PROD_DATABRICKS_TOKEN` | `dapi...` | PROD workspace token |

### 2. Create Databricks Tokens

**In each workspace:**
1. Click your username (top right) → **Settings**
2. **Developer** → **Access tokens**
3. **Generate new token**
4. Copy token immediately (shown only once!)
5. Add as GitHub Secret

## 🔄 CI/CD Workflow

### Automatic Deployment

**DEV Deployment:**
```
Push to branch: retail-analytics_new_dev
→ GitHub Actions runs deploy-dev.yml
→ Deploys Genie Space to DEV workspace
```

**PROD Deployment:**
```
Merge PR to main
→ GitHub Actions runs deploy-prod.yml
→ Deploys Genie Space to PROD workspace
```

### Manual Deployment

You can trigger deployment manually:
1. Go to **Actions** tab in GitHub
2. Select workflow (Deploy to Development / Production)
3. Click **Run workflow**

## 📝 Development Workflow

### Making Changes

```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Make changes to genie/space_config.json

# 3. Commit and push
git add .
git commit -m "Update Genie Space configuration"
git push origin feature/your-feature

# 4. Create Pull Request to main
```

### Testing in DEV

```bash
# Push to DEV branch to test
git checkout retail-analytics_new_dev
git merge feature/your-feature
git push origin retail-analytics_new_dev
```

GitHub Actions will automatically deploy to DEV workspace.

## 🔧 Local Deployment (Manual)

```bash
# Export environment variables
export DATABRICKS_HOST="https://dbc-9e376111-e24d.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..."
export CATALOG_NAME="retail_ai3_dev"

# Run deployment script
python3 scripts/deploy_genie_space.py
```

## 📚 Configuration Files

### genie/space_config.json

Complete Genie Space configuration:
* Space metadata (name, description)
* Table identifiers
* Starter questions
* Benchmark questions with expected SQL

### genie/uc_tables_schema.json

Unity Catalog tables schema documentation:
* Table names and types
* Column definitions
* Comments and metadata

## 🛠️ Customization

### Adding New Questions

Edit `genie/space_config.json`:

```json
{
  "starter_questions": [
    {
      "question": "Your new question?"
    }
  ]
}
```

### Changing Tables

Update tables in `genie/space_config.json`:

```json
{
  "tables": [
    "retail_ai3.gold.your_new_table"
  ]
}
```

## 📊 Monitoring

### GitHub Actions

View deployment status:
```
https://github.com/sirskyoleg/retail-analytics_new/actions
```

### Genie Space

Access deployed spaces:
* **DEV:** `https://dbc-9e376111-e24d.cloud.databricks.com/genie`
* **PROD:** `https://dbc-91a4ccf2-831f.cloud.databricks.com/genie`

## 🆘 Troubleshooting

### Deployment Fails

1. Check GitHub Actions logs
2. Verify secrets are correctly set
3. Ensure Databricks tokens are valid
4. Check catalog/table permissions

### Space Not Created

1. Verify tables exist in target catalog
2. Check table permissions
3. Ensure catalog name matches environment

## 📄 License

Internal project for retail analytics.

## 👥 Contact

For questions or support, contact the data team.
