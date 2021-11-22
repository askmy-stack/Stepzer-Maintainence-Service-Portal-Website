from django.contrib import admin
from home.models import employe, members, schedule,transactions
# # Register your models here.
admin.site.register(members)
admin.site.register(transactions)
admin.site.register(employe)
admin.site.register(schedule)


