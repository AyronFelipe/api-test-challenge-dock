from django.db import models
from datetime import date
from ..models.conta import Conta
from rest_framework import exceptions
from decimal import Decimal


class Transacao(models.Model):
    class TipoTransacao(models.IntegerChoices):
        SAQUE = 1, "Saque"
        DEPOSITO = 2, "Depósito"

    idTransacao = models.AutoField(primary_key=True)
    idConta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    valor = models.DecimalField(verbose_name="Valor", max_digits=9, decimal_places=2,)
    dataTransacao = models.DateTimeField(verbose_name="Data da Transação", auto_now_add=True, editable=False)
    tipo = models.IntegerField(choices=TipoTransacao.choices, blank=True, null=True)

    class Meta:
        app_label = "core"
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self) -> str:
        return f"{self.idTransacao} - {self.TipoTransacao(self.tipo).label} - {self.valor}, {self.dataTransacao}"

    @staticmethod
    def operacaoSaque(conta: Conta, valor: float) -> "Conta":

        totalSaqueDia: Decimal = 0.0
        limiteSaqueDiario = float(conta.limiteSaqueDiario)
        if valor > limiteSaqueDiario:
            raise exceptions.PermissionDenied(
                detail="Esse valor ultrapassa o limite de saque diário!"
            )
        transacoes = Transacao.objects.filter(
            idConta=conta,
            dataTransacao__date=date.today(),
            tipo=Transacao.TipoTransacao.SAQUE,
        )
        for temp_transacao in transacoes:
            totalSaqueDia = Decimal(totalSaqueDia) + temp_transacao.valor
        temp: Decimal = Decimal(totalSaqueDia) + Decimal(valor)
        if temp > limiteSaqueDiario:
            detail: str = f"Limite de saque diário alcançado. Limite disponível: { temp - limiteSaqueDiario }"
            raise exceptions.PermissionDenied(
                detail=detail
            )
        conta.sacarConta(valor)
        return conta
