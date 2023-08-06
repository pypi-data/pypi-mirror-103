from fastapi import Request

from simpsons_classifier.model import SimpsonsClassifier
from simpsons_classifier.config import AppConfig


class App:
    """
    Зависимость, которая инкапсулирует общие ресурсы приложения.
    """
    def __init__(self, req: Request):
        self.clf: SimpsonsClassifier = req.app.state.clf
        self.config: AppConfig = req.app.state.config
