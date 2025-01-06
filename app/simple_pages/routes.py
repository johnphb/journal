from flask import Blueprint, render_template, redirect, url_for, send_file, request
from .models import User, Entries
from app.extensions.database import db
from datetime import datetime


blueprint = Blueprint('simple_pages', __name__)


@blueprint.route('/')
def index():
  return redirect(url_for("simple_pages.login"))

@blueprint.route("/login", methods=['GET', 'POST'])
def login():
  return render_template("login.html")

@blueprint.route("/calendar", methods=['GET', 'POST'])
def calendar():
  # Get User
  user_id = 1

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

  return render_template("calendar.html", entries=all_entries)

@blueprint.route("/entry/<int:entry_id>", methods=['GET', 'POST'])
def entry(entry_id):

  # Get Entries Table from DB
  entry = Entries.query.get(entry_id)
  print(entry)
  return render_template("entry.html", entry=entry)

@blueprint.route("/entry/<int:entry_id>/edit", methods=['GET', 'POST'])
def edit_entry(entry_id):
  entry = Entries.query.get(entry_id)
  date_formatted = entry.date.strftime('%d.%m.%Y')

  if request.method == 'POST':
      # Update the entry with the form data
      entry.title = request.form['title']
      entry.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date() # Formating to py datetime object
      entry.content = request.form['content']

      # Commit the changes to the database
      db.session.commit()
      return redirect(url_for('simple_pages.entry', entry_id=entry.id))

  return render_template("edit_entry.html", entry=entry, date_formatted=date_formatted)

@blueprint.route("/new_entry", methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':

      # Create a new entry - get form data 
      new_entry = Entries(
        user_id=1, 
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
    return render_template("new_entry.html", current_date=current_date)