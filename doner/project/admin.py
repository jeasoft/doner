from django.contrib import admin

from .models import Project, Milestone, Ticket, Attachment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_private', 'last_active', 'created_date')
    list_filter = ('is_private', 'created_date', 'last_active')
    search_fields = ('name', 'description')

admin.site.register(Project, ProjectAdmin)


class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'deadline')
    list_filter = ('project',)
    search_fields = ('name', 'description')

admin.site.register(Milestone, MilestoneAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'submitter', 'assigned_to', 'status', 'priority', 'ttype')
    list_filter = ('project', 'submitted_date', 'modified_date', 'status', 'priority', 'ttype')
    search_fields = ('title', 'description')

admin.site.register(Ticket, TicketAdmin)


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

admin.site.register(Attachment, AttachmentAdmin)
