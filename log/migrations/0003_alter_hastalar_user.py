# Generated by Django 5.0.5 on 2024-05-15 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0002_alter_hastalar_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hastalar',
            name='user',
            field=models.CharField(max_length=50),
        ),
    ]
