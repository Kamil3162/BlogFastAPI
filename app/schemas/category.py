import typing

from pydantic import BaseModel


# first schema will be duirng create name

class CategoryScheme(BaseModel):
    category_name: str


class CategoryObject(BaseModel):
    id: int
    category_name: str

    class Config:
        from_attributes = True  # This enables ORM mode

class CategoryPostObject(BaseModel):
    post_id: int
    category_id: int

    class Config:
        from_attributes = True

class CategoriesPostsObject(CategoryPostObject):
    post_id: int
    categories_ids: typing.List


class CategoryResponse(BaseModel):
    success: bool
    message: str
    data: CategoryObject
