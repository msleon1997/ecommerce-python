from django.contrib import admin
from accounts.models import Account, userProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'username', 'mail', 'phone', 'is_active')
    list_display_links = ('first_name', 'last_name', 'mail')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined'),
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    
    
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius: 50px;" />'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')
    
    
    
admin.site.register(Account, AccountAdmin)
admin.site.register(userProfile, UserProfileAdmin)

