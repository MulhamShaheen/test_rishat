from django.contrib import admin
from .models import *


@admin.register(Item)
class PersonAdmin(admin.ModelAdmin):
    model = Item
    list_display = ['id', 'name', 'price']
    list_editable = ['name','price']
    list_filter = ('price',)
