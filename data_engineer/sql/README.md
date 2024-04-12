# Тест SQL

На основе таблиц базы данных, напишите SQL код, который возвращает необходимые результаты
Пример: 

Общее количество товаров
```sql
select count (*) from items
```

## Структура данных

Используемый синтаксис: Oracle SQL или другой

| Сustomer       | Description           |
| -------------- | --------------------- |
| customer\_id   | customer unique id    |
| customer\_name | customer name         |
| country\_code  | country code ISO 3166 |

| Items             | Description       |
| ----------------- | ----------------- |
| item\_id          | item unique id    |
| item\_name        | item name         |
| item\_description | item description  |
| item\_price       | item price in USD |

| Orders       | Description                 |
| ------------ | --------------------------- |
| date\_time   | date and time of the orders |
| item\_id     | item unique id              |
| customer\_id | user unique id              |
| quantity     | number of items in order    |

| Countries     | Description           |
| ------------- | --------------------- |
| country\_code | country code          |
| country\_name | country name          |
| country\_zone | AMER, APJ, LATAM etc. |


| Сonnection\_log         | Description                           |
| ----------------------- | ------------------------------------- |
| customer\_id            | customer unique id                    |
| first\_connection\_time | date and time of the first connection |
| last\_connection\_time  | date and time of the last connection  |

## Задания

### 1) Количество покупателей из Италии и Франции

| **Country_name** | **CustomerCountDistinct** |
| ------------------------- | ----------------------------- |
| France                    | #                             |
| Italy                     | #                             |

```sql
SELECT
    c.country_name,
    COUNT(DISTINCT cu.customer_id) AS CustomerCountDistinct
FROM
    Customers cu
JOIN
    Countries c ON cu.country_code = c.country_code
WHERE
    c.country_name IN ('Italy', 'France')
GROUP BY
    c.country_name;
```

### 2) ТОП 10 покупателей по расходам

| **Customer_name** | **Revenue** |
| ---------------------- | ----------- |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |

```sql
SELECT
    cu.customer_name,
    SUM(o.quantity * i.item_price) AS Revenue
FROM
    Orders o
JOIN
    Customers cu ON o.customer_id = cu.customer_id
JOIN
    Items i ON o.item_id = i.item_id
GROUP BY
    cu.customer_name
ORDER BY
    Revenue DESC
LIMIT 10;

```

### 3) Общая выручка USD по странам, если нет дохода, вернуть NULL

| **Country_name** | **RevenuePerCountry** |
| ------------------------- | --------------------- |
| Italy                     | #                     |
| France                    | NULL                  |
| Mexico                    | #                     |
| Germany                   | #                     |
| Tanzania                  | #                     |

```sql
SELECT
    c.country_name,
    SUM(o.quantity * i.item_price) AS RevenuePerCountry
FROM
    Orders o
JOIN
    Customers cu ON o.customer_id = cu.customer_id
JOIN
    Items i ON o.item_id = i.item_id
JOIN
    Countries c ON cu.country_code = c.country_code
GROUP BY
    c.country_name;
```

### 4) Самый дорогой товар, купленный одним покупателем

| **Customer\_id** | **Customer\_name** | **MostExpensiveItemName** |
| ---------------- | ------------------ | ------------------------- |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |

```sql
SELECT
    o.customer_id,
    cu.customer_name,
    i.item_name AS MostExpensiveItemName
FROM
    Orders o
JOIN
    Customers cu ON o.customer_id = cu.customer_id
JOIN
    Items i ON o.item_id = i.item_id
WHERE
    o.item_id IN (
        SELECT
            item_id
        FROM
            Orders
        WHERE
            customer_id = o.customer_id
        ORDER BY
            item_price DESC
        LIMIT 1
    );

```

### 5) Ежемесячный доход

| **Month (MM format)** | **Total Revenue** |
| --------------------- | ----------------- |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |

```sql
SELECT
    DATE_FORMAT(o.date_time, '%m') AS Month,
    SUM(o.quantity * i.item_price) AS TotalRevenue
FROM
    Orders o
JOIN
    Items i ON o.item_id = i.item_id
GROUP BY
    Month;
```

### 6) Найти дубликаты

Во время передачи данных произошел сбой, в таблице orders появилось несколько 
дубликатов (несколько результатов возвращаются для date_time + customer_id + item_id). 
Вы должны их найти и вернуть количество дубликатов.

```sql
SELECT
    COUNT(*) AS TotalDuplicates
FROM
    (SELECT
        date_time,
        customer_id,
        item_id
     FROM
        Orders
     GROUP BY
        date_time,
        customer_id,
        item_id
     HAVING
        COUNT(*) > 1) AS Duplicates;
```

### 7) Найти "важных" покупателей

Создать запрос, который найдет всех "важных" покупателей,
т.е. тех, кто совершил наибольшее количество покупок после своего первого заказа.

| **Customer\_id** | **Total Orders Count** |
| --------------------- |-------------------------------|
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |

```sql
SELECT
    customer_id,
    COUNT(*) AS TotalOrdersCount
FROM
    Orders
WHERE
    date_time > (SELECT
                    MIN(date_time)
                FROM
                    Orders
                WHERE
                    Orders.customer_id = customer_id)
GROUP BY
    customer_id
ORDER BY
    TotalOrdersCount DESC;
```

### 8) Найти покупателей с "ростом" за последний месяц

Написать запрос, который найдет всех клиентов,
у которых суммарная выручка за последний месяц
превышает среднюю выручку за все месяцы.

| **Customer\_id** | **Total Revenue** |
| --------------------- |-------------------|
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |

```sql
-- result here
```
