import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

app = Flask(__name__)

# 1. Get the URL from Render's Environment
uri = os.environ.get('DATABASE_URL', 'sqlite:///ndis.db')

# 2. Update the prefix to use pg8000
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql+pg8000://", 1)
elif uri.startswith("postgresql://"):
    uri = uri.replace("postgresql://", "postgresql+pg8000://", 1)

# Note: We removed the 'sslmode' logic here because pg8000 doesn't support it.
app.config['SQLALCHEMY_DATABASE_URI'] = uri
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