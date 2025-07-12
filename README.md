# Skill Swap Application<br>

## 📁 Project Structure<br>

Odoo-Hackathon-Team-IBEX-Coders/<br>
├── static/ # Static assets<br>
│ ├── css/style.css # Main stylesheet<br>
│ └── js/main.js # Client-side scripts<br>
│
├── templates/ # Jinja2 templates (17 files)<br>
│ ├── auth/ # Authentication templates<br>
│ │ ├── login.html<br>
│ │ └── register.html<br>
│ ├── skills/ # Skill management<br>
│ │ ├── browse.html<br>
│ │ └── manage.html<br>
│ ├── base.html # Base template<br>
│ └── index.html # Homepage<br>
│
├── app.py # Flask application entry<br>
├── forms.py # WTForm definitions<br>
├── models.py # SQLAlchemy models<br>
├── requirements.txt # Dependencies<br>
└── README.md # This file<br>




## 📦 Dependencies<br>
```python<br>
 requirements.txt<br>
flask>=3.1.1                # Web framework<br>
flask-sqlalchemy>=3.1.1     # ORM extension<br>
flask-login>=0.6.3          # Authentication<br>
flask-wtf>=1.2.2            # Form handling<br>
psycopg2-binary>=2.9.10     # PostgreSQL adapter<br>
email-validator>=2.2.0      # Email validation<br>
gunicorn>=23.0.0            # Production server<br>


Setup & Execution<br>
Install dependencies:<br>

bash<br>
pip install -r requirements.txt<br>
Configure environment:<br>

bash<br>
export FLASK_APP=app.py<br>
export FLASK_ENV=development<br>
Database setup:<br>

bash<br>
flask init-db<br>
Run the application:<br>

bash<br>
python3 app.py<br>
# Access at http://localhost:5000<br>
🔄 Workflow<br>
User Journey:<br>

Register → Log in → Add skills → Browse swaps → Connect<br>

Core Features:<br>

Skill matching algorithm
<br>
Request/approval system<br>

User rating mechanism<br>

Admin Commands:

bash
flask seed-db       # Populate test data
flask clear-swaps   # Reset all exchanges
