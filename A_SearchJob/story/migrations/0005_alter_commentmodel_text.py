# Generated by Django 4.2.6 on 2023-11-17 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0004_alter_storymodel_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='text',
            field=models.CharField(max_length=300, verbose_name='Text of comment'),
        ),
    ]