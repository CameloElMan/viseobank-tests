# Generated by Django 2.2.2 on 2019-09-17 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_websettings_text_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='websettings',
            name='footer_text',
            field=models.CharField(default='© 2019 VISEO - All rights reserved.', help_text='Enter company footer', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='websettings',
            name='footer_text_color',
            field=models.CharField(default='000000', help_text='Enter company primary color hexa code without #', max_length=6),
        ),
    ]