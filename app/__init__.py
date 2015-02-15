from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy

DATABASE = 'database.db'

# create app
app = Flask(__name__)

# setup db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ip.db'
db = SQLAlchemy(app)

# register blueprints
from app.bulletin_board.views import bulletin_board
app.register_blueprint(bulletin_board)


# Run server
if __name__ == '__main__':
    app.run()
