import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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

# pg8000 doesn't support sslmode in the URL; pass ssl via connect_args instead
app.config['SQLALCHEMY_DATABASE_URI'] = uri
if uri.startswith("postgresql+pg8000://"):
    import ssl
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'connect_args': {'ssl_context': ssl_context}}
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
        referral = Referral(
            client_name=request.form['client_name'],
            contact_number=request.form['contact_number'],
            service_needed=request.form['service_needed']
        )
        db.session.add(referral)
        db.session.commit()
        return redirect('/')
    return render_template('referral.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))