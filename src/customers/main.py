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

