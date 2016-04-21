from django.contrib import admin
from django.contrib.auth.models import User
from .models import *


admin.site.register(MyModel)
admin.site.register(Book)
admin.site.register(Reporter)
admin.site.register(Article)

#admin.site.register(Person)
#admin.site.register(Group)
admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Country)
admin.site.register(City)



# Register your models here.
