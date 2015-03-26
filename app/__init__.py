from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

DATABASE = 'database.db'

# create app
app = Flask(__name__)

bcrypt = Bcrypt(app)

# setup db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ip.db'
db = SQLAlchemy(app)

# setup login
app.secret_key = 'SOMEOMEOMEOMSD'
login_manager = LoginManager()
login_manager.init_app(app)

# register blueprints
from app.bulletin_board.views import bulletin_board
app.register_blueprint(bulletin_board)


# Run server
if __name__ == '__main__':
    app.run()
