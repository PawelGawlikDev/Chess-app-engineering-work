# Generated by Django 4.0.6 on 2022-10-05 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chessapp', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='partie',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chessapp.user'),
        ),
    ]
