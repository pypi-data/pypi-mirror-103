import requests
import json
import time
import datetime
from flask import request, request_finished, got_request_exception, request_started, current_app

class InstaLog:

    def __init__(self, metadata={}, log_type='string', api_key=None, api_secret_key=None):
        self.check_type('metadata', metadata, [type({})])
        self.check_type('log_type', log_type, [type('')])
        self.check_type('api_key', api_key, [type(''), type(None)])
        self.check_type('api_secret_key', api_secret_key, [type(''), type(None)])
        self.metadata = metadata
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.log_type = log_type
        self.protocol = "https"
        self.domain = "www.regiment.tech"
        self.log_route = "/log/"
        self.request_headers = {
            "api-key": self.api_key,
            "api-secret-key": self.api_secret_key
        }
        self.CRITICAL=50
        self.ERROR=40
        self.WARNING=30
        self.INFO=20
        self.DEBUG=10
        self.NOTSET=0

    def check_type(self, name, val, expected_types):
        for expected_type in expected_types:
            if type(val) == expected_type:
                return
        raise Exception(
            'InstaLog: given {} of type {} expected one of [{}]'.format(
                name,
                type(val),
                expected_types
                )
            )

    def init_app(self, app, **kwargs):

        metadata = app.config.get('INSTALOG_META_DATA', kwargs.get('metadata', self.metadata))
        api_key = app.config.get('INSTALOG_API_KEY', kwargs.get('api_key', self.api_key))
        api_secret_key = app.config.get('INSTALOG_API_SECRET_KEY', kwargs.get('api_secret_key', self.api_secret_key))
        log_type = app.config.get('INSTALOG_LOG_TYPE', kwargs.get('log_type', self.log_type))

        self.check_type('metadata', metadata, [type({})])
        self.check_type('log_type', log_type, [type('')])
        self.check_type('api_key', api_key, [type('')])
        self.check_type('api_secret_key', api_secret_key, [type('')])

        self.metadata = metadata
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.log_type = log_type
        self.request_headers = {
            "api-key": self.api_key,
            "api-secret-key": self.api_secret_key
        }
        app.instalog = self
        request_started.connect(self.get_request_start_time, app)
        request_finished.connect(self.log_request, app)
        got_request_exception.connect(self.log_exception, app)

    def log_request(self, sender, response):

        if hasattr(request, 'instalog_request_start_time'):
            response_time = time.time() - request.instalog_request_start_time

        additional_attrs = {
            "response_time": response_time
        }

        sender.instalog.info('{} - - [{}] "{} {} {}" {} -'.format(request.remote_addr, self.get_current_date_time(),
            request.method,
            request.full_path,
            request.environ.get('SERVER_PROTOCOL'),
            response.status
            ), additional_attrs = additional_attrs)

    def log_exception(self, sender, exception):
        sender.instalog.info('{} - - [{}] "{} {} {}" - {}'.format(
            request.remote_addr,
            self.get_current_date_time(),
            request.method,
            request.path,
            request.environ.get('SERVER_PROTOCOL'),
            self.exc_info_from_error(exception)
            ))

    def info(self, log, additional_attrs={}):
        self.log(log, log_level=self.INFO, additional_attrs=additional_attrs)

    def log(self, log, log_level=10, additional_attrs={}):

        try:
            
            if not self.is_initialized():
                raise Exception("flask_regiment.InstaLog: not initialized with API_SECRET_KEY")

            request_payload = {
                "log": log,
                "log_type": self.log_type,
                "log_level": log_level,
                "metadata": self.metadata,
                "generated_at": time.time()
            }

            request_payload.update(additional_attrs)

            response = requests.post(
                url='{}://{}{}'.format(self.protocol, self.domain, self.log_route),
                json=request_payload,
                headers=self.request_headers)

        except Exception as err:
            print(err)
    
    def get_request_start_time(self, sender, **kwargs):
        request.instalog_request_start_time = time.time()

    def is_initialized(self):
        if self.api_secret_key == None:
            return False
        return True

    def get_current_date_time(self):
        date_time = datetime.datetime.now(datetime.timezone.utc)
        return date_time.strftime("%d/%b/%Y %H:%M:%S")

    def exc_info_from_error(self, error):
        if isinstance(error, tuple) and len(error) == 3:
            exc_type, exc_value, tb = error
        elif isinstance(error, BaseException):
            tb = getattr(error, "__traceback__", None)
            if tb is not None:
                exc_type = type(error)
                exc_value = error
            else:
                exc_type, exc_value, tb = sys.exc_info()
                if exc_value is not error:
                    tb = None
                    exc_value = error
                    exc_type = type(error)
        else:
            raise ValueError("Expected Exception object to report, got %s!" % type(error))

        return exc_type, exc_value, tb
