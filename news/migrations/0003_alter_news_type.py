# Generated by Django 4.0 on 2021-12-18 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_news_managers_news_apicreated_news_kids_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='type',
            field=models.CharField(choices=[('comment', 'Comment'), ('story', 'Story'), ('job', 'Job'), ('poll', 'Poll')], default='comment', max_length=200),
        ),
    ]