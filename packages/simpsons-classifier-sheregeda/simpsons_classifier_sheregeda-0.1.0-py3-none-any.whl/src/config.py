from typing import Dict

import yaml

from pydantic import BaseSettings


class ClassifierConfig(BaseSettings):
    """
    Конфигурация для модели.
    """
    # Наименование файла, который содержит веса модели
    name: str
    # Каталог с моделями
    dir: str
    # Ширина и длина картинки в пикселях, которая подается в сеть
    image_size: int
    # Имена персонажей по их идентификатору
    label_names: Dict[int, str]


class AppConfig(BaseSettings):
    """
    Конфигурация приложения.
    """
    # Конфигурация для модели
    model: ClassifierConfig
    # Каталог, в котором осуществляется поиск изображений для классификации
    images_dir: str


def read_config(
    config_path: str
) -> AppConfig:
    """
    По переданному пути прочитать содержимое yaml файла и сформировать
    конфигурация приложения на основе него.

    :param config_path:
        `str`, путь до файла с настройками.

    :return:
        `AppConfig`, конфигурация приложения.
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return AppConfig(**config)
