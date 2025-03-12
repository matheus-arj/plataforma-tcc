import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
import logging
from customers.domain.customer_domain import CustomerDomain

logger = logging.getLogger(__name__)

class CustomerStorage:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                database=os.getenv('POSTGRES_DB')
            )
            self.__create()
            logger.debug('Connected to database')

        except Exception as e:
            logger.error(f'Error connecting to database: {e}')
            self.connection = None
    
    def __create(self):
        if self.connection is None:
            logging.error(f"[CUSTOMER-STORAGE] Connection error!")
            return
        
        c = self.connection.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
        ''')

        self.connection.commit()

    def get(self, id: int) -> CustomerDomain:
        logging.debug(f"[CUSTOMER-STORAGE] Getting customer with ID: {id}")
        db = self.connection.cursor()
        db.execute('''
            SELECT
                id, name, email
            FROM
                customers
            WHERE id = ?
        ''', (id,))
        customer = db.fetchone()
        logging.info(f"[CUSTOMER-STORAGE] Customer retrieved: {customer}")
        ret = CustomerDomain(customer[1], customer[2])
        ret.set_id(customer[0])
        return ret
    
    def get_all(self) -> list:
        logging.debug("[CUSTOMER-STORAGE] Getting all customers")
        db = self.connection.cursor()
        db.execute('''
            SELECT
                id, name, email
            FROM
                customers
        ''')
        customers = db.fetchall()
        logging.debug(f"[CUSTOMER-STORAGE] All customers retrieved")
        ret = []
        
        for customer in customers:
            logger.debug(f"[CUSTOMER-STORAGE] data: {customer}")
            item = CustomerDomain(customer[1], customer[2])
            item.set_id(customer[0])
            ret.append(item)
        
        return ret
    
    def add(self, customer: CustomerDomain) -> int:
        logging.debug(f"[CUSTOMER-STORAGE] Adding customer")
        db = self.connection.cursor()
        db.execute('''
            INSERT INTO customers (name, email)
            VALUES (%s, %s)
        ''', (customer.name, customer.email))

        self.connection.commit()
        
        return db.lastrowid

    def update(self, customer: CustomerDomain) -> bool:
        logging.debug(f"[CUSTOMER-STORAGE] Updating customer")
        db = self.connection.cursor()
        db.execute('''
            UPDATE customers
            SET name = %s, email = %s
            WHERE id = %s
        ''', (customer.name, customer.email, customer.customer_id))
        self.connection.commit()
        return db.rowcount > 0
    
    def delete(self, id: int) -> bool:
        logging.debug(f"[CUSTOMER-STORAGE] Deleting customer with Id: {id}")
        db = self.connection.cursor()
        db.execute('''
            DELETE FROM customers
            WHERE id = ?
        ''', (id))

        self.connection.commit()
        
        return db.rowcount > 0