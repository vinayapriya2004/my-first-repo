# from django.contrib import admin
# from .models import Profile

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'role', 'phone', 'specialization']
#     list_filter = ['role']



from django.contrib import admin
from .models import Profile ,PatientRegistration  

class PatientProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'age', 'gender', 'phone', 'department',
        'doctor', 'address', 'is_approved'
    )
    list_filter = ('is_approved', 'gender', 'department')
    search_fields = ('user__username', 'user__email', 'phone')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(role='patient')  # Only show patients

admin.site.register(Profile)
admin.site.register(PatientRegistration)
