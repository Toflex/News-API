# Generated by Django 4.0 on 2021-12-18 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_news_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='itemID',
            field=models.PositiveBigIntegerField(auto_created=True, null=True, unique=True),
        ),
    ]
