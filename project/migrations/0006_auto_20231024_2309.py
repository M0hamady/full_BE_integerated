# Generated by Django 3.2.20 on 2023-10-24 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20231023_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('Key_option', models.CharField(max_length=20)),
                ('created_by', models.CharField(max_length=40, null=True)),
                ('uuid', models.UUIDField(editable=False, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies_options', to='project.commentoptions')),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=255)),
                ('uuid', models.UUIDField(editable=False, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='ProjectDetail_comment',
        ),
        migrations.AddField(
            model_name='projectbasic',
            name='heater',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.heater', verbose_name='heater'),
        ),
        migrations.AddField(
            model_name='projectbasic',
            name='toiletType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.toilettype', verbose_name='toiletType'),
        ),
        migrations.AlterField(
            model_name='projectbasic',
            name='hight_window',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='notes',
            name='project_basic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.projectbasic'),
        ),
        migrations.AddField(
            model_name='commentoptions',
            name='project_basic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_options', to='project.projectbasic'),
        ),
    ]
