# Generated by Django 3.1.4 on 2021-01-20 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='language',
            field=models.CharField(default='python', max_length=6),
            preserve_default=False,
        ),
    ]
