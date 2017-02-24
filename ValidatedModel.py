from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _

# Custom model validation in the clean() method; this is the boilerplate code.
class ValidatedModel(models.Model):
    def save(self, *args, **kwargs):
        # Try to clean and check errors.
        # In case errs already exists, do not overwrite. See addErr().
        if not hasattr(self, 'errs'): self.errs = {}
        self.clean()

        # After cleaning, either raise the errors or else continue with save.
        if self.errs != {}: raise ValidationError(errs)
        super(ValidatedModel, self).save(*args, **kwargs)

    def addErr(self, text, field=NON_FIELD_ERRORS, code=None, params=None):
        # In case someone calls this method without save(), we create the errs
        # dict, up to them to call save() eventually.
        if not hasattr(self, 'errs'): self.errs = {}

        # This isn't about raising individual ValidationErrors; you can do that
        # elsewhere if you want; it's a single line of code.
        error = ValidationError(_(text), code=code, params=params)
        errs.setdefault(field, []).append(error)

    class Meta:
        abstract = True
