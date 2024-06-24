from django.contrib import admin
from .models import Hastalar, Doktorlar, Randevular

admin.site.register(Hastalar)
admin.site.register(Doktorlar)
admin.site.register(Randevular)
