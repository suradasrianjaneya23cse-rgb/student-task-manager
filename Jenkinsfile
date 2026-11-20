pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m pip install -r requirements.txt'
            }
        }

        stage('Check Python Syntax') {
            steps {
                sh 'python -m py_compile app.py'
            }
        }

        stage('Application Smoke Test') {
            steps {
                sh '''
                    TASKS_FILE=jenkins-test-tasks.json python - <<'PY'
from app import app, DATA_FILE

client = app.test_client()
response = client.get("/")
assert response.status_code == 200
assert b"Student Task Manager" in response.data

client.post("/add", data={"task": "Jenkins test task"})
assert b"Jenkins test task" in client.get("/").data
client.get("/complete/0")
client.get("/delete/0")

if DATA_FILE.exists():
    DATA_FILE.unlink()

print("Application smoke test passed.")
PY
                '''
            }
        }
    }

    post {
        success {
            echo 'Student Task Manager pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
