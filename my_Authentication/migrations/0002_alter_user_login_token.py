# Generated by Django 3.2 on 2024-05-18 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_Authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_login',
            name='token',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='token'),
        ),
    ]