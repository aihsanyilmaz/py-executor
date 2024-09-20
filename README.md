# Selenium Service

This project provides an infrastructure for running automation tests using a Flask-based API and Selenium grid.

For the Turkish version of this documentation, please see [README_TR.md](README_TR.md).

## Project Structure

selenium-service/
│
├── flask/ # Flask application
│ ├── app.py # Main Flask application
│ ├── run.py # Module managing Selenium operations
│ ├── fatals.py # Error management module
│ ├── packages/ # Executable Python scripts
│ └── README.txt # Flask API usage guide
├── docker-compose.yml # Docker Compose configuration
└── .env # Environment variables



## Installation

1. Clone the project:
   ```
   git clone https://github.com/aihsanyilmaz/selenium-service.git
   cd selenium-service
   ```

2. Create the `.env` file and set the necessary variables:
   ```
   cp example.env .env
   ```
   Edit the `.env` file and enter the required values.

3. Start the services with Docker Compose:
   ```
   docker-compose up -d
   ```

## Usage

### Flask API

For detailed information about using the Flask API, please refer to the [Flask API Usage Guide](flask/README.md) file.

### Selenium Grid

Selenium Grid runs at `http://localhost:4444`. You can run your Selenium tests using this address.

### Accessing Chrome Nodes via VNC

To access Chrome nodes via VNC:

1. Connect to `localhost:5900`, `localhost:5901`, etc. using a VNC client.
2. Use "secret" as the password.

Note: The VNC port range is determined by the `VNC_PORT_START` and `VNC_PORT_END` variables in the `.env` file.

## Configuration

Project configuration is done through the `.env` file. Important configuration variables:

- `CHROME_NODES`: Number of Chrome nodes to be created
- `VNC_PORT_START` and `VNC_PORT_END`: Port range to be used for VNC ports
- `PUSHER_*`: Pusher configuration (for real-time notifications)
- `AUTH_HASH`: Hash used for API authentication

## Development

To add new packages:

1. Create a new Python file under the `flask/packages/` directory.
2. Define the `boot` function in the file.
3. Perform the desired operations using Selenium and Pusher functions.

For an example package, you can look at the `flask/packages/example.py` file.

## Troubleshooting

- If you're having trouble starting the services, use the `docker-compose logs` command to check the error messages.
- If you're having issues with VNC connection, check your firewall settings and make sure the necessary ports are open.

## Contributing

1. Fork this repository
2. Create a new feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push your branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.