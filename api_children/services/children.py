import os
from typing import List

from django.db import transaction
from django.db.models import Value
from django.db.models.functions import Collate

from api_children.models import Children
from base.services import ImageService
from common.constants.api_children import ChildrenStatus
from common.constants.base import Gender
from common.constants.image import ImageDefaultChildren


class ChildrenService:
    @classmethod
    def get_filter_query(cls, request):
        name = request.query_params.get("name")
        age = request.query_params.get("age")
        gender = request.query_params.get("gender")
        status = request.query_params.get("status")

        age = age if age != 'undefined' else ''
        gender = gender if gender != 'undefined' else ''
        status = status if status != 'all' else ''

        filter_args = dict()

        if age:
            filter_args.update(age=age)
        if gender:
            filter_args.update(gender=gender)
        if status:
            filter_args.update(status=status)
        if name:
            name = Collate(Value(name.strip()), "utf8mb4_general_ci")

        queryset = Children.objects.filter(name__icontains=name, **filter_args)
        return queryset

    @classmethod
    def init_data_children(cls, request):
        data = request.data.dict()
        gender = int(data.get('gender'))
        personal_picture = request.FILES.get('personal_picture')
        if personal_picture:
            image_link = ImageService.upload_image(personal_picture, os.getenv('CLOUDINARY_CHILDREN_FOLDER'))
            data['personal_picture'] = image_link
        else:
            data['personal_picture'] = ImageDefaultChildren.Female if gender == Gender.FEMALE else ImageDefaultChildren.Male
        return data

    @classmethod
    def upload_image_data_children(cls, request):
        data = request.data.dict()
        personal_picture = request.FILES.get('personal_picture')
        if personal_picture:
            image_link = ImageService.upload_image(personal_picture, os.getenv('CLOUDINARY_CHILDREN_FOLDER'))
            data['personal_picture'] = image_link
        return data

    @classmethod
    def update_children_status(cls, children, status):
        children.status = status
        children.save()
        return children

    @classmethod
    def destroy_multi_children(cls, children_ids: List[str]) -> bool:
        try:
            with transaction.atomic():
                bonus_leaves = Children.objects.filter(id__in=children_ids)
                bonus_leaves.delete()
            return True
        except Exception as e:
            return False
