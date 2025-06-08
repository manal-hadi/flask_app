from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for flash messages

db = SQLAlchemy(app)

#create a database model
class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

#Create the database
with app.app_context():
    db.create_all()

#create homepage
@app.route('/')
def index():
    users = user.query.all()
    return render_template('index.html', users=users)

#create a route to add a new user
@app.route('/add', methods = ['GET', 'POST'])
def add():
    name = request.form.get("name")
    email = request.form.get("email")
    if name and email:
        new_user = user(name=name, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Email already registered!', 'error')
    return redirect('/')

#create a route to delete a user
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = user.query.get_or_404(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)