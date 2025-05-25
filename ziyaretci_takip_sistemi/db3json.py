from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.String(20))  # Telefon alanı
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    visit_date = db.Column(db.Date) 

def export_visitors_to_json():
    with app.app_context():
        visitors = Visitor.query.all()
        data = []
        for visitor in visitors:
            data.append({
                'id': visitor.id,
                'name': visitor.name,
                'email': visitor.email,
                'tel': visitor.tel,
                'registered_on': visitor.registered_on.isoformat() if visitor.registered_on else None,
                'visit_date': visitor.visit_date.isoformat() if visitor.visit_date else None
            })
        
        with open('ziyaretci.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Ziyaretçiler başarıyla ziyaretci.json dosyasına kaydedildi!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Veritabanı ve tablolar oluşturulur, opsiyonel
        export_visitors_to_json()
