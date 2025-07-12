# Skill Swap Application

## 📁 Project Structure

Odoo-Hackathon-Team-IBEX-Coders/
├── static/ # Static assets
│ ├── css/style.css # Main stylesheet
│ └── js/main.js # Client-side scripts
│
├── templates/ # Jinja2 templates (17 files)
│ ├── auth/ # Authentication templates
│ │ ├── login.html
│ │ └── register.html
│ ├── skills/ # Skill management
│ │ ├── browse.html
│ │ └── manage.html
│ ├── base.html # Base template
│ └── index.html # Homepage
│
├── app.py # Flask application entry
├── forms.py # WTForm definitions
├── models.py # SQLAlchemy models
├── requirements.txt # Dependencies
└── README.md # This file




## 📦 Dependencies
```python
 requirements.txt
flask>=3.1.1                # Web framework
flask-sqlalchemy>=3.1.1     # ORM extension
flask-login>=0.6.3          # Authentication
flask-wtf>=1.2.2            # Form handling
psycopg2-binary>=2.9.10     # PostgreSQL adapter
email-validator>=2.2.0      # Email validation
gunicorn>=23.0.0            # Production server


Setup & Execution
Install dependencies:

bash
pip install -r requirements.txt
Configure environment:

bash
export FLASK_APP=app.py
export FLASK_ENV=development
Database setup:

bash
flask init-db
Run the application:

bash
python3 app.py
# Access at http://localhost:5000
🔄 Workflow
User Journey:

Register → Log in → Add skills → Browse swaps → Connect

Core Features:

Skill matching algorithm

Request/approval system

User rating mechanism

Admin Commands:

bash
flask seed-db       # Populate test data
flask clear-swaps   # Reset all exchanges
