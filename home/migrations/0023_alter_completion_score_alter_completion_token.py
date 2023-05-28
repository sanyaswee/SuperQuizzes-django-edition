# Generated by Django 4.2.1 on 2023-05-28 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_completion_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completion',
            name='score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='completion',
            name='token',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]