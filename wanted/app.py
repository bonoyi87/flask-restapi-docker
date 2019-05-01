from flask import Flask

from wanted.extensions import db


def create_app(config_object='wanted.settings'):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)

    return None

