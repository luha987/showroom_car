from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merk = db.Column(db.String(100))
    model = db.Column(db.String(100))
    tahun = db.Column(db.Integer)
    harga_dasar = db.Column(db.Float)
    jumlah_pinjaman = db.Column(db.Float, nullable=True)
    suku_bunga = db.Column(db.Float, nullable=True)  # persen per tahun
    services = db.relationship('Service', backref='car', lazy=True)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    tanggal = db.Column(db.Date)
    deskripsi = db.Column(db.String(255))
    biaya = db.Column(db.Float)
