
from flask import Flask

app = Flask(__name__)


@app.route('/blog/<int:postID>')
def hello_name(postID):
    return 'Blog Number {}'.format(postID)


@app.route('/rev/<float:revNo>')
def revision(revNo):
    return 'Revision Number {}'.format(revNo)


if __name__ == '__main__':
    app.run(debug=True)
