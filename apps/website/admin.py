from django.contrib import admin
from apps.website.models import WebSettings

# Register the Admin classes for WebSettings using the decorator
@admin.register(WebSettings)
class WebSettingsAdmin(admin.ModelAdmin):
	list_display = ('company_name', 'company_logo', 'is_active')
