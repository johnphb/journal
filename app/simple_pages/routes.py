from flask import Blueprint, render_template, redirect, url_for, send_file, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Entries
from app.extensions.database import db
from datetime import datetime

from app.scripts.seed import seed_database


blueprint = Blueprint('simple_pages', __name__)

@blueprint.route('/run-seed')
def run_seed():
    return seed_database()


# ---------- Account Management ----------
@blueprint.route('/')
def index():
  return redirect(url_for("simple_pages.login"))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['uname']
        password = request.form['pword']

        # Check username already exists
        existing_user = User.query.filter_by(uname=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('simple_pages.register'))

        # Create new user
        new_user = User(uname=username, pword=password)

        # Add to DB
        db.session.add(new_user)
        db.session.commit()

        # redirect -> login
        flash('User created successfully!')
        return redirect(url_for('simple_pages.login'))

    return render_template('register.html', show_navbar=False)

@blueprint.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    # Get form data
    username = request.form['uname']
    password = request.form['pword']

    # Get User with that username from DB
    user = User.query.filter_by(uname=username).first()

    # If password correct -> login
    if user and user.pword == password:
        login_user(user)

        # redirect -> calendar
        flash('Logged in successfully.', 'success')
        return redirect(url_for('simple_pages.calendar'))

    flash('Invalid username or password.')

  return render_template("login.html", show_navbar=False)

@blueprint.route("/logout")
@login_required
def logout():
    # logout and redirect -> login
    logout_user()
    flash('You have been logged out.', 'info')

    return redirect(url_for('simple_pages.login'))

@blueprint.route("/account")
@login_required
def account():
    # get current user
    user = User.query.get(current_user.id)

    # count number of entries un db
    entry_count = Entries.query.filter_by(user_id=user.id).count()

    return render_template("account.html", user=user, entry_count=entry_count, show_navbar=True)

@blueprint.route("/account/edit", methods=['GET', 'POST'])
@login_required
def edit_account():
    if request.method == 'POST':
        # get form data
        new_username = request.form['uname']
        new_password = request.form['pword']

        # check if username exists
        if new_username != current_user.uname:
            existing_user = User.query.filter_by(uname=new_username).first()
            if existing_user:
                
                # refresh
                flash('Username already exists. Please choose a different one.', 'danger')
                return redirect(url_for('simple_pages.edit_account'))

        # Update user details
        current_user.uname = new_username
        if new_password:  # Only change pword if its new
            current_user.pword = new_password

        # sent to db and redirect -> account
        db.session.commit()
        flash('Account updated successfully!', 'success')
        return redirect(url_for('simple_pages.account'))

    return render_template("edit_account.html", user=current_user, show_navbar=True)



# ---------- App Pages ----------
@blueprint.route("/calendar", methods=['GET', 'POST'])
@login_required
def calendar():
  # Get User
  user_id = current_user.id

  # Get Entries Table from DB  - Only for User          - Sorted by Date (latest first)
  all_entries = Entries.query.filter_by(user_id=user_id).order_by(Entries.date.desc()).all()

  # Sending to DB
  if request.method == "POST":
    data = request.get_json() # Get json file from postman

    new_entry = Entries( 
      user_id=data["user_id"],
      date=datetime.strptime(data["date"], '%d.%m.%Y').date(), # Formating to py datetime object
      title=data["title"],
      content=data["content"]
    )
    try: # Sending to DB
      db.session.add(new_entry) 
      db.session.commit()
    except Exception as e:
      print(e)

  return render_template("calendar.html", entries=all_entries, show_navbar=True)

@blueprint.route("/entry/<int:entry_id>", methods=['GET', 'POST'])
@login_required
def entry(entry_id):

  # Get Entries Table from DB
  entry = Entries.query.get(entry_id)
  return render_template("entry.html", entry=entry, show_navbar=True)

@blueprint.route("/entry/<int:entry_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
  # Get Entry from DB
  entry = Entries.query.get(entry_id)

  if request.method == 'POST':
      # Update entry with form data
      entry.title = request.form['title']
      entry.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date() # Formatting to py datetime object
      entry.content = request.form['content']

      # Commit to DB
      db.session.commit()
      return redirect(url_for('simple_pages.entry', entry_id=entry.id))

  return render_template("edit_entry.html", entry=entry, show_navbar=True)

@blueprint.route("/new_entry", methods=['GET', 'POST'])
@login_required
def new_entry():
    if request.method == 'POST':

      # Create a new entry - get form data 
      new_entry = Entries(
        user_id=current_user.id, 
        title=request.form['title'], 
        date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(), # formatting to py datetime object
        content=request.form['content']
        )  

      # Add and commit to DB
      db.session.add(new_entry)
      db.session.commit()

      # Redirect to new entry page
      return redirect(url_for('simple_pages.entry', entry_id=new_entry.id))

    # Get the current date in DB format
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("new_entry.html", current_date=current_date, show_navbar=True)