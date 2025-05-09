# Generated by Django 5.1.6 on 2025-04-06 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification_app', '0004_alter_customuser_student_dropoff_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_message',
            field=models.TextField(blank=True, default='Default notification message.', null=True),
        ),
    ]
