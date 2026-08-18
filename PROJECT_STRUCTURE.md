# 📂 Структура проекту - Створення таблиць

## 🎯 Де знаходиться створення таблиць

### 1️⃣ SQL DDL Файли (схеми таблиць)
**Локація:** `src/schemas/`

```
src/schemas/
├── customer_service_summary.sql  ← DDL для таблиці customer service
├── product_wise_revenue.sql      ← DDL для таблиці product revenue  
└── top_customers.sql             ← DDL для таблиці top customers
```

**Що вони роблять:**
- Створюють таблиці через `CREATE TABLE IF NOT EXISTS`
- Використовують змінні `${catalog}` та `${schema}` з databricks.yml
- Автоматично підставляються при deployment

**Приклад:**
```sql
CREATE TABLE IF NOT EXISTS ${catalog}.${schema}.customer_service_summary (
  issue_category STRING COMMENT 'Category of customer service issue',
  total_records BIGINT COMMENT 'Total number of records'
)
USING delta;
```

---

### 2️⃣ DABs Resource Configuration
**Локація:** `resources/tables.yml`

```yaml
resources:
  jobs:
    create_uc_tables:
      name: Create UC Tables - ${bundle.target}
      tasks:
        - task_key: create_customer_service_summary
          sql_task:
            warehouse_id: ${var.warehouse_id}
            file:
              path: ../src/schemas/customer_service_summary.sql
```

**Що це робить:**
- Створює Databricks Job для створення таблиць
- Запускає SQL файли на SQL Warehouse
- Виконується автоматично при `databricks bundle deploy`

---

### 3️⃣ Databricks Asset Bundle Config
**Локація:** `databricks.yml`

```yaml
bundle:
  name: retail-analytics

include:
  - resources/*.yml  ← Включає resources/tables.yml

targets:
  dev:
    variables:
      catalog: retail_ai3_dev
      schema: gold
      warehouse_id: 5b8e2cea7c9d6bbf
      
  prod:
    variables:
      catalog: retail_ai3
      schema: gold
      warehouse_id: ${var.prod_warehouse_id}
```

**Що це робить:**
- Визначає змінні для DEV та PROD
- Підставляє їх в SQL файли
- Керує deployment процесом

---

## 🔄 Як працює автоматичне створення таблиць

### Крок 1: Git Push
```bash
git push origin retail-analytics_new_dev
```

### Крок 2: GitHub Actions
`.github/workflows/smart-deploy.yml` запускається автоматично

### Крок 3: Databricks Bundle Deploy
```bash
databricks bundle deploy --target dev
```

### Крок 4: Виконання
1. Читає `databricks.yml`
2. Підставляє змінні:
   - `${catalog}` → `retail_ai3_dev`
   - `${schema}` → `gold`
   - `${var.warehouse_id}` → `5b8e2cea7c9d6bbf`
3. Створює Job з 3 tasks
4. Кожен task виконує свій SQL файл
5. Таблиці створюються в `retail_ai3_dev.gold`

---

## 📊 Повна структура проекту

```
retail-analytics_new/
│
├── databricks.yml                    ← Головна конфігурація DABs
│
├── src/
│   ├── schemas/                      ← ⭐ SQL DDL для таблиць
│   │   ├── customer_service_summary.sql
│   │   ├── product_wise_revenue.sql
│   │   └── top_customers.sql
│   │
│   └── pipelines/                    ← DLT pipelines (bronze/silver/gold)
│       ├── bronze/
│       ├── silver/
│       └── gold/
│
├── resources/                        ← ⭐ DABs ресурси
│   └── tables.yml                    ← Job для створення таблиць
│
├── genie/                            ← Genie Space конфігурація
│   ├── space_config.json
│   └── uc_tables_schema.json
│
├── scripts/                          ← Deployment скрипти
│   ├── deploy_genie_space.py
│   └── deploy_genie_local.py
│
└── .github/workflows/                ← CI/CD workflows
    ├── smart-deploy.yml              ← Головний deployment workflow
    ├── deploy-dev.yml
    ├── deploy-prod.yml
    └── validate.yml
```

---

## 🎯 Швидкі відповіді

### ❓ "Де створення таблиць?"
**Відповідь:** 
- SQL: `src/schemas/*.sql`
- Конфігурація: `resources/tables.yml`
- Змінні: `databricks.yml`

### ❓ "Як додати нову таблицю?"
**Відповідь:**
1. Створіть SQL файл у `src/schemas/new_table.sql`
2. Додайте task у `resources/tables.yml`
3. Commit + push → автоматичний deployment

### ❓ "Як це працює локально?"
**Відповідь:**
```bash
cd /Workspace/Repos/sirsky.oleg@gmail.com/retail-analytics_new
databricks bundle deploy --target dev
```

### ❓ "Де налаштування DEV vs PROD?"
**Відповідь:**
У `databricks.yml` → секція `targets:`
- `dev`: retail_ai3_dev.gold
- `prod`: retail_ai3.gold

---

## ✅ Тепер це РЕАЛЬНА автоматизація!

**До:**
- ❌ Немає SQL файлів
- ❌ Немає DABs конфігурації
- ❌ Тільки експортована схема

**Після:**
- ✅ SQL DDL файли готові
- ✅ DABs ресурс налаштований
- ✅ Автоматичний deployment працює
- ✅ Змінні для DEV/PROD
- ✅ Git-based version control
