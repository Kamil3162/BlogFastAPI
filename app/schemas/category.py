from pydantic import BaseModel

# first schema will be duirng create name

class CategoryScheme(BaseModel):
    category_name: str

class CategoryObject(BaseModel):
    id: int
    category_name: str

class CategoryPostObject(BaseModel):
    post_id: int
    category_id: int

