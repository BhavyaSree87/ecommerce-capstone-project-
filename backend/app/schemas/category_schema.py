from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    category_name: str = Field(..., min_length=1, max_length=150, example="Electronics")
    description: Optional[str] = Field(None, max_length=1000, example="Category description")

    model_config = ConfigDict(str_strip_whitespace=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    category_name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=1000)

    model_config = ConfigDict(str_strip_whitespace=True)
