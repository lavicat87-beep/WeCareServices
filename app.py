from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
# Use PostgreSQL for professional business data
sqlalchemy_database_uri = os.environ.get('DATABASE_URL', 'sqlite:///ndis.db')
if sqlalchemy_database_uri.startswith('postgres://'):
    sqlalchemy_database_uri = sqlalchemy_database_uri.replace('postgres://', 'postgresql+pg8000://', 1)
elif sqlalchemy_database_uri.startswith('postgresql://'):
    sqlalchemy_database_uri = sqlalchemy_database_uri.replace('postgresql://', 'postgresql+pg8000://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))