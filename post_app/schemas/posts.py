from pydantic import BaseModel, ConfigDict, Field


class PostCreateSchema(BaseModel):
    post_text: str = Field(min_length=1, max_length=10000)


class PostUpdateSchema(BaseModel):
    post_text: str = Field(min_length=1, max_length=10000)


class PostInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    post_text: str
    owner_id: int
    img_url: str | None = None
