# Frontend Authentication

## Overview

The frontend uses simple credential-based authentication with no database. Credentials are stored as environment variables and validated on login.

## How It Works

### 1. Login Flow

```
User visits app → Redirect to /login (if not authenticated)
                  ↓
          User enters credentials
                  ↓
          POST /login with username + password
                  ↓
       Validate against env vars ADMIN_USERNAME + ADMIN_PASSWORD
                  ↓
         If valid → Set session['admin'] = True
                 → Flash success message
                 → Redirect to /vpcs
         If invalid → Flash error message
                   → Redirect to /login (stay on page)
```

### 2. Session Management

- Flask stores session in **encrypted cookies** (no server-side session database)
- Session key: `admin` (boolean)
- Cookie expires when browser closes (default Flask behavior)

**Configuration:**
```python
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
```

Changing `SECRET_KEY` invalidates all existing sessions.

### 3. Route Protection

All protected routes use the `@login_required` decorator:

```python
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            flash('Please log in first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/vpcs')
@login_required
def list_vpcs():
    ...
```

**Protected routes:**
- `/vpcs` and all VPC sub-routes
- `/subnets` and all subnet sub-routes

**Unprotected routes:**
- `/login` — Allow login attempt
- `/logout` — Allow logout
- `/` — Redirect to login if not authenticated

### 4. Logout

```
User clicks Logout → GET /logout
                      ↓
              session.pop('admin', None)
                      ↓
              Flash "Logged out" message
                      ↓
              Redirect to /login
```

## Credentials

**Environment Variables:**

```bash
export ADMIN_USERNAME="admin"      # default
export ADMIN_PASSWORD="admin"      # default
export SECRET_KEY="your-secret"    # default: dev-secret-key-change-in-production
```

**Development (no env vars set):**
- Username: `admin`
- Password: `admin`

**Production (recommended):**
```bash
export ADMIN_USERNAME="your-admin-user"
export ADMIN_PASSWORD="secure-random-password-here"
export SECRET_KEY="secure-random-key-for-flask"
```

## Security Notes

- **No password hashing** — Credentials are plain text environment variables. Not suitable for multi-user systems.
- **Single admin account** — No user management, roles, or permissions.
- **Session stored in cookies** — All session data is client-side, encrypted with `SECRET_KEY`.
- **No database** — No persistent storage, no audit log of logins.

For production with multiple users, consider:
- Hashing passwords with `werkzeug.security`
- Storing credentials in a database (PostgreSQL)
- Using OAuth/SAML for enterprise authentication

## Session Lifetime

- **Browser close** → Session expires
- **Manual logout** → Session destroyed
- **No timeout** → Session persists indefinitely (until browser close)

To add timeout, modify the decorator:

```python
from datetime import datetime, timedelta

if 'admin' not in session or \
   datetime.now() > session.get('expires_at', datetime.now()):
    # Session expired or not authenticated
    return redirect(url_for('login'))

# Extend session on each request
session['expires_at'] = datetime.now() + timedelta(hours=2)
```
