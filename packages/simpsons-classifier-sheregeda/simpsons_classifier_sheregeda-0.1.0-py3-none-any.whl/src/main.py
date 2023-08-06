import os

from fastapi import FastAPI

from src.config import AppConfig, ClassifierConfig, read_config
from src.model import SimpsonsClassifier
from src.api import api


def make_app(
    config: AppConfig,
    clf: SimpsonsClassifier,
) -> FastAPI:
    app = FastAPI()
    app.include_router(api)
    app.state.clf = clf
    app.state.config = config
    return app


def make_classifier(
    config: ClassifierConfig,
) -> SimpsonsClassifier:
    return SimpsonsClassifier(
        model_path=os.path.join(config.dir, config.name),
        label_names=config.label_names,
        image_size=config.image_size
    )


def app() -> FastAPI:
    config_dir = os.getenv('CONFIG_DIR')
    if config_dir is None:
        raise Exception('CONFIG_DIR env var is not specified')

    config = read_config(os.path.join(config_dir, 'classifier.yaml'))
    clf = make_classifier(config=config.model)

    return make_app(config=config, clf=clf)
