# Student Task Manager

A simple task-management web application built with Python Flask. Students can add tasks, view tasks, mark them as completed, and delete them.

## Features
- Add a task
- View the task list
- Mark a task as completed or undo completion
- Delete a task
- Store tasks in a local JSON file

## Technology Stack
Python, Flask, HTML, CSS, JSON, GitHub, Docker, and Jenkins.

## Project Files
- `app.py` - Flask application and user interface
- `tasks.json` - Initial task data
- `requirements.txt` - Python dependency
- `Dockerfile` - Docker image build instructions
- `Jenkinsfile` - Jenkins pipeline for dependency installation, syntax checking, and a basic application smoke test
- `.gitignore` - Files excluded from Git
- `README.md` - Project documentation

## Run Locally
Requires Python 3.12 or a compatible Python 3 version.

```bash
python -m venv venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

Open http://127.0.0.1:5000 in a browser.

## Build and Run with Docker

```bash
docker build -t student-task-manager .
docker run -p 5000:5000 student-task-manager
```

Open http://localhost:5000 in a browser.

Note: For persistent task data when replacing containers, mount a volume and set `TASKS_FILE` to a file in that volume.

## GitHub
Create a GitHub repository and push the contents of this folder. Configure Jenkins to use that repository and its `Jenkinsfile`.

## Jenkins
The included declarative pipeline expects a Jenkins agent with Python and pip installed, plus a POSIX shell (`sh`). It checks out the repository, installs dependencies, checks Python syntax, and runs a Flask test-client smoke test.

## Submission Note
This folder contains the application source code and DevOps configuration files. Docker and Jenkins execution must be performed in their respective environments if execution evidence is required by the instructor.
