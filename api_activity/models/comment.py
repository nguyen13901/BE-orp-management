
from django.db import models

from api_activity.managers import CommentManager
from api_activity.models import Activity
from api_user.models import Account
from base.models import TimeStampedModel


class Comment(TimeStampedModel):
    content = models.CharField(max_length=255, default="")
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    objects = CommentManager()

    class Meta:
        db_table = 'comment'
