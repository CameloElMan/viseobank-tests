# Generated by Django 2.2.2 on 2019-09-17 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_websettings_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='websettings',
            name='company_url',
            field=models.CharField(default='hello', help_text='Enter company url', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='websettings',
            name='company_logo',
            field=models.ImageField(default='company_logo.jpg', upload_to='logos/'),
        ),
    ]