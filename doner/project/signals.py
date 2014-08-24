from datetime import datetime

from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save, post_delete

from .models import Project, Milestone, Ticket


@receiver(m2m_changed, sender=Project.members.through)
def count_project_members(sender, instance, **kwargs):
    '''
    Count members after member add/remove.
    '''
    instance.members_number = instance.members.count()
    instance.save()


@receiver(post_save, sender=Milestone)
def set_have_milestones_if_first(sender, instance, created, **kwargs):
    '''
    If the first milestone is created set the project's milestone flag on True.
    '''
    if created and not instance.project.have_milestones:
        instance.project.have_milestones = True
        instance.project.save()


@receiver(post_delete, sender=Milestone)
def set_have_milestones_if_last(sender, instance, **kwargs):
    '''
    If the last milestone is removed set the project's milestone flag on False.
    '''
    if not instance.project.milestone_set.exists():
        instance.project.have_milestones = False
        instance.project.save()


@receiver(post_save, sender=Ticket)
@receiver(post_delete, sender=Ticket)
def update_project_last_active(sender, instance, **kwargs):
    '''
    If the first milestone is created set the project's milestone flag on True.
    '''
    instance.project.last_active = datetime.now()
    instance.project.save()
