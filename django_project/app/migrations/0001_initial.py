# Generated by Django 2.1.1 on 2018-09-14 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('space_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('client', 'client'), ('manager', 'manager')], default='client', max_length=50)),
                ('access', models.CharField(choices=[('yes', 'yes'), ('no', 'no'), ('empty', 'empty')], default='empty', max_length=50)),
            ],
            options={
                'verbose_name': 'AccessRequest',
                'verbose_name_plural': 'AccessRequest',
            },
        ),
    ]