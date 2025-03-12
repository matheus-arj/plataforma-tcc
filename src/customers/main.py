import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from dotenv import load_dotenv
import logging
from customers.service import customer_service
from customers.domain.customer_domain import CustomerDomain

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

storage = customer_service.CustomerService()
service = customer_service.CustomerService()

app = FastAPI()

@app.get("/hello")
def hello():
    return {"Hello World"}

@app.get("/customers")
def get_customer():
    return storage.get_all()

@app.post("/customers")
async def add_customer(request: Request):
    logging.info(f"[CUSTOMER-API] Adding new customer: {request}")
    data = await request.json()
    customer = CustomerDomain(data['name'], data['email'])
    customer_id = service.add(customer)
    logging.info(f"customer id {customer_id}")
    return customer

@app.put("/customers/{customer_id}")
async def update_customer(request: Request, customer_id: int):
    logging.info(f"[CUSTOMER-API] Updating customer: {request}")
    data = await request.json()
    customer = CustomerDomain(data['name'], data['email'])
    customer.set_id(customer_id)
    service.update(customer)
    return customer