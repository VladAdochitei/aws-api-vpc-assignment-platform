# AWS VPC&Subnet Provisioning Engine

A simple Flask web UI for managing AWS VPCs and Subnets.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export API_BASE_URL="https://your-api-gateway-url/dev"
export API_KEY="your-api-key"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD="your-secure-password"
export SECRET_KEY="your-secret-key"
```

3. Run the application:
```bash
make run
```

Or directly:
```bash
python app.py
```

The app will start on `http://localhost:5000`

## Authentication

The application is protected with an admin login. All requests require authentication.

Default credentials (development):
- Username: `admin`
- Password: `admin`

Change these via environment variables in production:
```bash
export ADMIN_USERNAME="your-admin-user"
export ADMIN_PASSWORD="your-secure-password"
```

## Testing

Run integration tests against the API:
```bash
make test
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_BASE_URL` | `https://wevckik1ug.execute-api.eu-central-1.amazonaws.com/dev` | Backend API URL |
| `API_KEY` | `dev-local-key-CHANGE-ME` | API authentication key |
| `ADMIN_USERNAME` | `admin` | Admin username |
| `ADMIN_PASSWORD` | `admin` | Admin password |
| `SECRET_KEY` | `dev-secret-key-change-in-production` | Flask session secret |

## Features

- **VPC Management**
  - List all VPCs
  - Create new VPCs
  - View VPC details
  - Edit VPC properties
  - Delete VPCs

- **Subnet Management**
  - List all subnets
  - Create subnets within a VPC
  - View subnet details
  - Edit subnet properties
  - Delete subnets

- **Admin Authentication**
  - Login/logout
  - Session management
  - No database required
