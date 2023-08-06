from flask import Flask
from flask_regiment import InstaLog
import time

instalog = InstaLog()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        INSTALOG_API_SECRET_KEY='84e74a5b-1235-4da5-85ad-b46fa7888543',
        INSTALOG_API_KEY='ad8459f8-300c-4b56-a3ec-67552b09777e',
        INSTALOG_META_DATA={
            "environment": "staging",
            "service_name": "test_app",
            "namespace": "zeroone"
        },
        INSTALOG_LOG_TYPE='string'
    )

    instalog.init_app(app)

    app.instalog.info("custom log")

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    @app.route('/e')
    def error():
        1/0
        return '', 200

    return app
