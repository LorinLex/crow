from django.contrib import admin

from .models import  MainUser, GameSetting, Transaction

admin.site.register(MainUser)
admin.site.register(GameSetting)
admin.site.register(Transaction)
