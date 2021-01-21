from django.contrib import admin

from .models import Profile, City, MainUser, GameSetting, Transaction, Step, Game

admin.site.register(MainUser)
admin.site.register(City)
admin.site.register(Profile)
admin.site.register(GameSetting)
admin.site.register(Transaction)
admin.site.register(Step)
admin.site.register(Game)