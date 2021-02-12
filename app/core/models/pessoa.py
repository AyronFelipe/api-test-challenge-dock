from django.db import models

from ..mixins.data_criacao_mixin import DataCriacaoMixin


class Pessoa(DataCriacaoMixin):

    idPessoa = models.AutoField(primary_key=True)
    nome = models.CharField(verbose_name="Nome", max_length=200)
    cpf = models.CharField(verbose_name="CPF", max_length=11, unique=True)
    dataNascimento = models.DateField(verbose_name="Data de Nascimento")

    class Meta:
        app_label = "core"
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

    def __str__(self) -> str:
        return f"{self.nome} - {self.cpf}"
