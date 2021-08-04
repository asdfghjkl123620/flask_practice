import os
from flask import Flask,session
from datetime import timedelta
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    #創造並且配置app
    app = Flask(__name__, instance_relative_config=True)
    #  __name__ Flask 才能知道在哪里可以 找到模板和静态文件等东西
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flask.sqlite'),
        JWT_SECRET_KEY="super-secret"
    )


    jwt = JWTManager(app)

    
    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    #確保instance folder exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #a simple page that says hello
    @app.route("/hello")
    def hello():
        return 'Hello, world!'

    from flaskr import db

    db.init_app(app)
    

    from flaskr import auth
    app.register_blueprint(auth.bp)

    from flaskr import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')


    return app