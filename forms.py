from flask_wtf import FlaskForm
from wtforms import (DateField, FloatField, IntegerField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired


class CarForm(FlaskForm):
    merk = StringField('Merk', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    tahun = IntegerField('Tahun', validators=[DataRequired()])
    harga_dasar = FloatField('Harga Dasar', validators=[DataRequired()])
    jumlah_pinjaman = FloatField('Jumlah Pinjaman')
    suku_bunga = FloatField('Suku Bunga (persen)')
    submit = SubmitField('Tambah Mobil')

class ServiceForm(FlaskForm):
    tanggal = DateField('Tanggal', validators=[DataRequired()])
    deskripsi = TextAreaField('Deskripsi', validators=[DataRequired()])
    biaya = FloatField('Biaya', validators=[DataRequired()])
    submit = SubmitField('Tambah Service')
