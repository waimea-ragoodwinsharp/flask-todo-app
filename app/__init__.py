#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================



#-----------------------------------------------------------
# home page
#-----------------------------------------------------------
@app.get("/")
def show_all_chores():
    with connect_db() as db:
        sql = """
            SELECT id, name, priority, complete
            FROM chores
            ORDER BY priority ASC
        """
        params = ()
        chores = db.execute(sql, params).fetchall()

        return render_template("pages/chore_list.jinja", chores=chores)

#-----------------------------------------------------------
# New Creature form
#-----------------------------------------------------------
@app.get("/chore/new")
def show_chore_form():
    return render_template("pages/chore_new.jinja")

#-----------------------------------------------------------
# Help page - Show some help
#-----------------------------------------------------------
@app.get("/help")
def show_help():

    flash("Flash test message")
    flash("Flash test message with a longer bit of text")
    flash("Success test message", "success")
    flash("Error test message", "error")

    return render_template("pages/help.jinja")

#-----------------------------------------------------------
# Handel the creature form
#-----------------------------------------------------------
@app.post("/chore/new")
def process_chore_form():
    #get form data
    name = request.form.get("name", "unknown").strip()
    priority = request.form.get("priotiry", "unknown").strip() #defult value if no species
    

    #connect to the DB
    with connect_db() as db:
        sql = """
            INSERT INTO chores ( priority, name )
            VALUES (?, ?)
        """
        params = (priority, name)

        #run qeury
        db.execute(sql, params)

        flash(f"Chore {name} added successfully")

        #done, return to list
        return redirect("/")

#-----------------------------------------------------------
# uncheck the box 
#-----------------------------------------------------------
@app.get("/chore/<int:id>/complete")
def show_box_unticked(id):
    with connect_db() as db:
        sql = """
            UPDATE chores SET complete = 1 WHERE id = ?
        """
        params = (id,)
        db.execute(sql, params)

        return redirect("/")

#-----------------------------------------------------------
# check the box 
#-----------------------------------------------------------
@app.get("/chore/<int:id>/incomplete")
def show_box_ticked(id):
    with connect_db() as db:
        sql = """
            UPDATE chores SET complete = 0 WHERE id = ?
        """
        params = (id,)
        db.execute(sql, params)

        return redirect("/")

#-----------------------------------------------------------
# chore deletion
#-----------------------------------------------------------
@app.get("/chore/<int:id>/delete")
def delete_a_chores(id):
    with connect_db() as db:
        
        sql = """
            DELETE FROM chores
            WHERE id=?
        """
        params = (id,)
        db.execute(sql, params)


        flash("chore deleted", "success")

        return redirect("/")
#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

