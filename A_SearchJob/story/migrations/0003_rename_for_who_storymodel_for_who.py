# Generated by Django 4.2.6 on 2023-11-17 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0002_rename_headline_storymodel_headline'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storymodel',
            old_name='For_who',
            new_name='for_who',
        ),
    ]