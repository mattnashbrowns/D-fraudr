import os

from flask import Flask, g

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        # Load the instance config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
        
    # Create the instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Basic functionality page
    @app.route('/hello')
    def hello():
        return 'Look out, scammers!'
    
    from . import db
    db.init_app(app)
    
    from . import upload
    app.register_blueprint(upload.bp)
    app.add_url_rule('/upload', endpoint='upload_file')
    app.add_url_rule('/', endpoint='files'
    
    from . import analyze
    app.register_blueprint(analyze.bp)
    
    return app

    