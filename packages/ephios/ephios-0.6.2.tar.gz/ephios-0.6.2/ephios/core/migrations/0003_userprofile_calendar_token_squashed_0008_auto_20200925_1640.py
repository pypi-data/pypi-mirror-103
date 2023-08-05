# Generated by Django 3.1.1 on 2020-09-25 14:54

import secrets
import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_initial_permissions"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="calendar_token",
            field=models.CharField(default=secrets.token_urlsafe, max_length=254),
        ),
        migrations.CreateModel(
            name="QualificationCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("title", models.CharField(max_length=254, verbose_name="title")),
            ],
            options={
                "verbose_name": "qualification track",
                "verbose_name_plural": "qualification tracks",
            },
        ),
        migrations.RemoveField(
            model_name="qualification",
            name="track",
        ),
        migrations.RemoveField(
            model_name="qualificationgrant",
            name="expiration_date",
        ),
        migrations.AddField(
            model_name="qualification",
            name="included_qualifications",
            field=models.ManyToManyField(related_name="included_in_set", to="core.Qualification"),
        ),
        migrations.AddField(
            model_name="qualification",
            name="uuid",
            field=models.UUIDField(default=None, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="qualificationgrant",
            name="expires",
            field=models.DateTimeField(blank=True, null=True, verbose_name="expiration date"),
        ),
        migrations.AlterField(
            model_name="qualificationgrant",
            name="qualification",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="grants",
                to="core.qualification",
            ),
        ),
        migrations.AlterField(
            model_name="qualificationgrant",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="qualification_grants",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="QualificationTrack",
        ),
        migrations.AddField(
            model_name="qualification",
            name="category",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="qualifications",
                to="core.qualificationcategory",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="qualification",
            name="abbreviation",
            field=models.CharField(default="", max_length=254),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name="qualification",
            options={"verbose_name": "qualification", "verbose_name_plural": "qualifications"},
        ),
        migrations.AlterModelOptions(
            name="userprofile",
            options={"verbose_name": "user profile", "verbose_name_plural": "user profiles"},
        ),
        migrations.AlterField(
            model_name="qualification",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="qualifications",
                to="core.qualificationcategory",
                verbose_name="category",
            ),
        ),
        migrations.AlterField(
            model_name="qualification",
            name="included_qualifications",
            field=models.ManyToManyField(related_name="included_by", to="core.Qualification"),
        ),
        migrations.AlterField(
            model_name="qualification",
            name="title",
            field=models.CharField(max_length=254, verbose_name="title"),
        ),
        migrations.AlterField(
            model_name="qualificationgrant",
            name="qualification",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.qualification",
                verbose_name="qualification",
            ),
        ),
        migrations.AlterField(
            model_name="qualificationgrant",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="user profile",
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="calendar_token",
            field=models.CharField(
                default=secrets.token_urlsafe, max_length=254, verbose_name="calendar token"
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="date_of_birth",
            field=models.DateField(verbose_name="date of birth"),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="email address"),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="first_name",
            field=models.CharField(max_length=254, verbose_name="first name"),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="last_name",
            field=models.CharField(max_length=254, verbose_name="last name"),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="phone",
            field=models.CharField(max_length=254, null=True, verbose_name="phone number"),
        ),
        migrations.AlterField(
            model_name="qualification",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name="qualificationgrant",
            name="qualification",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="grants",
                to="core.qualification",
                verbose_name="qualification",
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="phone",
            field=models.CharField(
                blank=True, default="", max_length=254, verbose_name="phone number"
            ),
            preserve_default=False,
        ),
    ]
