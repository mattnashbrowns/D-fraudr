import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'dfraudr.sqlite'),
    )
    
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
    
    return app