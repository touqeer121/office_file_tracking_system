from django.core.validators import FileExtensionValidator
from django.db import models
from accounts.models import CustomUser
from django.template.defaultfilters import slugify
from django.utils.text import slugify

def get_pdf_path(instance, filename):
    return 'Attached_files/{0}/pdf/{1}'.format(instance.app_id, filename)


class Application_Count(models.Model):
    app_cnt = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.app_cnt)


class Scholarship(models.Model):
    name = models.CharField(max_length=255, default='')
    # slug = models.SlugField(max_length=30, unique=True, editable=False)
    abbreviation = models.CharField(max_length=10, default='')
    department = models.ForeignKey('accounts.Department', verbose_name="Department", on_delete=models.CASCADE, blank=True,
                                   null=True)
    receiver_authority_id = models.IntegerField(default=1)
    requirements_info = models.TextField(default='Requirement information needs to be updated.')
    max_step = models.IntegerField(default="1")

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         slug = slugify(self.name)
    #         while True:
    #             try:
    #                 Scholarship = Scholarship.objects.get(slug=slug)
    #                 if Scholarship == self:
    #                     self.slug = slug
    #                     break
    #                 else:
    #                     slug = slug + '_'
    #             except:
    #                 self.slug = slug
    #                 break
    #     super(Scholarship, self).save()

    def __str__(self):
        return self.name


class Application(models.Model):
    app_id = models.CharField(max_length=20, primary_key=True)
    request = models.ForeignKey(Scholarship, verbose_name="Request", on_delete=models.CASCADE,default=1)
    applicant = models.ForeignKey(CustomUser, verbose_name="Applicant", on_delete=models.CASCADE,default=1)
    category = models.CharField(max_length=300, default="")
    title = models.CharField(max_length=300, default="")
    department = models.ForeignKey('accounts.Department', verbose_name="Department", on_delete=models.CASCADE, blank=True,
                                   null=True)

    attached_pdf = models.FileField(upload_to=get_pdf_path,
                                   validators=[FileExtensionValidator(["pdf"])],
                                   null=True, blank=True, default=None)

    current_authority = models.IntegerField(max_length=300, default="")
    current_step = models.IntegerField(default="0")
    max_step = models.IntegerField(default="1")
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    def __unicode__(self):
        return str(self.app_id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Application, self).save(*args, **kwargs)


