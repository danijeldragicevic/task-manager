from flask import Flask, jsonify, request
from pymongo import MongoClient, errors
import uuid
import config
import os

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

# Connect to MongoDB using configuration from config.py
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

# Convert MongoDB ObjectId to JSON serializable format
def serialize_task(task):
    return {
        "id": task["id"],
        "title": task["title"],
        "description": task["description"]
    }

# Endpoint to create a new task
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data or "description" not in data:
        return jsonify({"error": "Title and description are required"}), 400

    task = {
        "id": str(uuid.uuid4()),  # Generate a unique ID for the task
        "title": data["title"],
        "description": data["description"]
    }
    try:
        tasks_collection.insert_one(task)
    except errors.PyMongoError as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Task created", "task": serialize_task(task)}), 201

# Endpoint to list all tasks
@app.route("/tasks", methods=["GET"])
def list_tasks():
    try:
        tasks = [serialize_task(task) for task in tasks_collection.find()]
    except errors.PyMongoError as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(tasks), 200

# Endpoint to get a single task by ID
@app.route("/tasks/<id>", methods=["GET"])
def get_task(id):
    try:
        task = tasks_collection.find_one({"id": id})
    except errors.PyMongoError as e:
        return jsonify({"error": str(e)}), 500
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(serialize_task(task)), 200

# Endpoint to update a task by ID
@app.route("/tasks/<id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()
    update_fields = {}
    if "title" in data:
        update_fields["title"] = data["title"]
    if "description" in data:
        update_fields["description"] = data["description"]

    try:
        result = tasks_collection.update_one({"id": id}, {"$set": update_fields})
    except errors.PyMongoError as e:
        return jsonify({"error": str(e)}), 500
    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task updated"}), 200

# Endpoint to delete a task by ID
@app.route("/tasks/<id>", methods=["DELETE"])
def delete_task(id):
    try:
        result = tasks_collection.delete_one({"id": id})
    except errors.PyMongoError as e:
        return jsonify({"error": str(e)}), 500
    if result.deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted"}), 200

# Endpoint to check application health
@app.route("/ping", methods=["GET"])
def get_app_info():
    app_info = {
        "name": get_config_value('APP_NAME'),
        "version": get_config_value('APP_VERSION')
    }
    return jsonify(app_info), 200

# Run the app
if __name__ == "__main__":
    try:
        app.run(debug=False, host=get_config_value('APP_HOST'), port=get_config_value('APP_PORT'))
    except ValueError as e:
        print(f"Configuration error: {e}")
        os._exit(1)