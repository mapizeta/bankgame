from django.contrib import admin

from .models import Game,Gamer,Statistic,Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'amount']

admin.site.register(Game)
admin.site.register(Gamer)
admin.site.register(Statistic)
admin.site.register(Transaction,TransactionAdmin)
