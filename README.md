# Flask Task Manager 
Simple Flask (Python) app with basic CRUD operations for MongoDB, managed with Docker Compose.

# Technology
- Python: 3.10.15
- Flask: 2.3.2
- Pymongo: 4.10.1
- Docker: 27.2.0
- Github action to check the code quality

# To create and run the containers
Please make sure you have the Docker installed on your machine.
```
$ docker --version
Docker version 27.2.0, build 3ab4256
```
<br>

Navigate to the root directory of the project and execute following command:
```
docker-compose up
```
<br>

This will build images, create network and the volume and run the containers, as it is described in the `docker-compose.yaml` file:
```
$ docker images 
REPOSITORY     TAG       IMAGE ID       CREATED         SIZE
task-manager   latest    bc621aa9efbd   6 minutes ago   140MB
mongo          latest    77c59b638412   5 days ago      855MB
```
```
$ docker network ls
NETWORK ID     NAME                   DRIVER    SCOPE
5dba91cbd731   bridge                 bridge    local
7911564b26e6   host                   host      local
ce82d2e870de   none                   null      local
8d060ed9f258   task_manager_network   bridge    local
```
```
$ docker volume ls
DRIVER    VOLUME NAME
local     task-manager-data
```
```
$ docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                    NAMES
9685d50f1995   task-manager   "python main.py"         7 minutes ago   Up 7 minutes   0.0.0.0:8000->8000/tcp   task_manager
d4e8fd1ca86c   mongo:latest   "docker-entrypoint.s…"   7 minutes ago   Up 7 minutes   27017/tcp                mongodb
```
When both containers are up and running, you can access the Flask app on `http://localhost:8000/`.

# Exposed endpoints
Following endpoints will be exposed:

| Methods | Urls         | Action                  |
|---------|--------------|-------------------------|
| POST    | /tasks       | Creates task            |
| GET     | /tasks       | Get all tasks           |
| GET     | /tasks/{id}  | Get task by it's id     |
| PUT     | /tasks/{id}  | Update task by it's id  |
| DELETE  | /tasks/{id}  | Delete task by it's id  |

# Examples
Create a task:
```
$ curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d'{"title":"New Task", "description":"This is a new task description"}'
```
Response returned:
```
{
  "message": "Task created",
  "task": {
    "description": "This is a new task description",
    "id": "4a4abc57-ed19-46d0-b9df-93afb7ccb7d7",
    "title": "New Task"
  }
}
```
<br>

Get all tasks:
```
$ curl -X GET http://localhost:8000/tasks
```
Response returned:
```
[
  {
    "description": "This is a new task description",
    "id": "4a4abc57-ed19-46d0-b9df-93afb7ccb7d7",
    "title": "New Task"
  }
]
```
<br>

Get task by it's id:
```
$ curl -X GET http://localhost:8000/tasks/4a4abc57-ed19-46d0-b9df-93afb7ccb7d7
```
Response returned:
```
{
  "description": "This is a new task description",
  "id": "4a4abc57-ed19-46d0-b9df-93afb7ccb7d7",
  "title": "New Task"
}
```
<br>

Update task by it's id:
```
$ curl -X PUT http://localhost:8000/tasks/4a4abc57-ed19-46d0-b9df-93afb7ccb7d7 -H "Content-Type: application/json" -d'{"title":"Updated Task", "description":"This is an updated task description"}'
```
Response returned:
```
{
  "message": "Task updated"
}
```
<br>

Delete task by it's id:
```
$ curl -X DELETE http://localhost:8000/tasks/4a4abc57-ed19-46d0-b9df-93afb7ccb7d7
```
Response returned:
```
{
  "message": "Task deleted"
}
```
# Clean up the environment
To clean up everything, execute following command:
```
docker-compose down -v
[+] Running 4/4
 ✔ Container task_manager        Removed      0.6s 
 ✔ Container mongodb             Removed      0.2s 
 ✔ Volume task-manager-data      Removed      0.0s 
 ✔ Network task_manager_network  Removed      0.0s      
```

# Licence
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
