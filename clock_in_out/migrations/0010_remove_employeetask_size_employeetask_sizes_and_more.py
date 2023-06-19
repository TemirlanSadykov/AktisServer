# Generated by Django 4.1.7 on 2023-06-17 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clock_in_out', '0009_rename_name_task_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeetask',
            name='size',
        ),
        migrations.AddField(
            model_name='employeetask',
            name='sizes',
            field=models.ManyToManyField(to='clock_in_out.size'),
        ),
        migrations.AlterField(
            model_name='employeetask',
            name='finish_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='employeetask',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]