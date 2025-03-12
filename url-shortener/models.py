from pydantic import BaseModel

class URLRequest(BaseModel):
    long_url: str
    custom_alias: str = None
