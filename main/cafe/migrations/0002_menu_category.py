# Generated by Django 4.2.10 on 2024-02-26 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='category',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
