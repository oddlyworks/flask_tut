from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint("views", __name__)  # flask command to 'initialize' views

"""Create and pass info to home.html"""


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is blank!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added", category="success")

    return render_template("home.html", user=current_user)  # return actual webage


"""Delete note logic, don't follow for sure."""


@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)  # not sure where this is coming from
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:  # does the noteId exist?
        if note.user_id == current_user.id:  # does note belong to user?
            db.session.delete(note)  # if so delete
            db.session.commit()  # push commit of deleted note
            return jsonify({})

    return jsonify({})
