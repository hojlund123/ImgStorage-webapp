# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from cryptography.fernet import Fernet
import os
import imghdr

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(16))

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize the encryption key
key = Fernet.generate_key()
fernet = Fernet(key)

# Define the User class for user authentication
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Define a dictionary of users with their username and password
users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

# Define the route for the login page
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(id=username)
            login_user(user)
            return redirect(url_for('upload'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

# Define the route for the logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Define the allowed file types for upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

# Define the route for the upload page
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Encrypt the file name before saving
            filename = fernet.encrypt(file.filename.encode()).decode()
            file.save(os.path.join('uploads', filename))
            flash('File uploaded successfully')
            return redirect(url_for('upload'))
        else:
            flash('File type not allowed')
    return render_template('upload.html')

# Define the route for the homepage
@app.route('/home')
@login_required
def home():
    # Get all uploaded image files and their encrypted names
    files = os.listdir('uploads')
    image_files = [fernet.decrypt(file.encode()).decode() for file in files if imghdr.what(os.path.join('uploads', file))]
    return render_template('home.html', files=image_files)

# Define the route for deleting an uploaded file
@app.route('/delete/<filename>')
@login_required
def delete(filename):
    # Delete the file with the given filename
    os.remove(os.path.join('uploads', fernet.encrypt(filename.encode()).decode()))
    flash('File deleted successfully')
    return redirect(url_for('home'))

# Define the required user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Run the Flask application
if __name__ == '__main__':
    app
