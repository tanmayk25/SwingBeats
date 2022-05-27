from django.contrib import admin
from .models import Profile, Monitored_Detail

# Register your models here.
admin.site.register(Profile)
admin.site.register(Monitored_Detail)
admin.site.site_header="SwingBeats"