# Generated by Django 4.2.1 on 2023-05-22 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_completion_remove_question_answers_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completion',
            name='right_answers',
        ),
        migrations.AlterField(
            model_name='completion',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]