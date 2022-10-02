# Generated by Django 4.1 on 2022-09-29 09:01

from django.db import migrations

from api_activity.static import ActivityData
from common.constants.api_activity import ActivityType
from utils.activity import read_content


def init_data_activity(apps, schema_editor):
    activity_model = apps.get_model("api_activity", "Activity")
    charity_activity = [activity_model(title=charity['title'],
                                       content=read_content(charity['content']), location=charity['location'],
                                       start_date=charity['start_date'], end_date=charity['end_date'],
                                       cover_picture=charity['cover_picture'], expense=charity['expense'],
                                       activity_type=ActivityType.CHARITY)
                        for charity in ActivityData.charity_activity]

    event = [activity_model(title=event['title'],
                            content=read_content(event['content']), location=event['location'],
                            start_date=event['start_date'], end_date=event['end_date'],
                            cover_picture=event['cover_picture'], expense=event['expense'],
                            activity_type=ActivityType.EVENT)
             for event in ActivityData.event]

    activity_model.objects.bulk_create(charity_activity)
    activity_model.objects.bulk_create(event)


class Migration(migrations.Migration):

    dependencies = [
        ('api_activity', '0004_rename_description_activity_content'),
    ]

    operations = [
        migrations.RunPython(init_data_activity, migrations.RunPython.noop)
    ]