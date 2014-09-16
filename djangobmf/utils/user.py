from django.apps import apps

from djangobmf.settings import CONTRIB_EMPLOYEE
from djangobmf.settings import CONTRIB_TEAM


def bmfuser(user):

    if not hasattr(user, 'djangobmf_employee'):
        try:
            employee = apps.get_model(CONTRIB_EMPLOYEE)
            try:
                setattr(
                    user,
                    'djangobmf_employee',
                    employee.objects.get(user=user)
                )
            except employee.DoesNotExist:
                setattr(user, 'djangobmf_employee', None)

            setattr(user, 'djangobmf_has_employee', True)

        except LookupError:
            setattr(user, 'djangobmf_employee', None)
            setattr(user, 'djangobmf_has_employee', False)

    if not hasattr(user, 'djangobmf_teams'):
        try:
            teams = apps.get_model(CONTRIB_TEAM)
            setattr(
                user,
                'djangobmf_teams',
                teams.objects.filter(members=getattr(user, 'djangobmf_employee')).values_list("id", flat=True),
            )
        except LookupError:
            setattr(user, 'djangobmf_teams', [])
