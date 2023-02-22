from django.contrib import admin
from .models import OfficeUser
from .models import Album
from .models import Link
from .models import count,log,Story

# Register your models here.
admin.site.register(OfficeUser)
admin.site.register(Album)
admin.site.register(Link)
admin.site.register(count)
admin.site.register(log)
admin.site.register(Story)