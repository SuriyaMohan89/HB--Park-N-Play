""" Locate Children's park and rate"""

from jinja2 import StrictUndefined

from flask import(Flask,render_template, redirect, request, flash, session, url_for)
from flask_debugtoolbar import DebugToolbarExtension

from model_db import User,Park,Rating,Favorite, connect_to_db,db
from sqlalchemy import update


app = Flask(__name__)
