# Generated by Django 4.2.6 on 2023-11-17 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0006_alter_commentmodel_options_alter_storymodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storymodel',
            name='for_who',
            field=models.CharField(choices=[('employers', 'employers'), ('employees', 'employees'), ('everyone', 'everyone')], default='everyone', max_length=20, verbose_name='Useful for whom'),
        ),
    ]
