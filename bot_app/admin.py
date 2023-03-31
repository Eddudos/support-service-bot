from django.contrib import admin
from django.utils import timezone
from . import models


# Регистрация таблиц в админке для возможности редактирования
admin.site.register([models.BotClient, models.BotDictionary, models.TokenTable])

@admin.register(models.BotButton)
class BotButtonAdmin(admin.ModelAdmin):
    fields = ('sort_id', 'name', 'reaction', 'open_line', 'num_selected')
    readonly_fields = ('num_selected',)
    list_display = ('name', 'sort_id')
    ordering = ('sort_id',)


@admin.register(models.PublicationTable)
class PublicationTableAdmin(admin.ModelAdmin):
    fields = ('name', 'image', 'text', 'date', 'status', 'num_users', 'num_sent')
    readonly_fields = ('status', 'num_users', 'num_sent')
    # def get_changeform_initial_data(self, request):
    #     print('asdsa')
    #     print('date': timezone.now())
    #     return {'date': timezone.now()}


@admin.register(models.BotUser)
class BotUserAdmin(admin.ModelAdmin):
    fields = ('user_id', 'name', 'initial_date', 'last_date', 'counter')
    readonly_fields = ('name', 'user_id', 'initial_date', 'last_date')
