# Generated by Django 4.0.4 on 2022-05-09 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expensetrack', '0002_subscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribe',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expensetrack.signup'),
        ),
    ]
