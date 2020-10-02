from django.db import models
from accounts.models import *
from django.template.defaultfilters import slugify
from django.utils.text import slugify

class Application(models.Model):
    app_id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(CustomUser, verbose_name="Provider", on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(max_length=300, default="")
    subject = models.CharField(max_length=300, default="")
    department = models.ForeignKey('accounts.Department', verbose_name="Department", on_delete=models.CASCADE, blank=True,
                                   null=True)

    # atteched_pdf = models.FileField(upload_to=get_note_path,
    #                                validators=[FileExtensionValidator(["pdf"])],
    #                                null=True, blank=True, default=None)

    current_step = models.IntegerField(default="0")
    is_approved = models.BooleanField(default=False)
    def __unicode__(self):
        return str(self.note_id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Application, self).save(*args, **kwargs)