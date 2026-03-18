# 🌸 Containerized Iris ML Predictor

**Welcome to my first Docker project!** This project is a microservice-based web application that trains and serves a Machine Learning model using the classic Iris dataset. It is built to demonstrate containerization, multi-tier architecture, and basic MLOps principles.

## 🏗️ Architecture
This application runs across two isolated Docker containers connected via a private Docker network:
* **The Web App (Flask/Scikit-Learn):** A custom Python image that handles web traffic, trains the Random Forest classifier, saves the model state, and makes real-time predictions.
* **The Database (Redis):** An in-memory cache used to persistently track site visitor counts across container restarts.

## 🚀 How to Run the App Locally

To run this project on your own machine, you just need Docker installed. 

1. **Clone the repository:**
   git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git)
   cd YOUR_REPO_NAME

2. **Build and start the containers:**
    docker-compose up --build

3. **Use the App:**
Open your browser and navigate to http://localhost:8000/.
(Note: You must click "Train Model Now" before you can make predictions!)

4. **Shut it down:**
    docker-compose down

More about Docker Commands
As part of this project, I utilized the following commands to build, run, and publish my architecture:

docker-compose up --build: This command reads the docker-compose.yml file, builds the custom Flask image from the Dockerfile, downloads the Redis image, and spins up the entire connected network. The --build flag forces it to install any new dependencies in requirements.txt.

docker-compose down: Safely shuts down and removes all containers and networks created by the up command.

docker tag <local-image> <username>/<repo-name>:latest: This attaches my specific Docker Hub username to the local image, which is required before uploading it to the cloud.

docker push <username>/<repo-name>:latest: Uploads the fully built, heavy container image to Docker Hub so it can be deployed anywhere.

☁️ What is Docker Hub?
This project's final image was published to Docker Hub.
Docker Hub is a cloud-based container registry (similar to how GitHub is a registry for code). By pushing my built image to Docker Hub, I ensure "Build Once, Run Anywhere." Instead of manually configuring a server with Python and Scikit-Learn to run this app, a production server or a Kubernetes cluster simply needs to pull my image from Docker Hub and it will run identically to my local environment.