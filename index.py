from flask import Flask, request
from flask_moment import Moment
from datetime import datetime


app = Flask(__name__)
moment = Moment(app)

@app.errorhandler(404)
def page_not_found(error):
    return 'page not found', 404


if __name__ == '__main__':
    app.run(debug=True)


