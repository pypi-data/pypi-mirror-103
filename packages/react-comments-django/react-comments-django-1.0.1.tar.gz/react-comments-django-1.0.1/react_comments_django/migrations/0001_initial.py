# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-09-02 17:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import react_comments_django.models
import react_comments_django.utils.utility_funcs


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('uid', models.UUIDField(default=react_comments_django.utils.utility_funcs.gen_uuid, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, default='')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(blank=True, null=True)),
                ('deleted_on', models.DateTimeField(blank=True, null=True)),
                ('_upvotes', models.IntegerField(blank=True, default=0)),
                ('_downvotes', models.IntegerField(blank=True, default=0)),
                ('wsi', models.FloatField(blank=True, default=0)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=150, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='react_comments_django.Post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('url', models.URLField(blank=True, default='', max_length=120)),
                ('views', models.IntegerField(blank=True, default=0)),
                ('locked', models.BooleanField(default=False)),
                ('is_stickied', models.BooleanField(default=False)),
                ('op', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='react_comments_django.Post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=200, null=True, unique=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, default='', max_length=120)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserPostVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val', react_comments_django.models.IntegerRangeField(blank=True, default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_post_votes', to='react_comments_django.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='thread',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread', to='react_comments_django.Topic'),
        ),
    ]
