from flask import Flask
from pymongo import MongoClient, errors
import os
from app import config

# Initialize the Flask app
app = Flask(__name__)

# Function to get configuration values with error handling
def get_config_value(key, default=None):
    try:
        value = getattr(config, key)
        if value is None:
            raise ValueError(f"Configuration value for {key} is missing")
        return value
    except AttributeError:
        if default is not None:
            return default
        raise ValueError(f"Configuration value for {key} is missing")

# Connect to MongoDB
try:
    client = MongoClient(
        host=get_config_value('MONGO_HOST'),
        port=get_config_value('MONGO_PORT'),
        username=get_config_value('MONGO_USERNAME'),
        password=get_config_value('MONGO_PASSWORD')
    )
    db = client.task_manager
    tasks_collection = db.tasks_collection
except ValueError as e:
    print(f"Configuration error: {e}")
    os._exit(1)
except errors.PyMongoError as e:
    print(f"Database connection error: {e}")
    os._exit(1)

# Import routes (to avoid circular imports)
from app import routes
