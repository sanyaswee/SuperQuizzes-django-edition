# Generated by Django 4.2.1 on 2023-05-23 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_remove_completion_right_answers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='searchable',
            field=models.CharField(default='<django.db.models.fields.charfield>', max_length=50),
        ),
    ]
