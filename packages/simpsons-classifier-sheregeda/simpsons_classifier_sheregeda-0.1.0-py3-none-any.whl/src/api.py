import os

from fastapi import Body, Depends, APIRouter
from pydantic import BaseModel

from src import deps


api = APIRouter(prefix='/v1')


class PredictResponse(BaseModel):
    """
    Ответ хэндлера для получения предсказания модели.
    """
    # Имя персонажа
    label: str


@api.post(
    '/predict',
    summary='Получить предсказание о том, какой из персонажей Симпсонов '
            'изображен на картинке.',
    response_model=PredictResponse,
)
def predict(
    image_id: str = Body(
        ..., embed=True, description='Идентификатор изображения'
    ),
    app: deps.App = Depends()
):
    image_path = os.path.join(app.config.images_dir, image_id)
    label = app.clf.predict(image_path)
    return {'label': label}
