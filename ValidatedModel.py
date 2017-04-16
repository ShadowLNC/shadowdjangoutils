from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _


# Custom model validation in the clean() method; this is the boilerplate code.
class ValidatedModel(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errs = {}  # For addErr() calls without calling save().

    def save(self, extra_errs=None, *args, **kwargs):
        # Try to clean, then check errors. We aallow pre-existing errors to be
        # raised. Specify extra_errs=<self_object>.errs in order to carry over
        # previous errors when saving, instead of clearing the slate (default).
        if extra_errs is None:
            extra_errs = {}
        self.errs = extra_errs
        self.full_clean()

        # After cleaning, either raise the errors or else continue with save.
        if self.errs != {}:
            raise ValidationError(self.errs)
        super().save(*args, **kwargs)

    def addErr(self, text, field=NON_FIELD_ERRORS, code=None, params=None):
        # This isn't about raising individual ValidationErrors; you can do that
        # elsewhere if you want; it's a single line of code.
        error = ValidationError(_(text), code=code, params=params)
        self.errs.setdefault(field, []).append(error)

    class Meta:
        abstract = True
