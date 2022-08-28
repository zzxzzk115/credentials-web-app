# Generated by Django 4.1 on 2022-08-28 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('credential_id', models.TextField(primary_key=True, serialize=False)),
                ('base_url', models.TextField()),
                ('access_transcript_from', models.TextField()),
                ('user_email_address', models.EmailField(max_length=254)),
                ('user_access_code', models.TextField()),
                ('left_logo_path', models.TextField()),
                ('right_logo_path', models.TextField()),
                ('pdf_file_path', models.TextField()),
            ],
        ),
    ]
