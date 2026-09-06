from pydantic import BaseModel, HttpUrl


class URLCreateRequest(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    short_code: str
    original_url: str
    short_url: str

    class Config:
        from_attributes = True
