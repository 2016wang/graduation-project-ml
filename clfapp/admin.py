from django.contrib import admin

# Register your models here.

from .models import Users, Models, Settings, Uploadfile


class UsersAdmin(admin.ModelAdmin):
    list_display = ['username']


class ModelsAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'model_upload', 'model_desc']


class SettingsAdmin(admin.ModelAdmin):
    pass


class UploadfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'file', 'uploaded_at']


admin.site.register(Users, UsersAdmin)
admin.site.register(Models, ModelsAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(Uploadfile, UploadfileAdmin)
