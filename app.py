from dotenv import load_dotenv
import os

from flask import Flask, render_template, redirect, request, url_for, make_response, session, flash
from flask_session import Session
from functools import wraps
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import sqlite3

from models import db, User, Poll, Option, Vote 
from utils import get_color


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure application
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', "sqlite:///polls.db")


# Initialise the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()


def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("You need to log in first", "info")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    
    return decorated_function


@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in and handle login form submissions."""

    # Forget any user id
    session.clear()
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required", "error")
            return redirect(url_for("login"))

        try:

            user = User.query.filter_by(username=username).first()

            if user is None:
                print("user")
                flash("That username does not exist, please try again.")
                return render_template('login.html') 

            if not check_password_hash(user.hashed_password, password):
                print("password")
                flash('Password incorrect, please try again.')
                return render_template('login.html') 
            
            session["user_id"] = user.id
            return redirect(url_for("index"))
        
        except NoResultFound:
            flash("Invalid username and/or password", "warning")
            return redirect(url_for("login"))

    return render_template("login.html")



@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username:
            flash("Must provide username", "warning")
            return redirect(url_for("register"))
        
        if not password or not confirm_password:
            flash("Must provide both password fields", "warning")
            return redirect(url_for("register"))
        
        if password != confirm_password:
            flash("Passwords do not match", "warning")
            return redirect(url_for("register"))
        
        hashed_password = generate_password_hash(password)

        try:
            new_user = User(username=username, hashed_password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            flash("User registered successfully!", "success")
            return redirect(url_for("login"))
        
        except IntegrityError:
        # Roll back the transaction if an IntegrityError occurs
            db.session.rollback()
            flash("This username already exist", "error")
            return redirect(url_for("register"))
        
        except Exception as e:
            # Rollback the session and show a generic error message
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("register"))

    return render_template('register.html')


@app.route("/create_poll", methods=["GET", "POST"])
@login_required
def create_poll():
    """Create a new poll."""
    if request.method == "POST":

        user_id = session.get("user_id")
        creator = User.query.get(user_id)

        if not creator:
            flash("Invalid user. Please log in again.", "danger")
            return redirect(url_for('login'))
        
        question = request.form.get("title")
        
        options = []
        for key, value in request.form.items():
            if key.startswith("option_") and value.strip():
                options.append(value.strip())

        if not options or len(options) < 2:
            flash("Please provide at least two options.", "info")
            return redirect(url_for("create_poll"))
        
        unique_id = secrets.token_urlsafe(8)
        new_poll = Poll(question=question, unique_id=unique_id, creator_id=creator.id)
        db.session.add(new_poll)
        db.session.commit()

        for option_text in options:
            new_option = Option(text=option_text, poll_id=new_poll.id)
            db.session.add(new_option)
        db.session.commit()
        
        flash("Poll created successfully!", "success")
        return redirect(url_for('view_poll', unique_id=unique_id))

    return render_template("create_poll.html")


@app.route("/view_poll/<unique_id>", methods=["GET", "POST"])
def view_poll(unique_id):
    """View a specific poll and handle voting."""
    poll = Poll.query.filter_by(unique_id=unique_id).first_or_404()
    options = Option.query.filter_by(poll_id=poll.id).all()
    total_votes = sum(option.vote_count for option in options)
    
    # Calculate maximum vote count
    max_votes = max((option.vote_count for option in options), default=0)
    
    # Get user's IP address
    user_ip = request.remote_addr
    
    if request.method == "POST":
        option_id = request.form.get("option_id")
        if option_id:
            # Check if this IP address has already voted
            existing_vote = Vote.query.join(Option).filter(
                Option.poll_id == poll.id, Vote.ip_address == user_ip
            ).first()
            if not existing_vote:
                vote = Vote(option_id=option_id, ip_address=user_ip)
                db.session.add(vote)
                db.session.commit()
                flash("Vote recorded", "success")
            else:
                flash("You have already voted", "info")
            return redirect(url_for("view_poll", unique_id=unique_id))
        
    return render_template("view_poll.html", poll=poll, options=options, total_votes=total_votes, max_votes=max_votes, get_color=get_color)


@app.route('/view_all_polls')
@login_required
def view_all_polls():
    """View all polls created by the logged-in user."""
    user_id = session.get("user_id")
    polls = Poll.query.filter_by(creator_id=user_id).all()  # Get only polls created by the logged-in user

    return render_template('view_all_polls.html', polls=polls)


@app.route("/logout")
def logout():
    """Log user out and clear session."""

    # Forget any user_id
    session.clear()

    # Redirect user to homepage
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)