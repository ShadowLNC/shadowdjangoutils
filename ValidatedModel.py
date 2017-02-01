from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _

class ValidatedModel(models.Model):
    def save(self, *args, **kwargs):

        #try clean and check errors
        self.errs = {}
        self.clean()
        if self.errs != {}: raise ValidationError(errs)

        #if no errs, then continue
        super(ValidatedModel, self).save(*args, **kwargs)

    def addErr(text, field=None, code=None, params=None, errs=None):
        #if we don't have an errs dict, just throw the ValidationError,
        #since save() wasn't called and didn't set/won't check self.errs
        error = ValidationError(_(text), code=code, params=params)
        if errs is None and not hasattr(self, "errs"): raise error
        
        errs = errs or self.errs #fallback
        field = field or NON_FIELD_ERRORS #None/""
        errs.setdefault(field, []).append(error)

    class Meta:
        abstract = True
