import uuid

# Simple in-memory store
schedules = []

def generate_id():
    return str(uuid.uuid4())
