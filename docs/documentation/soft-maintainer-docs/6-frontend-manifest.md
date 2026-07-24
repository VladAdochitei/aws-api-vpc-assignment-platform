# Frontend Application Manifest

**Name:** AWS VPC&Subnet Provisioning Engine  
**Type:** Flask web application  
**Location:** `src_frontend/`  
**Purpose:** Web UI for managing AWS VPCs and Subnets

## Architecture

- **APIClient** (`services/api_client.py`) — HTTP client wrapping backend Lambda API
- **Flask App** (`app.py`) — Route handlers and session management
- **Templates** (`templates/`) — Jinja2 HTML with minimal inline CSS

## Authentication

- No database. Credentials via environment variables.
- Login required for all routes except `/login` and `/logout`
- Session stored in Flask cookies

**Environment variables:**
```
ADMIN_USERNAME    default: admin
ADMIN_PASSWORD    default: admin
SECRET_KEY        default: dev-secret-key-change-in-production
```

## Routes

### Auth
| Route | Method | Purpose |
|-------|--------|---------|
| `/login` | GET/POST | Login page |
| `/logout` | GET | Destroy session, redirect to login |
| `/` | GET | Redirect to `/vpcs` if logged in, else `/login` |

### VPCs
| Route | Method | Purpose |
|-------|--------|---------|
| `/vpcs` | GET | List all VPCs (table view) |
| `/vpcs/create` | GET/POST | Create VPC form |
| `/vpcs/<vpc_id>` | GET | VPC detail + subnets list |
| `/vpcs/<vpc_id>/edit` | GET/POST | Edit VPC name/region/status |
| `/vpcs/<vpc_id>/delete` | POST | Delete VPC |

### Subnets
| Route | Method | Purpose |
|-------|--------|---------|
| `/subnets` | GET | List all subnets (table view) |
| `/vpcs/<vpc_id>/subnets/create` | GET/POST | Create subnet in VPC |
| `/subnets/<subnet_id>` | GET | Subnet detail |
| `/subnets/<subnet_id>/edit` | GET/POST | Edit subnet name/status |
| `/subnets/<subnet_id>/delete` | POST | Delete subnet |

## Data Flow

1. User submits form → Flask handler validates input
2. Handler calls `APIClient` method with form data
3. APIClient sends HTTP request to backend with `Authorization` header
4. Handler receives response, renders template or flashes error
5. User sees result

## Error Handling

- HTTP errors from backend logged to console
- User sees flash message ("Error: ...") on page
- Failed operations return user to list view

## Dependencies

```
Flask==3.0.0
requests==2.31.0
Werkzeug==3.0.1
```

## Running

```bash
cd src_frontend
export API_BASE_URL="https://api-gateway-url/dev"
export API_KEY="api-key"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD="password"

make run
```

Runs on `http://localhost:5000`

## Templates

All extend `base.html` (navigation, auth check, flash messages).

```
templates/
├── base.html          (layout, nav)
├── login.html         (auth form)
├── vpcs/
│   ├── list.html      (table)
│   ├── create.html    (form)
│   ├── detail.html    (view + subnet list)
│   └── edit.html      (form)
└── subnets/
    ├── list.html      (table)
    ├── create.html    (form)
    ├── detail.html    (view)
    └── edit.html      (form)
```
