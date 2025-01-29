from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'organization', 'address', 'adharcard',
                    'is_farmer', 'acre_of_land', 'kisan_card', 'is_buyer', 'gst')
    search_fields = ('user__username', 'phone', 'organization')
    list_filter = ('is_farmer', 'is_buyer')


admin.site.register(UserProfile, UserProfileAdmin)
