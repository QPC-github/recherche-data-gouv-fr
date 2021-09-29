from flask import Flask
from app.config import Config
from app.containers import Container
from app.presentation import seed, routes, api


def create_app(config: object = Config) -> Flask:
    container = Container()
    container.wire(modules=[routes, seed])

    app: Flask = Flask(__name__)
    app.container = container
    app.config.from_object(config)

    container.config.elasticsearch_url.from_value(app.config['ELASTICSEARCH_URL'])
    container.config.datasets_per_page.from_value(app.config['DATASETS_PER_PAGE'])
    container.config.search_dataset_fields.from_value(app.config['SEARCH_DATASET_FIELDS'])
    container.config.search_dataset_featured_weight.from_value(app.config['SEARCH_DATASET_FEATURED_WEIGHT'])
    container.config.search_dataset_certified_weight.from_value(app.config['SEARCH_DATASET_CERTIFIED_WEIGHT'])

    # register the database command
    seed.init_app(app)

    app.register_blueprint(routes.bp)
    app.register_blueprint(api.bp)

    return app
