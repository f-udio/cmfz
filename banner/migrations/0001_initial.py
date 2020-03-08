# Generated by Django 2.0.6 on 2020-03-05 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bnner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('status', models.SmallIntegerField()),
                ('create_time', models.DateField(auto_now_add=True)),
                ('pic', models.ImageField(upload_to='pics')),
            ],
        ),
    ]