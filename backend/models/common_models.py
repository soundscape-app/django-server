from django.db import models


# 공통 TimeStampedModel
class TimeStampedModel(models.Model):
    created_datetime = models.DateTimeField(verbose_name="생성일시", auto_now_add=True, null=True)
    updated_datetime = models.DateTimeField(verbose_name="수정일시", auto_now=True, null=True)

    class Meta:
        abstract = True
