from flask import jsonify, request
from app import app, tasks_collection
import uuid
from pymongo import errors

# Convert MongoDB ObjectId to JSON serializable format
def serialize_task(task):
    return {
        "id": task["id"],
        "title": task["title"],
        "description": task["description"]
    }

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

@app.route("/tasks", methods=["GET"])
def list_tasks():
    try:
        tasks = [serialize_task(task) for task in tasks_collection.find()]
    except errors.PyMongoError as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(tasks), 200

@app.route("/tasks/<id>", methods=["GET"])
def get_task(id):
    try:
        task = tasks_collection.find_one({"id": id})
    except errors.PyMongoError as e:
        return jsonify({"error": str(e)}), 500
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(serialize_task(task)), 200

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

@app.route("/healht", methods=["GET"])
def health_check():
    health_info = {
        "status": "up",
        "version": app.config.get("APP_VERSION"),
        "environment": app.config.get("APP_ENV")
    }
    return jsonify(health_info), 200
