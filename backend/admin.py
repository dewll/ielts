from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Audio_store,Skill

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name',
                    'email','zip_code','phone',
                    'state','city','score','password')

admin.site.register(User, UserAdmin)
admin.site.register(Audio_store)
admin.site.register(Skill)