import random

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User

from faker import Faker

from project.models import Project, Ticket


class Command(BaseCommand):

    def handle(self, *args, **options):

        fake = Faker()

        project = Project.objects.create(
            name=fake.pystr(),
            description=fake.sentence(),
            is_private=fake.boolean(),
            created_date=fake.date(),
        )

        for i in range(30):
            Ticket.objects.create(
                project=project,
                title=fake.pystr(),
                description=fake.sentence(),
                submitted_date=fake.date(),
                submitter=User.objects.first(),
                status=random.randint(1, 3),
                priority=random.randint(1, 3),
                ttype=random.randint(1, 3),
            )
