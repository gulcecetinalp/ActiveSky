from flask import Blueprint, render_template , request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash 
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)
# auth blue printini tanımladık, initde de app e ekleyeceğiz


#Kullanıcı /login URL'sine gittiğinde, bu fonksiyon çalışacak.
#methods=['GET', 'POST'] ifadesi, bu route'un hem GET hem de POST isteğini kabul edebileceğini söylüyor
#GET	Sayfayı görüntülemek için kullanılır. (Tarayıcıdan login sayfasını açmak gibi)
#POST	Formdan veri göndermek için kullanılır. (Kullanıcı email ve şifre gönderdiğinde)
@auth.route('/giriş_yap', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        şifre = request.form.get('şifre') #emin değiliz

        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.şifre, şifre):
                flash('Başarıyla giriş yapıldı.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.mainPage'))
                # viewsdeki bu metodu çağırıyor o da base.html ye gönderiyor, değiştirilebilir
            else:
                flash('Hatalı şifre girildi', category='error')
        else:
            flash('Bu email sistemde bulunmamaktadır.', category='error')

    return render_template("giriş_yap.html")

@auth.route('/kayıt_ol', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        kullanıcı_adı = request.form.get('kullanıcı_adı')
        şifre = request.form.get('şifre')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Bu email sistemde bulunmaktadır.', category='error')
        elif len(email) < 4:
            flash('Email en az 4 karakter olmalıdır.', category='error')
        elif len(kullanıcı_adı) < 2:
            flash('Kullanıcı adı en az 2 karakter olmalıdır.', category='error')
        elif len(şifre) < 7:
            flash('Şifre en az 7 karakter olmalıdır.', category='error')
        else:
            new_user = User(email=email, kullanıcı_adı=kullanıcı_adı, şifre=generate_password_hash(şifre, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Hesap başarıyla oluşturuldu.', category='success')
            return redirect(url_for('views.mainPage'))
            #yukarıdaki gibi değiştirlebilir

    return render_template("kayıt_ol.html")