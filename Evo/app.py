
from flask import Flask, request, render_template, redirect
from create_db import Note
from sqlalchemy import create_engine
import string
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('add_note.html')


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        engine = create_engine('sqlite:///notes.db', echo=True)
        # create a Session
        Session = sessionmaker(bind=engine)
        session = Session()

        note = Note(request.form['Title'], request.form['Body'])
        session.add(note)

        # commit the record database
        session.commit()
    return render_template('add_note.html')


@app.route('/notes')
def all_notes():
    engine = create_engine('sqlite:///notes.db', echo=True)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    notes = {}
    for note in session.query(Note):

        size_of_body = len(set(note.note_body.lower().translate(''.maketrans('', '', string.punctuation)).split()))
        notes[note.note_title] = [note.note_body, size_of_body]
    print(notes)
    notes = dict(sorted(notes.items(), key=lambda x: x[1][1], reverse=True))
    print(notes)

    return render_template(
        'all_notes.html', **locals()
    )


@app.route('/remove_note', methods=['GET', 'POST'])
def remove_note():
    if request.method == 'POST':
        engine = create_engine('sqlite:///notes.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        note = session.query(Note).filter_by(note_title=request.form['test']).first()
        session.delete(note)
        session.commit()
    return redirect('/notes')


if __name__ == '__main__':
    app.run()
