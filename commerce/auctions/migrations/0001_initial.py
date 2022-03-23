# Generated by Django 4.0.1 on 2022-03-23 10:39

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('starting_price', models.FloatField()),
                ('image_url', models.URLField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('current_bid', models.FloatField(blank=True, null=True)),
                ('buyer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Bidder', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Category', to='auctions.category')),
                ('creator', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('watchlist', models.ManyToManyField(blank=True, related_name='Watchers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Commented_item', to='auctions.list')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Commentator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.FloatField()),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Item_bidded', to='auctions.list')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Buyer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
