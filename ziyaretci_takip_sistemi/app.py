from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite kullanılıyor
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.String(20))  # Telefon alanı
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    visit_date = db.Column(db.Date) 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
def base():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if not name or not email or not password or not confirm:
            flash("Tüm alanları doldurunuz!", "danger")
        elif password != confirm:
            flash("Şifreler uyuşmuyor!", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Bu e-posta zaten kayıtlı.", "danger")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(name=name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash("Geçersiz e-posta veya şifre.", "danger")
        redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    visitor_list = Visitor.query.all()
    total_visitors = Visitor.query.count()  # Toplam ziyaretçi sayısı
    return render_template('dashboard.html', visitors=visitor_list, total_visitors=total_visitors)



@app.route('/visitor/delete/<int:visitor_id>', methods=['POST'])
@login_required
def visitor_delete(visitor_id):
    visitor = Visitor.query.get_or_404(visitor_id)
    db.session.delete(visitor)
    db.session.commit()
    flash('Ziyaretçi başarıyla silindi.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/visitor_update/<int:visitor_id>', methods=['GET', 'POST'])
@login_required
def visitor_update(visitor_id):
    visitor = Visitor.query.get_or_404(visitor_id)

    if request.method == 'POST':
        visitor.name = request.form.get('name')
        visitor.email = request.form.get('email')
        visitor.tel = request.form.get('tel')
        date_str = request.form.get('date')

        try:
            visitor.visit_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Geçersiz tarih formatı.", "danger")
            return redirect(url_for('visitor_update', visitor_id=visitor_id))

        db.session.commit()
        flash("Ziyaretçi bilgileri güncellendi.", "success")
        return redirect(url_for('dashboard'))

    return render_template('visitor_update.html', visitor=visitor)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Başarıyla çıkış yapıldı.", "info")
    return redirect(url_for('login'))

@app.route('/visitor_list')
@login_required
def visitor_list():
    visitor_list=Visitor.query.all()
    return render_template('visitor_list.html',visitors=visitor_list)

@app.route('/visitor_add', methods=['GET', 'POST'])
@login_required
def visitor_add():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        tel = request.form.get('tel')
        date_str = request.form.get('date')

        if not name or not email or not tel or not date_str:
            flash("Lütfen tüm alanları doldurunuz.", "danger")
            return redirect(url_for('visitor_add'))

        try:
            visit_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Geçersiz tarih formatı.", "danger")
            return redirect(url_for('visitor_add'))

        new_visitor = Visitor(name=name, email=email, tel=tel, visit_date=visit_date, registered_on=datetime.utcnow())
        db.session.add(new_visitor)
        db.session.commit()

        flash("Ziyaretçi başarıyla kaydedildi.", "success")
        return redirect(url_for('visitor_list'))

    return render_template('visitor_add.html')


@app.route('/users')
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/user_update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_update(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        new_password = request.form.get('password')

        if new_password:
            user.password = generate_password_hash(new_password)

        db.session.commit()
        flash("Kullanıcı başarıyla güncellendi.", "success")
        return redirect(url_for('users'))

    return render_template('user_update.html', user=user)

@app.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Kullanıcı başarıyla silindi.', 'success')
    except:
        db.session.rollback()
        flash('Kullanıcı silinirken bir hata oluştu.', 'danger')
    return redirect(url_for('users'))  # users sayfasına yönlendir


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
