# Generated by Django 3.2.4 on 2021-06-21 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_author_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name']},
        ),
    ]
