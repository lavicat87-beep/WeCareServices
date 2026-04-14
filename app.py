from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
# Use PostgreSQL for professional business data
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ndis.db')
db = SQLAlchemy(app, model_class=Base)

class Referral(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    client_name: Mapped[str] = mapped_column(nullable=False)
    contact_number: Mapped[str] = mapped_column(nullable=False)
    service_needed: Mapped[str] = mapped_column(nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/referral', methods=['POST', 'GET'])
def referral():
    if request.method == 'POST':
        # Logic to save referral to database
        return redirect('/')
    return render_template('referral.html')