
from flask import Flask, request, render_template
from create_db import Note
from sqlalchemy import create_engine
import string
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)


@app.route('/')
def index():
    return "Index"


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
        notes[note.note_title] = note.note_body

        text = set('wefwef, qwdwqd, !1fwef, 31dqw\ fqwd'.lower().translate(''.maketrans('', '', string.punctuation)).split())
    print(len(text))
    print(text)
    #note = sorted(note, key=lambda x: )
    return render_template(
        'all_notes.html', **locals()
    )


if __name__ == '__main__':
    app.run()
