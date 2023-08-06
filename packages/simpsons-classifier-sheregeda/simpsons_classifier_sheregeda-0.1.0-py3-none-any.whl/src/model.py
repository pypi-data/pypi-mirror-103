from typing import Dict

import torch
import torch.nn as nn

from torchvision.transforms import transforms
from PIL import Image, ImageOps
from PIL.JpegImagePlugin import JpegImageFile
from efficientnet_pytorch import EfficientNet


class SquarePad:
    """
    Трансформер, который делает изображение квадратным, заполняя наименьшую
    сторону черными пикселями.
    """

    def __call__(
        self, image: JpegImageFile
    ):
        max_side = max(image.size)
        return ImageOps.pad(image, (max_side, max_side))


class SimpsonsClassifier:
    """
    Класс для взаимодействия с моделью классификатором Симпсонов.
    """

    def __init__(
        self, model_path: str,
        label_names: Dict[int, str],
        image_size: int,
    ):
        self.model = EfficientNet.from_name('efficientnet-b1')
        self.model._fc = nn.Linear(
            self.model._fc.in_features, len(label_names)
        )

        if torch.cuda.is_available():
            self.model.load_state_dict(torch.load(model_path))
            self.model.cuda()
        else:
            self.model.load_state_dict(
                torch.load(model_path, map_location=torch.device('cpu'))
            )

        self.model.eval()

        self.transform = transforms.Compose([
            SquarePad(),
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        self.label_names = label_names

    def predict(
        self, image_path: str
    ) -> str:
        """
        Прочитать изображение с диска и получить предсказание модели.

        FIXME: сделать метод асинхронным.

        :param image_path:
            `str`, путь до файла с персонажем.

        :return:
            `str`, предсказанное имя персонажа.
        """
        image = Image.open(image_path)
        image = self.transform(image).unsqueeze(0)
        y_pred = self.model(image)
        _, predicted = torch.max(y_pred, 1)
        return self.label_names[predicted.item()]
