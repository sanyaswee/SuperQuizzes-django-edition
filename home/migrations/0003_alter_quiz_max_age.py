# Generated by Django 4.2.1 on 2023-05-09 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_quiz_completed_as_form_quiz_completed_as_quiz_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='max_age',
            field=models.SmallIntegerField(default=100),
        ),
    ]