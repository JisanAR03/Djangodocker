
# ArtixCore Django Docker Setup

This repository contains the Docker setup for the ArtixCore Django application. It includes all necessary configurations to get the application running with Docker.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Docker and Docker Compose on your machine.
- You have basic knowledge of Docker and Docker Compose.

## Getting Started

Follow these steps to get your ArtixCore Django application running:

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
cd to clone directory
```

### 2. Build the Docker Containers

Build the Docker containers using Docker Compose:

```bash
docker-compose build
```

This command builds the Docker images as defined in the `docker-compose.yml` file.

### 3. Run the Docker Containers

Start the Docker containers:

```bash
docker-compose up
```

This command starts the Docker containers. Your Django application should now be up and running.

### 4. Install Composer Dependencies

access the bash terminal of your container:

#### a. Get the Container ID

Find out the container ID of your app:

```bash
docker ps
```

Look for the container running your Django application and note down its ID.

#### b. Open Container's Bash Terminal

Access the bash terminal of your container: 

```bash
docker exec -it <container id> /bin/bash
```

Replace `<container id>` with the actual container ID you noted earlier.

#### c. migrate for adding table to database

Inside the container, run the Composer install command:

```bash
python manage.py migrate
```


## Accessing the Application

Once the containers are running, and the application is set up:

- The Django application should be accessible at `http://localhost:5000` (or another port if you configured it differently).

## Contributing

For any changes or improvements, please open an issue first to discuss what you would like to change. 

<!-- exception: UPDATE admin_app_customuser SET user_type = 'supreme_admin' WHERE id = '1'; -->