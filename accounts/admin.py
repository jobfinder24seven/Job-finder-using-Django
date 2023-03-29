from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *

# Register your models here.
class UserModel(UserAdmin):
	pass


admin.site.register(CustomUser, UserModel)

admin.site.register(Admin)
admin.site.register(JobSeeker)
admin.site.register(FeedBackEmployer)
admin.site.register(FeedBackJobSeeker)

