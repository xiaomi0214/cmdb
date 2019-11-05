from django.contrib import admin

# Register your models here.
from cmdb.models import *

class peopleAdmin(admin.ModelAdmin):
    list_display = ( 'nichen','passwd',)         ### 如图展示数据（元组）
    search_fields = ('nichen',)

class serverAdmin(admin.ModelAdmin):
    list_display = ( 'ipv4','cpu_jg','czxt','localtion','admin','application','use_people')         ### 如图展示数据（元组）
    search_fields = ('ipv4','cpu_jg')


admin.site.register(People, peopleAdmin)
admin.site.register(Server, serverAdmin)

