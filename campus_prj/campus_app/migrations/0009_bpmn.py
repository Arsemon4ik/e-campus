# Generated by Django 5.0 on 2024-01-04 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus_app', '0008_alter_article_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='BPMN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagram', models.TextField(verbose_name='Diagram')),
            ],
        ),
    ]
