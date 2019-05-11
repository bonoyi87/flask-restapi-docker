from flask import Flask

from apps.extensions import db, migrate
from apps import company


def create_app(config_object='apps.settings'):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(company.views.blueprint)
    return None
