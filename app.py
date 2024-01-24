from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory, current_app, abort, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)

# Load configuration from config.json
with open('config.json') as config_file:
     app.config.update(json.load(config_file))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=True)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    uploads = db.relationship('Upload', backref='user', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def is_password_hashed(password):
    return password.startswith('pbkdf2:sha256:')

def create_default_admin_user():
    admin_username = app.config['DEFAULT_ADMIN_USERNAME']
    admin_password = app.config['DEFAULT_ADMIN_PASSWORD']

    existing_user = User.query.filter_by(username=admin_username).first()
    if not existing_user:
        new_admin = User(username=admin_username, password=generate_password_hash(admin_password, method='pbkdf2:sha256'), is_admin=True)
        db.session.add(new_admin)
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            session.permanent = True  # make the session permanent
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    enable_public_registration = app.config.get('ENABLE_PUBLIC_REGISTRATION', False)
    return render_template('login.html', enable_public_registration=enable_public_registration)

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    # Verify the old password
    if not check_password_hash(current_user.password, old_password):
        flash('Current password is incorrect.')
        return redirect(url_for('dashboard'))

    # Update the user's password
    current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    db.session.commit()
    flash('Password changed successfully.')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    is_admin = current_user.is_admin
    users = User.query.all() if is_admin else None
    return render_template('dashboard.html', 
                           name=current_user.username, 
                           users=users, 
                           is_admin=is_admin, 
                           admin_username=current_app.config['DEFAULT_ADMIN_USERNAME'])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        file_url = url_for('uploaded_file', filename=filename, _external=True)

        expiry_option = request.form.get('expiry_time')
        expiry_time = None
        if expiry_option == 'burnable':
            expiry_time = None  # don't expire until first access
        else:
            expiry_time = datetime.utcnow() + timedelta(minutes=int(expiry_option))

        # Create a new upload record associated with the current user
        new_upload = Upload(filename=filename, user_id=current_user.id, expiry_time=expiry_time)
        db.session.add(new_upload)
        db.session.commit()

        flash(f'File uploaded successfully: <a href="{file_url}">{filename}</a>', 'success')
        return redirect(url_for('index'))
    
@app.route('/<filename>')
def uploaded_file(filename):
    upload = Upload.query.filter_by(filename=filename).first_or_404()
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if upload.expiry_time is None:
        upload.expiry_time = datetime.utcnow()  # expire now
        db.session.commit()
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    elif datetime.utcnow() > upload.expiry_time:
        db.session.delete(upload)
        db.session.commit()
        if os.path.exists(filepath):
            os.remove(filepath)  # delete the file from the filesystem
        abort(404)  # file has expired
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully.')
    else:
        flash('Invalid username or password.')
    return redirect(url_for('dashboard'))

@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    username = request.form.get('username')
    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully.')
        else:
            flash('User not found.')
    else:
        flash('Invalid username.')
    return redirect(url_for('dashboard'))

@app.route('/toggle_admin', methods=['POST'])
@login_required
def toggle_admin():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    if user:
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(f"Admin status toggled for {user.username}.")
    else:
        flash("User not found.")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
        create_default_admin_user()  # Create the default admin user
    app.run(host='0.0.0.0', port=8888, debug=True)