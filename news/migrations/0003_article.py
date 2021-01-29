# Generated by Django 3.1.4 on 2020-12-22 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20201222_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('post', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('tags', models.ManyToManyField(to='news.tags')),
            ],
        ),
    ]
