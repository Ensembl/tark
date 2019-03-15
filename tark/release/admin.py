from django.contrib import admin
from release.models import TranscriptReleaseTagRelationship,\
    TranscriptReleaseTagRelationshipAdmin

# Register your models here.
admin.site.register(TranscriptReleaseTagRelationship, TranscriptReleaseTagRelationshipAdmin)
