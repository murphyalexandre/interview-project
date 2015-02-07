from flask import Flask

from app.bulletin_board import bulletin_board

# create app
app = Flask(__name__)

# register blueprints
app.register_blueprint(bulletin_board)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
