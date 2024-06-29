from fastapi import FastAPI
from src.models import Bn2EnTranslator
from pydantic import BaseModel


class Translation(BaseModel):
    text_bn: str
    text_en: str


app = FastAPI()
bn2en = Bn2EnTranslator()


# @app.get('/ping/')
# async def ping():
#     return {"message": "pong"}


@app.get('/healthcheck')
async def root():
    return {"status": "ok"}


@app.get('/translate/')
async def translate(text: str):
    """
    Translates a sentence from Bangla to English
    :param text: Bengali text
    :return: English text
    """
    text_en = bn2en.translate(text)
    # text_en = bn2en(text)
    translation = Translation(text_bn=text, text_en=text_en)
    return translation







