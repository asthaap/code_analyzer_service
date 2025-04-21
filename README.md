******Code Analyzer Microservice******

This microservice allows users to submit code (e.g., Python, JavaScript) for analysis, including execution time, memory usage, and time/space complexity estimation. Results are stored in MongoDB. It consists of a Python-based backend (Flask) and a React frontend with Tailwind CSS, orchestrated using Docker Compose.
Prerequisites

Docker: Install Docker Desktop and ensure it’s running.
Node.js: Install Node.js (version 16 or higher) for frontend dependency setup.
Git: Install Git to clone the repository.

****Setup Instructions****

**Clone the Repository**
git clone https://github.com/asthaap/code_analyzer_service.git
cd code_analyzer_service

Replace <your-username> with your GitHub username (e.g., Rahul-pro1).

Install Frontend Dependencies Navigate to the frontend/ directory and install Node.js dependencies:
cd frontend
npm install
cd ..


Build and Run with Docker ComposeEnsure Docker is running, then build and start the containers:
docker-compose up --build


This builds the backend (Flask), frontend (React/Nginx), and MongoDB containers.
The --build flag ensures fresh images are created.



**Accessing the Application**

Frontend: Open your browser and visit http://localhost:5173 to access the React-based UI.


**Project Structure**

backend/: Flask-based code-analyzer service.
app.py: Analyzes code, estimates complexity, and stores results in MongoDB.
Dockerfile: Container configuration.
requirements.txt: Python dependencies (Flask, PyMongo, etc.).


frontend/: React frontend with Tailwind CSS.
src/App.jsx: Main React component.
Dockerfile, nginx.conf: Container and Nginx setup.
package.json: Node.js dependencies.


docker-compose.yml: Orchestrates backend, frontend, and MongoDB services.

**Troubleshooting**
MongoDB Connection Errors: Ensure the MongoDB container is running (docker-compose logs mongo). Verify the MONGO_URI is mongodb://mongo:27017/analyzer in the Docker network.
Frontend Not Loading: Confirm npm install was successful and frontend/Dockerfile builds correctly.
Backend Errors: Check backend/requirements.txt for missing dependencies or update pip in Dockerfile.
Port Conflicts: If ports 5173, 5000, or 27017 are in use, update docker-compose.yml with alternative ports.

**Stopping the Application**
To stop the containers:
docker-compose down

**To remove volumes and images (clean slate):**
docker-compose down -v --rmi all

