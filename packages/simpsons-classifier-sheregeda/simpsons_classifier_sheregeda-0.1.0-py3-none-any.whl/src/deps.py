from fastapi import Request

from src.model import SimpsonsClassifier
from src.config import AppConfig


class App:
    """
    Зависимость, которая инкапсулирует общие ресурсы приложения.
    """
    def __init__(self, req: Request):
        self.clf: SimpsonsClassifier = req.app.state.clf
        self.config: AppConfig = req.app.state.config
