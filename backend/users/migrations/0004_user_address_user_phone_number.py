# Generated by Django 5.1.7 on 2025-03-18 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_customerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='Ethiopia', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='Ethiopiayeye', max_length=12),
        ),
    ]
