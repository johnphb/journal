from flask import Blueprint, render_template, redirect, url_for, send_file
from .models import User, Entries



blueprint = Blueprint('simple_pages', __name__)


@blueprint.route('/')
def index():
  return redirect(url_for("simple_pages.login"))

@blueprint.route("/login", methods=['GET', 'POST'])
def login():
  return render_template("login.html")

@blueprint.route("/calendar", methods=['GET', 'POST'])
def calendar():
  all_entries = Entries.query.all()
  return render_template("calendar.html", entries=all_entries)

@blueprint.route("/entry", methods=['GET', 'POST'])
def entry():
  all_entries = Entries.query.all()
  return render_template("entry.html", entries=all_entries)