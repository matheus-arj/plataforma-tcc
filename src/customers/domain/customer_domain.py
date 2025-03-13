class CustomerDomain:
    def __init__(self, name: str, email: str):
        self.id = None
        self.name = name
        self.email = email

    def set_id(self, customer_id: int):
        self.id = customer_id

    def __str__(self):
        return f'Customer ID: {self.id}, Name: {self.name}, Email: {self.email}'
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }