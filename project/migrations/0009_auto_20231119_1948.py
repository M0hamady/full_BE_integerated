# Generated by Django 3.2.20 on 2023-11-19 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0002_chatboot_chatstate'),
        ('teamview', '0002_viewer_user'),
        ('client', '0005_auto_20231113_2145'),
        ('technical', '0001_initial'),
        ('project', '0008_auto_20231102_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies_client_project', to='client.client'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='designer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies_designer_project', to='designer.designer'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies_project', to='project.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_project', to='project.project'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='technical',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies_technical_project', to='technical.technical'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='viewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies_viewer_project', to='teamview.viewer'),
        ),
    ]