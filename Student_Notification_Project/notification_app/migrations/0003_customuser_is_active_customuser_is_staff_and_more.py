# Generated by Django 5.1.6 on 2025-04-02 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification_app', '0002_alter_customuser_email_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
