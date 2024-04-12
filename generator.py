from crew import SceneCrew
from stable_connector import txt2image_request
import uuid
import asyncio


async def sceneGeneration(scene: str, no: int):
    c = SceneCrew()
    tasks = [
        asyncio.create_task(c.generateScene(scene)) for _ in range(no)
    ]

    done, pending = await asyncio.wait(tasks)

    results = []

    for task in done:
        results.append(task.result())

    return results


def imageGeneration(results, uuid_str: str):
    # tasks = [
    #     asyncio.create_task(
    #         txt2image_request(res, uid, i)
    #         for i, res in enumerate(results)
    #     )
    # ]
    #
    # done, pending = await asyncio.wait(tasks)
    #
    # return [task.result() for task in done]

    data = []
    for i, res in enumerate(results):
        data.append(txt2image_request(res, uuid_str, i))

    return data


def aggregateData(data):
    results = []

    for item in data:
        imgBase64 = item["images"]
        params = item["parameters"]
        prompt = params["prompt"]

        results.append({
            "prompt": prompt,
            "image": imgBase64
        })

    return results
