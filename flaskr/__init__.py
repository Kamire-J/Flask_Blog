import os
from flask import Flask 


# Function that creates the flask app

def create_app(test_config=None):
    # Create and configu the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev', 
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),

    )

    if test_config is None:
        # Instance config is loaded if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if it has been passed
        app.config.from_mapping(test_config)

    # check to ensure the instance folder is present
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page to test app
    @app.route('/hello')
    def hello():
        return 'Hello Jack!'
    

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app