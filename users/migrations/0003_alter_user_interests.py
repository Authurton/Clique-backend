# Generated by Django 5.0.6 on 2024-06-09 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_interests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='interests',
            field=models.JSONField(default=list),
        ),
    ]
