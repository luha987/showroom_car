from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for

from forms import CarForm, ServiceForm
from models import Car, Service, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///showroom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.route('/')
def index():
    cars = Car.query.all()
    return render_template('index.html', cars=cars)

@app.route('/add', methods=['GET', 'POST'])
def add_car():
    form = CarForm()
    if form.validate_on_submit():
        car = Car(
            merk=form.merk.data,
            model=form.model.data,
            tahun=form.tahun.data,
            harga_dasar=form.harga_dasar.data,
            jumlah_pinjaman=form.jumlah_pinjaman.data,
            suku_bunga=form.suku_bunga.data
        )
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_car.html', form=form)

@app.route('/mobil/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    hpp = hitung_hpp(car)
    return render_template('car_detail.html', car=car, hpp=hpp)

@app.route('/car/<int:car_id>/add_service', methods=['GET', 'POST'])
def add_service(car_id):
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            car_id=car_id,
            tanggal=form.tanggal.data,
            deskripsi=form.deskripsi.data,
            biaya=form.biaya.data
        )
        db.session.add(service)
        db.session.commit()
        return redirect(url_for('car_detail', car_id=car_id))
    return render_template('add_service.html', form=form)

@app.route('/delete/<int:car_id>')
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    form = CarForm(obj=car)
    if form.validate_on_submit():
        form.populate_obj(car)
        db.session.commit()
        return redirect(url_for('car_detail', car_id=car.id))
    return render_template('add_car.html', form=form)

def hitung_hpp(car):
    # Pastikan ada nilai pinjaman dan suku bunga
    if car.jumlah_pinjaman and car.suku_bunga:
        try:
            hpp_dasar = car.harga_dasar / (car.jumlah_pinjaman + car.suku_bunga)
        except ZeroDivisionError:
            hpp_dasar = car.harga_dasar
    else:
        hpp_dasar = car.harga_dasar

    # Hitung total biaya service
    total_service = sum(service.biaya for service in car.services)

    return hpp_dasar + total_service

if __name__ == '__main__':
    app.run(debug=True)
