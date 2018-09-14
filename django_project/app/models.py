from django.db import models


class AccessRequest(models.Model):
    USER_TYPE = (
        ('client', 'client'),
        ('manager', 'manager'),
    )

    ACCESS_TYPE = (
        ('yes', 'yes'),
        ('no', 'no'),
        ('empty', 'empty'),
    )

    space_name = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=USER_TYPE, default=u"client")
    access = models.CharField(max_length=50, choices=ACCESS_TYPE, default=u"empty")

    class Meta:
        verbose_name = "AccessRequest"
        verbose_name_plural = "AccessRequest"

    def __str__(self):
        return '%s %s %s' % (self.name, self.type, self.access)

