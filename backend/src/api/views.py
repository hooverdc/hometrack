from typing import List

from django.http import HttpRequest, Http404
from django.shortcuts import render, get_object_or_404

from decimal import Decimal
from datetime import datetime

from ninja import Router, Schema
from pydantic import ValidationError, ValidationInfo, field_validator

from .models import Items, Images, Categories

from .services.images import ImagesService

# Create your views here.

router = Router()


class Image(Schema):
    uri: str


class Item(Schema):
    item_id: int
    name: str
    description: str
    quantity: int
    cost: Decimal
    category: str
    updated_on: datetime
    created_on: datetime
    images: List[str]

    @field_validator("category", mode="before")
    @classmethod
    def category_validator(cls, v) -> str:

        return v.name

    # @field_validator("images", mode="before")
    # @classmethod
    # def images_validator(cls, v: List[Image]) -> List[str]:
    #     pass


class CreateCategory(Schema):
    name: str


@router.post("/categories")
def create_category(request: HttpRequest, body: CreateCategory):
    category = Categories(name=body.name)
    category.save()


class Category(Schema):
    category_id: int
    name: str


@router.get("/categories")
def list_categories(request: HttpRequest):
    categories = Categories.objects.all()
    return {"categories": [Category.from_orm(c) for c in categories]}


@router.get("/items")
def list_items(request: HttpRequest):
    return {"items": Item.from_orm(item) for item in Items.objects.all()}


@router.get("/items/{item_id}")
def get_item(request: HttpRequest, item_id: str):
    try:
        item = get_object_or_404(Items, item_id=item_id)
    except Http404 as ex:
        raise ex
    except Exception as ex:
        raise ex

    return Item.from_orm(item)


class CreateItem(Schema):
    name: str
    description: str
    quantity: int
    cost: Decimal
    category: int


@router.post("/items")
def create_item(request: HttpRequest, body: CreateItem):
    item = Items(
        name=body.name,
        description=body.description,
        quantity=body.quantity,
        cost=body.cost,
        category_id=body.category,
    )
    item.save()
    return Item.from_orm(item)


@router.put("/items/{item_id}")
def update_item(request: HttpRequest, item_id: str):
    pass


@router.get("/items/{item_id}/image")
def upload_image(request: HttpRequest, item_id: str):
    """Return a presigned URL for uploading an image"""
    images_service = ImagesService()
    url = images_service.create_presigned_url(1, 1)
    return url


@router.delete("/items/{item_id}/image/{image_id}")
def delete_image(request: HttpRequest, item_id: str, image_id: str):
    """Delete an image"""
    # delete object from S3
    # delete image row
    pass
