import os

from fastapi import Body, Depends, APIRouter, status, HTTPException
from pydantic import BaseModel

from simpsons_classifier import deps


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
    responses={
        404: {
            'description': 'Файл с изображением не найден',
        },
    }
)
def predict(
    image_id: str = Body(
        ..., embed=True, description='Идентификатор изображения'
    ),
    app: deps.App = Depends()
):
    image_path = os.path.join(app.config.images_dir, image_id)

    if not os.path.isfile(image_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    label = app.clf.predict(image_path=image_path)
    return {'label': label}
