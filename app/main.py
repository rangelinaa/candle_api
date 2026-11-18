from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Candle Shop API")

categories: dict[int, dict] = {}
products: dict[int, dict] = {}
customers: dict[int, dict] = {}
orders: dict[int, dict] = {}


def next_id(store: dict) -> int:
    return max(store, default=0) + 1


class CategoryIn(BaseModel):
    name: str


class ProductIn(BaseModel):
    name: str
    price: float
    category_id: int
    description: Optional[str] = None
    stock: int = 0


class CustomerIn(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int


class OrderIn(BaseModel):
    customer_id: int
    items: list[OrderItemIn]


# 1. GET /categories
@app.get("/categories")
def list_categories():
    return list(categories.values())


# 2. POST /categories
@app.post("/categories", status_code=201)
def create_category(data: CategoryIn):
    cid = next_id(categories)
    categories[cid] = {"id": cid, **data.model_dump()}
    return categories[cid]


# 3. GET /products
@app.get("/products")
def list_products():
    return list(products.values())


# 4. GET /products/{product_id}
@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(404, "Product not found")
    return products[product_id]


# 5. POST /products
@app.post("/products", status_code=201)
def create_product(data: ProductIn):
    if data.category_id not in categories:
        raise HTTPException(400, "Category does not exist")
    pid = next_id(products)
    products[pid] = {"id": pid, **data.model_dump()}
    return products[pid]


# 6. PUT /products/{product_id}
@app.put("/products/{product_id}")
def update_product(product_id: int, data: ProductIn):
    if product_id not in products:
        raise HTTPException(404, "Product not found")
    products[product_id] = {"id": product_id, **data.model_dump()}
    return products[product_id]


# 7. DELETE /products/{product_id}
@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(404, "Product not found")
    del products[product_id]


# 8. POST /customers
@app.post("/customers", status_code=201)
def create_customer(data: CustomerIn):
    cid = next_id(customers)
    customers[cid] = {"id": cid, **data.model_dump()}
    return customers[cid]


# 9. POST /orders
@app.post("/orders", status_code=201)
def create_order(data: OrderIn):
    if data.customer_id not in customers:
        raise HTTPException(400, "Customer does not exist")
    total = 0.0
    items = []
    for it in data.items:
        p = products.get(it.product_id)
        if not p:
            raise HTTPException(400, f"Product {it.product_id} does not exist")
        total += p["price"] * it.quantity
        items.append({**it.model_dump(), "unit_price": p["price"]})
    oid = next_id(orders)
    orders[oid] = {
        "id": oid,
        "customer_id": data.customer_id,
        "items": items,
        "total": round(total, 2),
        "status": "new",
        "created_at": datetime.utcnow().isoformat(),
    }
    return orders[oid]


# 10. GET /orders
@app.get("/orders")
def list_orders():
    return list(orders.values())
