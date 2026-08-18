# 📋 PROD Genie Space - Інструкція створення

## 🔗 Крок 0: Відкрийте PROD Workspace

**URL:** https://dbc-91a4ccf2-831f.cloud.databricks.com

1. Увійдіть в акаунт
2. Перейдіть до **Genie** (ліва панель або головне меню)
3. Натисніть **"Create Space"** або **"New Space"**

---

## 📝 Крок 1: Базова інформація

### Назва Space:
```
Retail Analytics Starter Space
```

### Опис (Description):
```
Ласкаво просимо до Genie для аналізу даних роздрібної торгівлі. Тут ви можете задавати питання природною мовою українською або англійською, щоб отримати інсайти про клієнтів, виручку та обслуговування.
```

### Warehouse:
Оберіть будь-який доступний **Serverless Warehouse** або створіть новий

---

## 📊 Крок 2: Додайте таблиці

**ВАЖЛИВО:** Додайте всі 3 таблиці:

```
retail_ai3.gold.customer_service_summary
retail_ai3.gold.product_wise_revenue
retail_ai3.gold.top_customers
```

**Як додати:**
1. У полі "Add tables" введіть повну назву таблиці (catalog.schema.table)
2. Натисніть Enter або "Add"
3. Повторіть для всіх трьох таблиць

---

## ❓ Крок 3: Starter Questions

Додайте ці 3 стартові питання:

### Питання 1:
```
Які найбільш прибуткові продукти?
```

### Питання 2:
```
Яка середня оцінка обслуговування клієнтів?
```

### Питання 3:
```
Які топ-5 клієнтів за виручкою?
```

---

## 🎯 Крок 4: Benchmark Questions (Опціонально)

Якщо є можливість додати benchmark questions, додайте ці 8:

1. **Який продукт має найменшу виручку?**

2. **Покажи всі категорії проблем обслуговування клієнтів**

3. **What is the most common customer service issue category?**

4. **Скільки всього звернень до служби підтримки клієнтів?**

5. **Show me the most profitable products**

6. **Яка загальна виручка від усіх продуктів?**

7. **Who are the top 3 customers by spending?**

8. **Які топ-5 клієнтів за загальною витраченою сумою?**

---

## ✅ Крок 5: Збережіть та задокументуйте

1. **Натисніть "Create" або "Save"**
2. **Скопіюйте Space ID** з URL (формат: `/genie/rooms/{space_id}`)
3. **Оновіть документацію:**
   - Додайте Space ID у `GENIE_DEPLOYMENT_GUIDE.md`
   - Додайте URL Space у README.md

---

## 📋 Фінальний чек-ліст:

- [ ] Відкрито PROD workspace
- [ ] Створено новий Genie Space
- [ ] Додано назву: "Retail Analytics Starter Space"
- [ ] Додано опис
- [ ] Обрано Warehouse
- [ ] Додано 3 таблиці з catalog `retail_ai3.gold`
- [ ] Додано 3 starter questions
- [ ] (Опціонально) Додано 8 benchmark questions
- [ ] Збережено Space
- [ ] Скопійовано Space ID
- [ ] Перевірено, що Space працює (задано тестове питання)
- [ ] Оновлено GENIE_DEPLOYMENT_GUIDE.md з PROD Space ID
- [ ] Оновлено README.md з PROD Space URL

---

## 🔗 Після створення

**PROD Space URL буде:**
```
https://dbc-91a4ccf2-831f.cloud.databricks.com/genie/rooms/{SPACE_ID}
```

Де `{SPACE_ID}` - це ID, який ви скопіюєте після створення.

---

## 📞 Якщо виникли проблеми:

1. **Таблиці не знайдено:**
   - Перевірте, що каталог `retail_ai3` існує в PROD
   - Перевірте, що у вас є права SELECT на ці таблиці

2. **Не можу створити Space:**
   - Перевірте права доступу у workspace
   - Можливо потрібен адмін-доступ для створення Genie Spaces

3. **Warehouse не доступний:**
   - Створіть новий Serverless Warehouse
   - Або зверніться до адміністратора для доступу

---

## ✨ Готово!

Після створення PROD Space у вас буде:
- ✅ DEV Space: https://dbc-9e376111-e24d.cloud.databricks.com/genie/rooms/01f19a1eb2471ac1a7e433dcc10355f8
- ✅ PROD Space: https://dbc-91a4ccf2-831f.cloud.databricks.com/genie/rooms/{YOUR_SPACE_ID}

Обидва Space використовують однакову конфігурацію з Git репозиторію! 🎉
