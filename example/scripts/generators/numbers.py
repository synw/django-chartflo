# -*- coding: utf-8 -*-

from __future__ import print_function
from django.contrib.auth.models import User
from chartflo.models import Number


def gen_numbers():
    """
    Generate individual numbers
    """
    # users
    users = User.objects.all()
    num_users = users.count()
    print("Saving users number")
    num, _ = Number.objects.get_or_create(slug="users")
    num.name = "Users"
    num.legend = "Users"
    num.value = num_users
    num.save()
    num.generate()
    # emails
    print("Saving emails number")
    num, _ = Number.objects.get_or_create(slug="emails")
    num.name = "Emails"
    num.legend = "Emails"
    emails = 0
    for user in users:
        if user.email != "":
            emails += 1
    num.value = emails
    num.save()
    num.generate()
    # names
    print("Saving names number")
    num, _ = Number.objects.get_or_create(slug="names")
    num.name = "Names"
    num.legend = "Names"
    objs = 0
    for obj in users:
        if obj.first_name != "" and obj.last_name != "":
            objs += 1
    num.value = objs
    num.save()
    num.generate()
    # staff
    print("Saving staff number")
    num, _ = Number.objects.get_or_create(slug="staff")
    num.name = "Staff"
    num.legend = num.name
    num.value = users.filter(is_staff=True).count()
    num.save()
    num.generate()
    # superusers
    print("Saving superusers number")
    num, _ = Number.objects.get_or_create(slug="superusers")
    num.name = "Superusers"
    num.legend = num.name
    num.value = users.filter(is_superuser=True).count()
    num.save()
    num.generate()
