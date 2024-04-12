from generator import sceneGeneration, imageGeneration
from crew import SceneCrew
import asyncio

screw = SceneCrew()

scene = "A dark and lonely night"


async def main():
    data = await sceneGeneration(screw, scene, 2)

    print(len(data))

    with open("abc.txt", "w") as f:
        f.write(str(data))

    result = await imageGeneration(data)

    print(result)
    print(len(result))


if __name__ == "__main__":
    data = asyncio.run(main())
