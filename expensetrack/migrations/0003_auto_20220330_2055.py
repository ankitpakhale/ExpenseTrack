# Generated by Django 3.0 on 2022-03-30 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expensetrack', '0002_alter_expense_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(default='', max_length=30)),
                ('lastname', models.CharField(default='', max_length=30)),
                ('email', models.EmailField(default='', max_length=254)),
                ('password', models.CharField(default='', max_length=15)),
            ],
        ),
        migrations.AlterField(
            model_name='expense',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
