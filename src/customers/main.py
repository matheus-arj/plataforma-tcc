from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from storage.customer import CustomerStorage
from domain.customer import CustomerDomain

app = FastAPI()

storage = CustomerStorage()

class CustomerRequest(BaseModel):
    name: str
    email: str

@app.get('/customers')
async def get_customers():
    customers = storage.get_all()
    return [customer.dict() for customer in customers]

@app.post('/customers')
async def add_customer(customer: CustomerRequest):
    customer_domain = CustomerDomain(customer.name, customer.email)
    customer_id = storage.add(customer_domain)
    return {'customer_id': customer_id}
