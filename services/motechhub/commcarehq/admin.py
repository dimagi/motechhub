from django.contrib import admin
from commcarehq.credentials.models import CommcarehqInstance, CommcarehqCredential


class CommcarehqInstanceAdmin(admin.ModelAdmin):
    pass


class CommcarehqCredentialAdmin(admin.ModelAdmin):
    pass


admin.site.register(CommcarehqInstance, CommcarehqInstanceAdmin)
admin.site.register(CommcarehqCredential, CommcarehqCredentialAdmin)
