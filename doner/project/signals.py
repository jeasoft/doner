from datetime import datetime

from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save, post_delete
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Project, Milestone, Ticket, Log


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


@receiver(post_save, sender=Log)
def notify_related_users(sender, instance, created, **kwargs):

    ticket = instance.ticket

    # get related users ids
    users_ids = ticket.get_related_users_ids()

    if instance.author.id in users_ids:
        # remove author id
        users_ids.remove(instance.author.id)

    if not users_ids:
        return

    # get email
    User = get_user_model()
    emails = User.objects.filter(id__in=users_ids).values_list('email', flat=True)

    if instance.ltype == 2:
        # new comment
        template = 'project/comment_notification.txt'
    else:
        # ticket update
        template = 'project/ticket_notification.txt'

    msg_body = get_template(template).render(
        Context({
            'msg': instance.description,
            'author': instance.author,
            'host': settings.SITE_URL,
            'ticket_title': ticket.title,
            'ticket_url': ticket.get_absolute_url()
        })
    )

    ready_emails = []
    for email in emails:
        ready_emails.append(
            (
                _(u'[update] %s' % ticket.title),
                u'%s' % msg_body,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            ),
        )
    send_mass_mail(ready_emails)


@receiver(post_save, sender=Ticket)
def notify_about_new_ticket(sender, instance, created, **kwargs):
    if not created:
        return

    members_emails = instance.project.members.all().values_list('email', flat=True).exclude(id__in=[instance.submitter_id])

    if not members_emails:
        return

    ticket_assigned_to = '-'
    if instance.assigned_to:
        ticket_assigned_to = instance.assigned_to

    msg_body = get_template('project/new_ticket_notification.txt').render(
        Context({
            'ticket_submitter': instance.submitter,
            'ticket_assigned_to': ticket_assigned_to,
            'ticket_title': instance.title,
            'ticket_priority': instance.get_priority_display(),
            'ticket_status': instance.get_status_display(),
            'ticket_type': instance.get_ttype_display(),
            'ticket_description': instance.description,
            'host': settings.SITE_URL,
            'ticket_url': instance.get_absolute_url(),
        })
    )

    ready_emails = []
    for email in members_emails:
        ready_emails.append(
            (
                _(u'[new ticket] %s' % instance.title),
                u'%s' % msg_body,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            ),
        )
    send_mass_mail(ready_emails)
