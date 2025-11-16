from django.contrib import admin
from .models import Profile



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role',)
    search_fields = ('user__email',)


admin.site.register(Profile, ProfileAdmin)



admin.site.site_header = "Reservation Administration"
admin.site.site_title = "Reservation Admin"
admin.site.index_title = "Bienvenue dans l'administration Reservation"