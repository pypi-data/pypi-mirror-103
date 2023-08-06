from flask import Flask
from flask_regiment import InstaLog
import time

instalog = InstaLog()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        INSTALOG_API_SECRET_KEY='b1a4be7f-84b2-44e1-94ba-d4c5a030d20b',
        INSTALOG_API_KEY='c5cd09f9-17e4-4fe4-ba8f-53593352b1da',
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
