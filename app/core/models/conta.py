from rest_framework import exceptions
from django.db import models

from ..mixins.data_criacao_mixin import DataCriacaoMixin
from .pessoa import Pessoa


class Conta(DataCriacaoMixin):
    class TipoConta(models.IntegerChoices):
        CONTA_CORRENTE = 1, "Conta Corrente"
        CONTA_POUPANCA = 2, "Conta Poupança"
        CONTA_PAGAMENTO = 3, "Conta Pagamento"
        CONTA_SALARIO = 4, "Conta Salário"

    idConta = models.AutoField(primary_key=True)
    idPessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    saldo = models.DecimalField(
        verbose_name="Saldo",
        max_digits=9,
        decimal_places=2,
        default=0,
    )
    limiteSaqueDiario = models.DecimalField(
        verbose_name="Limite de Saque Diário",
        max_digits=9,
        decimal_places=2,
    )
    flagAtivo = models.BooleanField(verbose_name="Ativo", default=True)
    tipoConta = models.IntegerField(
        verbose_name="Tipo de Conta", choices=TipoConta.choices
    )

    class Meta:
        app_label = "core"
        verbose_name = "Conta"
        verbose_name_plural = "Contas"
        unique_together = [["idPessoa", "tipoConta"]]

    def __str__(self) -> str:
        ativa = "Ativa" if self.flagAtivo else "Desativa"
        return f"{self.idConta} - {self.TipoConta(self.tipoConta).label}, {ativa}"

    def depositarConta(self, valor: float) -> "Conta":
        """
        Método que realiza soma de um determinado valor ao saldo atual da conta
        """
        if self.flagAtivo and valor >= 0:
            self.saldo = self.saldo + valor
            self.save()
            return self

    def sacarConta(self, valor: float) -> "Conta":
        """
        Mátodo que realiza a subtração de um determinado valor do saldo atual da conta
        """
        if self.flagAtivo and valor >= 0:
            if self.saldo < valor:
                raise exceptions.PermissionDenied(detail="Saldo insuficiente")
            self.saldo = self.saldo - valor
            self.save()
            return self
