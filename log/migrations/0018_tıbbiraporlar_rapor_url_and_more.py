# Generated by Django 5.0.5 on 2024-05-17 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0017_alter_doktorlar_user_alter_hastalar_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tıbbiraporlar',
            name='rapor_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='tıbbiraporlar',
            name='rapor_json',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
