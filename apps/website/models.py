from django.db import models

# Create your models here.
class WebSettings(models.Model):
	website_title = models.CharField(max_length=120, help_text='Enter website title.')	
	company_name = models.CharField(max_length=60, help_text='Enter company name')
	company_url = models.CharField(max_length=200, help_text='Enter company url')
	company_logo = models.ImageField(upload_to = 'logos/', default = 'company_logo.jpg')
	footer_text = models.CharField(max_length=60, help_text='Enter company footer text.')
	header_color = models.CharField(default='000000', max_length=6, help_text='Enter company header color hexa code without #')
	footer_color = models.CharField(default='000000', max_length=6, help_text='Enter company footer color hexa code without #')
	website_background_color = models.CharField(default='FFFFFF', max_length=6, help_text='Enter company background color hexa code without #')
	footer_text_color = models.CharField(default='000000', max_length=6, help_text='Enter company footer text color hexa code without #')
	primary_color = models.CharField(default='000000', max_length=6, help_text='Enter company primary color hexa code without #')
	secondary_color = models.CharField(default='000000', max_length=6, help_text='Enter company secondary color hexa code without #')
	text_color = models.CharField(default='000000', max_length=6, help_text='Enter company text color hexa code without #')
	next_button_color = models.CharField(default='000000', max_length=6, help_text='Enter next button color hexa code without #')
	next_button_text_color = models.CharField(default='000000', max_length=6, help_text='Enter next button text color hexa code without #')
	matching_tolerance = models.FloatField(null=False, blank=False, default=0.6)

	success_message_title = models.CharField(max_length=200, help_text='Success message title on match.')
	success_message_body = models.CharField(max_length=200, help_text='Success message body on match.')
	failure_message_title = models.CharField(max_length=200, help_text='Failure message title on match.')
	failure_message_body = models.CharField(max_length=200, help_text='Failure message body on match.')

	is_active = models.BooleanField(default=False)