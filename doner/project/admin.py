from django.contrib import admin

from .models import Project, Ticket, Attachment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_private', 'created_date')
    list_filter = ('is_private', 'created_date')
    search_fields = ('name', 'description',)

admin.site.register(Project, ProjectAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'submitter', 'assigned_to', 'status', 'priority', 'ttype')
    list_filter = ('submitted_date', 'modified_date', 'status', 'priority', 'ttype')
    search_fields = ('title', 'description',)

admin.site.register(Ticket, TicketAdmin)


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

admin.site.register(Attachment, AttachmentAdmin)
