from django.db import models


class DataCriacaoMixin(models.Model):

    dataCriacao = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True
