# Generated by Django 4.2.1 on 2023-05-12 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_remove_question_quiz_quiz_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(related_name='quizzes', to='home.question'),
        ),
    ]
