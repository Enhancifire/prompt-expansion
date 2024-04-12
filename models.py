from pydantic import BaseModel


class Query(BaseModel):
    query: str
    no_of_images: int


class APIResponse:
    images: list[str]
    prompt: str
    negativePrompt: str
    steps: int
