# Generated by Django 3.0.7 on 2020-10-23 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comp_lib', '0004_auto_20201022_2027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['number']},
        ),
    ]
