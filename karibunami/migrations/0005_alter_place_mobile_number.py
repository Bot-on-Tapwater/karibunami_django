# Generated by Django 5.0.1 on 2024-01-21 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karibunami', '0004_alter_bookmark_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='mobile_number',
            field=models.CharField(max_length=256, null=True),
        ),
    ]