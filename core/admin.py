from django.contrib import admin

from .models import MainUser, GameSetting, Transaction, Session, Player, Production, Turn

admin.site.register(MainUser)
admin.site.register(GameSetting)
admin.site.register(Transaction)
admin.site.register(Session)
admin.site.register(Player)
admin.site.register(Production)
admin.site.register(Turn)

