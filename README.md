<h1 align="center">📌 Flask API Project – User & Todo Management</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.3-green" alt="Flask">
  <img src="https://img.shields.io/badge/Swagger-API%20Docs-orange" alt="Swagger">
  <img src="https://img.shields.io/badge/Database-SQLAlchemy-yellow" alt="Database">
</p>

---

<h2>🚀 Project Overview</h2>
<p>
This project is a <b>Flask-based REST API application</b> that demonstrates modern backend development practices with:
<ul>
  <li>User Authentication & Password Security (using <b>Bcrypt</b> with OOPs encapsulation)</li>
  <li>Todo Management system with relational mapping</li>
  <li>Fetching external data from <code>JSONPlaceholder</code> API and saving into local database</li>
  <li>Complete CRUD operations for both Users & Todos</li>
  <li>API Documentation powered by <b>Swagger UI</b></li>
</ul>
</p>

---

<h2>🛠️ Technologies Used</h2>
<table>
  <tr><td>Backend</td><td>Flask, Flask-RESTful, Blueprints</td></tr>
  <tr><td>Database</td><td>SQLAlchemy (SQLite/MySQL/Postgres ready)</td></tr>
  <tr><td>Security</td><td>Flask-Bcrypt for password hashing</td></tr>
  <tr><td>Documentation</td><td>Swagger UI</td></tr>
  <tr><td>Concepts</td><td>OOPs Principles (Encapsulation, Methods in Classes, Reusable Models)</td></tr>
</table>

---

<h2>📂 Project Structure</h2>

<pre>
project/
│── app/
│   ├── __init__.py        # App Factory
│   ├── models.py          # User & Todo Models (OOPs applied)
│   ├── routes/
│   │   ├── api.py         # Todo APIs (CRUD + External API)
│   │   └── user.py        # User Registration & Authentication
│   ├── docs.py            # Swagger Documentation
│
│── migrations/            # Database migrations
│── requirements.txt       # Dependencies
│── run.py                 # Entry point
</pre>

---

<h2>📌 API Features</h2>

<ul>
  <li><b>User APIs:</b> Register, Login, Password Security with Hashing</li>
  <li><b>Todo APIs:</b> Create, Read, Update, Delete Todos</li>
  <li><b>External Data:</b> Fetch todos from JSONPlaceholder and save into DB</li>
  <li><b>Swagger:</b> Interactive API docs at <code>/swagger</code></li>
</ul>

---

<h2>🔑 Example API Endpoints</h2>

```http
GET  /api/todo            # Fetch all todos (from DB)
POST /api/todo/fetch      # Fetch & Save from JSONPlaceholder
POST /api/users/register  # Create a new user
POST /api/users/login     # Authenticate user
