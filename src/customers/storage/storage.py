import psycopg2
import logging

logger = logging.getLogger(__name__)

class CustomerStorage:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
            host='${{ POSTGRES_HOST }}',
            port='${{ POSTGRES_PORT }}',
            user='${{ POSTGRES_USER }}',
            password='${{ POSTGRES_PASSWORD }}',
            database='${{ POSTGRES_DB }}'
        )
            self.__create()
            logger.debug('Connected to database')

        except Exception as e:
            logger.error(f'Error connecting to database: {e}')
    
    def __create(self):
        if self.connection is None:
            logging.error(f"[CUSTOMER-STORAGE] Connection error!")
            return
        
        c = self.connection.cursor()
        c.execute(''''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
            );
        ''')

        self.connection.commit()