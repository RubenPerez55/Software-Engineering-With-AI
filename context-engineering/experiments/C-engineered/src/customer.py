import re
from dataclasses import dataclass

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s\.]+(\.[^@\s\.]+)+$")

@dataclass
class Customer:
    customer_id: int
    name: str
    email: str
    created_by: str
    updated_by: str

def update_customer_email(customer, new_email, updated_by):
    if customer is None:
        raise ValueError("customer-not-found")
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        raise ValueError("invalid-email")
    customer.email = new_email.lower()
    customer.updated_by = updated_by
    return customer
