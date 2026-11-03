# Personal Notes API

## Project Description

Personal Notes API is a Flask backend for a personal notes application.

Users can create accounts, log in, and manage their personal notes. Each user should only be able to access, update, and delete their own notes.

This project uses session-based authentication and is developed by a five-member Moringa group.

The provided React frontend in `client-with-sessions` handles signup and login. Notes endpoints can be tested using Postman or curl.

## Technologies

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* Flask-Migrate
* Flask-Bcrypt
* Flask Sessions
* React
* Git and GitHub

## Project Structure

```text
project-root/
├── client-with-jwt/
├── client-with-sessions/
├── server/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── seed.py
│   ├── requirements.txt
│   └── routes/
│       ├── security.py
│       └── notes.py
├── README.md
├── TESTING.md
└── .gitignore

```

## Backend Setup

1. Clone the repository:

```bash
git clone https://github.com/ManwaMocha/flask-c10-summative-lab-sessions-and-jwt-clients.git
```

2. Navigate into the server directory:

```bash
cd flask-c10-summative-lab-sessions-and-jwt-clients
cd server
```

3. Create a virtual environment:

```bash
python3 -m venv venv
```

4. Activate the virtual environment:

```bash
source venv/bin/activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```
## Database Setup

After installing dependencies, run:

```bash
python -m flask --app app db upgrade
```

This creates the database tables.

## Seed Sample Data

To add sample users and notes, run:

```bash
python seed.py
```

Demo accounts:

| Username | Password |
|---|---|
| john | password123 |
| mary | password456 |

## Running the Backend

From inside the `server` directory, run:

```bash
python -m flask --app app run --port 5555 --debug
```

The backend will be available at:

`http://127.0.0.1:5555`

## Authentication

The application uses session-based authentication.

Users must log in before accessing protected notes functionality. Each user should only be able to manage their own notes.

## Testing

API endpoints can be tested using Postman or curl.

See `TESTING.md` for the manual testing instructions and expected API behaviour.
## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | /signup | Register a user |
| POST | /login | Log in |
| GET | /check_session | Check login session |
| DELETE | /logout | Log out |

### Notes

All notes endpoints require login.

| Method | Endpoint | Description |
|---|---|---|
| GET | /notes | Get notes |
| GET | /notes/<int:note_id> | Get one note |
| POST | /notes | Create a note |
| PATCH | /notes/<int:note_id> | Update a note |
| DELETE | /notes/<int:note_id> | Delete a note |

### Pagination

Use page and per_page to control results.

Example:

```text
GET /notes?page=1&per_page=10
```
## Contributors

This project was developed collaboratively by a five-member Moringa School group.
