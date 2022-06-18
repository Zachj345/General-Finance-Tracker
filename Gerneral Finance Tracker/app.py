from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super secret'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


'''DATABASES'''


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(111), unique=True, nullable=False)
    password = db.Column(db.String(111), nullable=False)
    expenses = db.relationship('Expense', cascade='all, delete, delete-orphan',
                               backref='user', lazy=True, passive_deletes=True)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(60), nullable=False)
    note = db.Column(db.String(111))
    date = db.Column(db.DateTime(timezone=True), default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)


def get_total(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('no user to calculate subtotal', category='error')
    else:
        return sum([i.amount for i in user.expenses])


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    expenses = [i for i in Expense.query.all() if i in current_user.expenses]
    amount_sort = sorted(expenses, key=lambda n: n.amount)
    category_sort = sorted(expenses, key=lambda n: n.category)
    date_sort = sorted(expenses, key=lambda n: n.date)

    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        note = request.form.get('note')
        if not note:
            note = ''
        if not amount:
            flash('Please enter the amount payed in dollars', category='error')
        else:
            new_expense = Expense(amount=amount, category=category,
                                  note=note, date=date.today(), user_id=current_user.id)
            db.session.add(new_expense)
            db.session.commit()
            flash('Successfully added!', category='success')
            return redirect(url_for('home'))

    return render_template('home.html', user=current_user, expenses=expenses,
                           amount_sort=amount_sort, category_sort=category_sort, date_sort=date_sort,
                           get_total=get_total)


@app.route('/remove/<id>', methods=['GET', 'POST'])
@login_required
def remove_expense(id):
    expense = Expense.query.filter_by(id=id).first()
    if not expense:
        flash('This expense does not exist', category='error')
    else:
        db.session.delete(expense)
        db.session.commit()

    return jsonify({'success': 'facts'})


'''AUTHENTICATION'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash("Passwords do not match, please try again.", category='error')
        else:
            flash(
                'Username not in database, please check your spelling and try again', category='error')
    return render_template('login.html', user=current_user)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username must not be taken!', category='error')

        elif len(username) < 4:
            flash('Username must be longer than 4 characters.', category='error')
        elif len(password1) < 4:
            flash('Password must be longer than 4 characters', category='error')
        elif password1 != password2:
            flash('Passwords must match!', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('home'))

    return render_template('sign-up.html', user=current_user)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
