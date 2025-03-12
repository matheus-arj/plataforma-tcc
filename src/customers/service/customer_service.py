import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from customers.domain.customer_domain import CustomerDomain
from customers.storage.customer_storage import CustomerStorage

class CustomerService:
    def __init__(self):
        self.storage = CustomerStorage()
        logging.info("[CUSTOMER-SERVICE] Service initialized")

    def get(self, id: int) -> CustomerDomain:
        ret = None

        try:
            ret = self.storage.get(id)
            logging.info(f"[CUSTOMER-SERVICE] Customer retrieved")
        except Exception as e:
            logging.error(f"[CUSTOMER-SERVICE] Error retrieving customer: {e}")

        return ret
    
    def get_all(self) -> list:
        ret = []

        try:
            ret = self.storage.get_all()
            logging.debug("[CUSTOMER-SERVICE] All users retrieved")
        except Exception as e:
            logging.error(f"[CUSTOMER-SERViCE] Error to get all users")
        
        return ret

    def add(self, customer: CustomerDomain) -> int:
        ret = None

        try:
            ret = self.storage.add(customer)
            logging.info(f"[CUSTOMER-SERVICE] Customer added")
        except Exception as e:
            logging.error(f"[CUSTOMER-SERVICE] Error adding new customer: {e}")
        return ret
    
    def update(self, customer: CustomerDomain) -> bool:
        ret = False
        try:
            ret = self.storage.update(customer)
            logging.info(f"[CUSTOMER-SERVICE] Customer updated")
        except Exception as e:
            logging.error(f"[CUSTOMER-SERVICE] Error updating customer: {e}")
            return ret
        
    def delete(self, id: int) -> bool:
        ret = False

        try:
            ret = self.storage.delete(id)
            logging.info(f"[CUSTOMER-SERVICE] Customer deleted")
        except Exception as e:
            logging.error(f"[CUSTOMER-SERVICE] Error deleting customer: {e}")
        
        return ret