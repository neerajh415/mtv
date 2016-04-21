from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils.translation import ugettext_lazy as _

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email Id"), max_length=254, unique=True )
    first_name = models.CharField(_('First Name'), max_length=255, blank=True)
    middle_name = models.CharField(_('Middle Name'), max_length=255, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=255, blank=True)
    birth_date = models.DateField(_('Date of Birth'), null=True, blank=True)
    USERNAME_FIELD = 'email'







