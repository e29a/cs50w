# Generated by Django 4.2.5 on 2023-09-25 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('author', models.CharField(max_length=64)),
                ('likes', models.IntegerField()),
            ],
        ),
    ]