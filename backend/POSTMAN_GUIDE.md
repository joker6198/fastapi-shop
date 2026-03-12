# Postman Guide

Это краткое руководство по проверке текущего FastAPI backend через Postman.

## 1. Запуск сервера

Из папки `fastapi_shop/backend`:

```bash
.venv/bin/python run.py
```

Если сервер поднялся, базовый адрес будет:

```text
http://127.0.0.1:8000
```

Проверка в браузере:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/api/docs`
- `http://127.0.0.1:8000/health`

## 2. Настройка Postman

Удобно создать environment с переменной:

```text
base_url = http://127.0.0.1:8000
```

Тогда в запросах можно писать:

```text
{{base_url}}/api/categories
```

Для `POST` и `PUT`:

- вкладка `Body`
- выбрать `raw`
- выбрать формат `JSON`

## 3. Что можно тестировать сейчас

В текущем проекте есть:

- служебные роуты `GET /` и `GET /health`
- категории `GET /api/categories`, `GET /api/categories/{id}`
- товары `GET /api/products`, `GET /api/products/{id}`, `GET /api/products/category/{category_id}`
- корзина `POST /api/cart/add`, `POST /api/cart`, `PUT /api/cart/update`, `DELETE /api/cart/remove/{product_id}`

Сейчас роутов создания категории и товара через API нет. То есть таблицы создаются автоматически, но наполнять их нужно отдельно, пока вы не добавите `POST` эндпоинты.

## 4. Базовые запросы

### Проверка сервера

`GET {{base_url}}/`

Ожидаемый ответ:

```json
{
  "message": "Welcome to fastapi shop API",
  "docs": "api/docs"
}
```

`GET {{base_url}}/health`

Ожидаемый ответ:

```json
{
  "status": "healthy"
}
```

## 5. Категории

### Получить все категории

`GET {{base_url}}/api/categories`

Если данных пока нет, ответ обычно будет:

```json
[]
```

### Получить категорию по id

`GET {{base_url}}/api/categories/1`

Если категория найдена:

```json
{
  "id": 1,
  "name": "Phones",
  "slug": "phones"
}
```

Если не найдена, обычно будет `404`.

## 6. Товары

### Получить все товары

`GET {{base_url}}/api/products`

Ожидаемый формат:

```json
{
  "products": [],
  "total": 0
}
```

### Получить товар по id

`GET {{base_url}}/api/products/1`

Ожидаемый формат:

```json
{
  "id": 1,
  "name": "iPhone 15",
  "description": "Smartphone",
  "price": 999.0,
  "category_id": 1,
  "image_url": "static/images/iphone.jpg",
  "created_at": "2026-03-12T10:00:00",
  "category": {
    "id": 1,
    "name": "Phones",
    "slug": "phones"
  }
}
```

### Получить товары по категории

`GET {{base_url}}/api/products/category/1`

По смыслу этот эндпоинт должен возвращать список товаров категории:

```json
{
  "products": [
    {
      "id": 1,
      "name": "iPhone 15",
      "description": "Smartphone",
      "price": 999.0,
      "category_id": 1,
      "image_url": "static/images/iphone.jpg",
      "created_at": "2026-03-12T10:00:00",
      "category": {
        "id": 1,
        "name": "Phones",
        "slug": "phones"
      }
    }
  ],
  "total": 1
}
```

## 7. Корзина

Корзина сейчас хранится не в БД, а в виде словаря вида:

```json
{
  "1": 2,
  "3": 1
}
```

Это значит:

- товар `1` в количестве `2`
- товар `3` в количестве `1`

Важно: в JSON ключи всегда строки. FastAPI/Pydantic потом преобразует их в `int`.

### Добавить товар в корзину

`POST {{base_url}}/api/cart/add`

Body:

```json
{
  "product_id": 1,
  "quantity": 2,
  "cart": {}
}
```

Пример ответа:

```json
{
  "cart": {
    "1": 2
  }
}
```

Если корзина уже есть:

```json
{
  "product_id": 3,
  "quantity": 1,
  "cart": {
    "1": 2
  }
}
```

Ответ:

```json
{
  "cart": {
    "1": 2,
    "3": 1
  }
}
```

### Получить детали корзины

`POST {{base_url}}/api/cart`

Body:

```json
{
  "1": 2,
  "3": 1
}
```

Ожидаемый формат:

```json
{
  "items": [
    {
      "product_id": 1,
      "name": "iPhone 15",
      "price": 999.0,
      "quantity": 2,
      "subtotal": 1998.0,
      "image_url": "static/images/iphone.jpg"
    }
  ],
  "total": 1998.0,
  "items_count": 2
}
```

### Обновить количество товара в корзине

`PUT {{base_url}}/api/cart/update`

Body:

```json
{
  "product_id": 1,
  "quantity": 5,
  "cart": {
    "1": 2,
    "3": 1
  }
}
```

Ожидаемая логика:

```json
{
  "cart": {
    "1": 5,
    "3": 1
  }
}
```

### Удалить товар из корзины

`DELETE {{base_url}}/api/cart/remove/1`

Body:

```json
{
  "cart": {
    "1": 2,
    "3": 1
  }
}
```

Ожидаемый ответ:

```json
{
  "cart": {
    "3": 1
  }
}
```

## 8. Практический порядок тестирования

Удобная последовательность:

1. Проверить `GET /health`
2. Проверить `GET /api/categories`
3. Проверить `GET /api/products`
4. Если в БД есть товары, проверить `GET /api/products/1`
5. Проверить `POST /api/cart/add`
6. Проверить `POST /api/cart`
7. Проверить `PUT /api/cart/update`
8. Проверить `DELETE /api/cart/remove/{product_id}`

## 9. Если получаете ошибку

Что проверить первым:

- сервер запущен именно из `fastapi_shop/backend`
- открыт адрес `http://127.0.0.1:8000`, а не `0.0.0.0`
- в Postman для `POST` и `PUT` выбран `Body -> raw -> JSON`
- у товара и категории уже есть данные в БД, если вы тестируете `GET /{id}`

Если приходит `500`, смотрите traceback в терминале, где запущен сервер. Для FastAPI это главный источник точной причины ошибки.
