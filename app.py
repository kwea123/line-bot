import os

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return os.environ['test']

if __name__ == '__main__':
   app.run()

