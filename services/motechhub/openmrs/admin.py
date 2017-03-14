from django.contrib import admin
from openmrs.concepts.models import OpenmrsConcept
from openmrs.credentials.models import OpenmrsInstance, OpenmrsCredential


class OpenmrsInstanceAdmin(admin.ModelAdmin):
    pass


class OpenmrsCredentialAdmin(admin.ModelAdmin):
    pass


class OpenmrsConceptAdmin(admin.ModelAdmin):
    pass


admin.site.register(OpenmrsInstance, OpenmrsInstanceAdmin)
admin.site.register(OpenmrsCredential, OpenmrsCredentialAdmin)
admin.site.register(OpenmrsConcept, OpenmrsConceptAdmin)
