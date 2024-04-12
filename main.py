from fastapi import FastAPI
from models import Query
from generator import sceneGeneration, imageGeneration, aggregateData
import asyncio
import uuid

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello, World!"}


@app.post("/generate")
async def generateImage(query: Query):
    scenes = await sceneGeneration(query.query, query.no_of_images)
    #
    print(scenes)

    uuid_str = str(uuid.uuid4())

    results = imageGeneration(scenes, uuid_str)

    images = aggregateData(results)

    return {"images": images, "id": uuid_str}
