# FastAPI Microservice of Google OR-Tools

This project replaces a Django implementation with FastAPI to provide a lightweight and efficient microservice architecture.

## Features

- FastAPI for high-performance microservices
- Automated schedule generation using Google OR-tools
- Simple POST endpoint to return employee schedules

## Setup

### Installing Python

Ensure you have Python 3.7 or higher installed on your system. You can download the latest version of Python from the [official Python website](https://www.python.org/downloads/).

### Creating and Activating a Virtual Environment

To ensure a clean and isolated environment for running the FastAPI application, it’s best to use a virtual environment. Follow these steps:

1. **Install Virtualenv**: Virtualenv is a tool to create isolated Python environments. Install it using pip:

    ```bash
    pip install virtualenv
    ```
2. **Clone Repository**: create a new directory and clone this repository:

    ```bash
    git clone https://github.com/Raiyan03/OR.git
    ```

2. **Create a Virtual Environment**: Navigate to the root directory of your project and create a virtual environment:

    ```bash
    virtualenv venv
    ```

    This command creates a directory named `venv` that contains the virtual environment.

3. **Activate the Virtual Environment**:

    - **On Windows**:

      ```bash
      venv\Scripts\activate
      ```

    - **On macOS and Linux**:

      ```bash
      source venv/bin/activate
      ```

    You should see the virtual environment’s name (`venv`) in your command prompt, indicating that it’s active.

### Installing Dependencies

With the virtual environment activated, install the required dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
### Running the server

You can start the the FastApi server by using uvicorn

```bash
uvicorn main:app --reload
```

### Deactivating the Virtual Environment

When you’re done working on the project, deactivate the virtual environment by running:

```bash
deactivate
```