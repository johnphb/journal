from flask import Blueprint, render_template, redirect, url_for, send_file


blueprint = Blueprint('simple_pages', __name__)


@blueprint.route('/')
def index():
  return redirect(url_for("simple_pages.login"))

@blueprint.route("/login", methods=['GET', 'POST'])
def login():
  return render_template("login.html")

@blueprint.route("/calendar", methods=['GET', 'POST'])
def calendar():

  list = [
     ["Date1", "Title1", "Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1 Description1"], 
     ["Date2", "Title2", "Description1"], 
     ["Date3", "Title3", "Description1"]
     ]
  return render_template("calendar.html", list=list)

@blueprint.route("/entry", methods=['GET', 'POST'])
def entry():
   return render_template("entry.html")