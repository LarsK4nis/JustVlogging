# Microblogging Platform
<p align="center">
  <img src="image-2.png" alt="Main Image" width="35%" />
</p>

## Overview
The Microblogging Platform is a web-based application that allows users to post and share their opinions and comments in a microblogging environment. It is designed to be simple yet functional, catering to those who appreciate minimalism in web design.

## Installation and Setup
The application is containerized using Docker and orchestrated with Docker Compose. This setup ensures easy deployment and management of the application and its associated services.

### Prerequisites
- Docker
- Docker Compose

### Steps to Install
1. **Clone the repository**: Clone the project repository to your local machine.
    ```bash
    git clone https://github.com/LarsK4nis/JustVlogging
    ```
2. **Navigate to the project directory**:
    ```bash
    cd /JustVlogging
    ```
3. **Build and run the containers**:
    ```bash
    docker-compose up --build
    ```

## Architecture
The application follows a standard structure for Flask-based applications and includes the following components:

- `app/`: Main application directory with Flask routes, forms, templates, and utility scripts.
- `docker/`: Contains Dockerfiles for setting up the Python/Flask environment and the PostgreSQL database.
- `docker-compose.yml`: Defines and configures the services of the application.

### Services
- **Flask Application**: The main web application built with Flask.
- **PostgreSQL Database**: For storing user and post data.
- **MinIO**: Object storage server for handling image uploads.
- **pgAdmin**: Web-based PostgreSQL database management.

### Credentials
- **pgAdmin**:
  - **URL**: `http://localhost:8080`
  - **Email**: `admin@admin.com`
  - **Password**: `root`
  - **Database_Name**: `microblogging`
  <p align="center">
    <img src="image.png" alt="pgAdmin Credentials" width="75%" />
  </p>
  - **HostName/Address**: `db`
  - **Username**: `user`
  - **Password**: `password`
  <p align="center">
    <img src="image-1.png" alt="Database Connection" width="75%" />
  </p>
- **PostgreSQL**:
  - **User**: `user`
  - **Password**: `password`

### Project Structure
<pre><code>
.
├── README.md                    # Project overview and setup instructions
├── app                          # Main application directory
│   ├── __init__.py              # Initializes the Flask app and configures components
│   ├── forms.py                 # Defines forms for user input
│   ├── minio_utils.py           # Utility functions for MinIO operations
│   ├── models.py                # Database models
│   ├── routes.py                # Flask routes for different endpoints
│   ├── static                   # Contains static files like CSS, JavaScript, and images
│   ├── templates                # HTML templates for rendering views
│   └── utils.py                 # Additional utility functions
├── app.py                       # Entry point to run the Flask application
├── docker                       # Contains Docker related files
├── docker-compose.yml           # Docker Compose file to orchestrate containers
├── requirements.txt             # Python dependencies for the project
└── tests                        # Contains test scripts for the application
</code></pre>

## Testing
The `tests/` directory contains scripts to test various components of the application. Run these tests to ensure the application functions as expected.

## Contributing
Contributions to the project are welcome. Please follow the standard Git workflow for contributions.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
