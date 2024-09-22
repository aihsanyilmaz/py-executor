# Asynchronous Python Executor API

This FastAPI-based application provides an asynchronous API for executing dynamic Python code. The application can run Python scripts located in the `files/` directory and process the results asynchronously. Pusher integration is used for real-time notifications, allowing instant delivery of progress and results of long-running operations to clients.

## Key Features

- Asynchronous code execution
- Extensibility: Ability to run Python scripts from the `files/` directory
- Real-time notifications: Instant delivery of process status and results using Pusher
- RESTful API: Fast and modern API interface with FastAPI
- API Security: API key-based authentication
- Configurable: Flexible configuration with environment variables
- Docker support: Includes Dockerfile for easy deployment and scaling

## Project Structure

The project structure is as follows:

```
app/
├── files/
│   └── example.py  # Example Python script
├── modules/
│   └── pusher.py
├── __init__.py
├── main.py
├── dependencies.py
├── process.py
├── execution.log
├── requirements.txt
├── Dockerfile
├── example.env
├── .gitignore
├── README.md
└── LICENSE
```

The `files/` directory contains Python scripts to be executed. The `example.py` file is provided as a sample script to demonstrate how to use the API.

## Installation and Running

### Setting Up Environment Variables

1. Copy the `example.env` file to `.env`:
   ```
   cp example.env .env
   ```
2. Open the `.env` file and update the necessary variables with your own values.

### Installation with Docker

1. Clone the project:
   ```
   git clone <repo-url>
   cd <project-directory>
   ```

2. Build the Docker image:
   ```
   docker build -t asynchronous-python-api .
   ```

3. Run the Docker container:
   ```
   docker run -p 8000:8000 remote-async-py-executor
   ```

### Manual Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   uvicorn main:app --reload
   ```

## Usage

1. Place your Python script in the `files/` directory.
2. Use the API to run your script (visit the `/docs` endpoint for details).
3. Receive results in real-time via Pusher.

As an example, you can use the API to run the `files/example.py` file.

## API Documentation

To access the API documentation and view all endpoints:
- Swagger UI: `http://your-domain/docs`

## Pusher Integration

The application uses Pusher for real-time notifications. You can configure your Pusher settings in the `.env` file.

## Security

- All API requests must be authenticated with the `X-API-KEY` header.
- Keep your API key secure and change it regularly.
- Never add the `.env` file to version control.

## Contributing

For bug reports, feature requests, and pull requests, please contact us via GitHub.

## License

[MIT License](LICENSE)
