from datetime import datetime

from django.db.models.signals import m2m_changed, post_save, post_delete

from .models import Project, Milestone, Ticket


def count_project_members(sender, instance, **kwargs):
    '''
    Count members after member add/remove.
    '''
    instance.members_number = instance.members.count()
    instance.save()

m2m_changed.connect(count_project_members, sender=Project.members.through)


def set_have_milestones_if_first(sender, instance, created, **kwargs):
    '''
    If the first milestone is created set the project's milestone flag on True.
    '''
    if created and not instance.project.have_milestones:
        instance.project.have_milestones = True
        instance.project.save()

post_save.connect(set_have_milestones_if_first, sender=Milestone)


def set_have_milestones_if_last(sender, instance, **kwargs):
    '''
    If the last milestone is removed set the project's milestone flag on False.
    '''
    if not instance.project.milestone_set.exists():
        instance.project.have_milestones = False
        instance.project.save()

post_delete.connect(set_have_milestones_if_last, sender=Milestone)


def update_project_last_active(sender, instance, **kwargs):
    '''
    If the first milestone is created set the project's milestone flag on True.
    '''
    instance.project.last_active = datetime.now()
    print('new last_active')
    instance.project.save()

post_save.connect(update_project_last_active, sender=Ticket)
post_delete.connect(update_project_last_active, sender=Ticket)
