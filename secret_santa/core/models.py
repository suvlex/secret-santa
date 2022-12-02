import hashlib

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from model_utils import FieldTracker
from random import choice
from templated_email import send_templated_mail


class User(AbstractUser):
    dob = models.DateField(verbose_name="Date of birth", null=True, blank=True)

    @property
    def name(self):
        first_name = self.first_name
        last_name = self.last_name

        if first_name and last_name:
            return f"{first_name} {last_name}"
        elif first_name:
            return first_name
        elif last_name:
            return last_name
        return self.email

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255)

    def __str__(self) -> str:
        return self.name


class Member(models.Model):
    team = models.ForeignKey(Team, related_name="members", on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Name', max_length=255, null=True, blank=True)
    email_address = models.EmailField("Email address")
    email_address_tracker = FieldTracker(fields=['email_address'])
    hashed_email = models.CharField("Hashed recipient's email", max_length=32, null=True, blank=True)

    colleagues = models.ManyToManyField("self", blank=True)

    def save(self, *kwargs) -> None:
        if self.pk is None or (self.email_address_tracker.changed() and self.user is None):
            self.hashed_email = self.get_hashed_email()

        if self.name or self.user:
            super().save(*kwargs)
        else:
            raise ValidationError('The member must have a name or connection to the user')

    def __str__(self) -> str:
        return self.name or self.user.name

    def get_hashed_email(self):
        return hashlib.md5((self.email + settings.HASH_SALT).encode('utf-8')).hexdigest()

    @property
    def email(self) -> str:
        user = self.user
        return user.email if user else self.email_address

    @property
    def full_name(self) -> str:
        user = self.user
        return user.name if user else self.name

def mailing(santa, recipient_name) -> None:
    try:
        send_templated_mail(
            template_name='your_ward.email',
            recipient_list=[santa.email],
            from_email=settings.TEMPLATED_EMAIL_FROM_EMAIL,
            context=dict(recipient_name=recipient_name)
        )
    except Exception:
        pass


class Celebration(models.Model):
    team = models.ForeignKey(Team, verbose_name="The team celebrating the new year", on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(verbose_name="Next year")

    def __str__(self) -> str:
        return f'{self.team} in {self.year}'

    class Meta:
        unique_together = ["team", "year"]
        ordering = ["year"]

    def save(self, **kwargs) -> None:
        specified_year = self.year
        current_year = timezone.now().year

        if specified_year <= current_year:
            raise ValidationError(
                f"Enter the next year. The specified year ({specified_year}) is less than the current year" + \
                    f" ({current_year})"
            )
        return super().save(**kwargs)

    def get_colleagues_count_dict(self, colleagues_dict):
        colleagues_count_dict = dict()
        for key, value in colleagues_dict.items():
            colleagues_count_dict[key] = len(value)

        return dict(sorted(colleagues_count_dict.items(), key=lambda item: item[1]))

    def check_and_run(self):
        flag = True
        while flag:
            try:
                dict_for_mailing = dict()
                list_for_create_secret_santa = list()

                colleagues_dict = dict()
                for member in self.team.members.prefetch_related("colleagues"):
                    for colleague in member.colleagues.all():
                        if member in colleagues_dict:
                            colleagues_dict[member].append(colleague)
                        else:
                            colleagues_dict[member] = [colleague]

                colleagues_count_dict = self.get_colleagues_count_dict(colleagues_dict)

                while colleagues_count_dict:
                    member = list(colleagues_count_dict.keys())[0]
                    colleague = choice(colleagues_dict[member])
                    dict_for_mailing[member] = colleague.full_name
                    list_for_create_secret_santa.append(SecretSanta(santa=member, recipient=colleague, celebration=self))

                    colleagues_dict.pop(member)
                    for key, value in colleagues_dict.items():
                        if colleague in value:
                            value.remove(colleague)
                            colleagues_dict[key] = value
                    colleagues_count_dict = self.get_colleagues_count_dict(colleagues_dict)

                SecretSanta.objects.bulk_create(list_for_create_secret_santa)

                for key, value in dict_for_mailing.items():
                    mailing(key, value)

                flag = False
            except Exception:
                pass

    def run(self):
        self.clear()
        self.check_and_run()

    def clear(self):
        self.secret_santas.all().delete()


class SecretSanta(models.Model):
    santa = models.OneToOneField(Member, verbose_name="Santa", related_name='me_santa',  on_delete=models.CASCADE)
    recipient = models.OneToOneField(
        Member, verbose_name="Recipient of a gift from Santa", related_name='my_santa', on_delete=models.CASCADE
    )
    celebration = models.ForeignKey(Celebration, related_name='secret_santas', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.santa} {self.recipient} {self.celebration}'

    class Meta:
        unique_together = ["santa", "recipient", "celebration"]

    def resend_email(self) -> None:
        mailing(self.santa, self.recipient.name)
