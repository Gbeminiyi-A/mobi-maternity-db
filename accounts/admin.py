from django.contrib import admin
from .models import UserRegistration, HealthInfo, HealthWorkerInfo, Consultation

# Register your models here.
admin.site.register(UserRegistration)


class HealthInfoAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Show health info only for patients
        return qs.filter(user__userregistration__role='P')


admin.site.register(HealthInfo, HealthInfoAdmin)


class HealthCareInfoAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Show health care info only for doctors
        return qs.filter(user__userregistration__role='H')

    list_display = ('user', 'specialty')


admin.site.register(HealthWorkerInfo, HealthCareInfoAdmin)


admin.site.register(Consultation)
