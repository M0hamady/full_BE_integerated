# Generated by Django 3.2.20 on 2023-10-23 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20231023_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ceilingdecoration',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='designcolors',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='designstyle',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='flooringmaterial',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='furniture',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='hightwindow',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='lightingtype',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='walldecorations',
            name='comment',
        ),
    ]
