from ..models.conta import Conta
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from ..serializers.conta import CreateContaSerializer, ContaSerializer
from ..serializers.transacao import TransacaoSerializer
from ..serializers.saldo import SaldoContaSerializer
from rest_framework import status, exceptions
from django.db import transaction
from datetime import date


class ContaViewSet(viewsets.ViewSet):
    def create(self, request):
        """
        Endpoint de criação de contas
        """
        serializer = CreateContaSerializer(data=request.data)
        with transaction.atomic():
            if serializer.is_valid():
                instance = serializer.validated_data
                conta: Conta = Conta.objects.create(
                    idPessoa=instance.get("idPessoa"),
                    saldo=instance.get("saldo"),
                    limiteSaqueDiario=instance.get("limiteSaqueDiario"),
                    tipoConta=instance.get("tipoConta"),
                )
                contaResponse = ContaSerializer(conta)
                return Response(data=contaResponse.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def saldo(self, request, pk=None):
        """
        Endpoint de consulta de saldo por conta
        """
        try:
            conta: Conta = Conta.objects.get(pk=pk)
            serializer = SaldoContaSerializer(conta)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Conta.DoesNotExist:
            raise exceptions.NotFound(detail="Conta não encontrada!")

    @action(methods=["patch"], detail=True)
    def acao(self, request, pk=None):
        """
        Endpoint para bloqueio e desbloqueio de conta
        """
        try:
            conta: Conta = Conta.objects.get(pk=pk)
            conta.flagAtivo = not conta.flagAtivo
            conta.save()
            serializer = ContaSerializer(conta)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Conta.DoesNotExist:
            raise exceptions.NotFound(detail="Conta não encontrada!")

    @action(detail=True)
    def extrato(self, request, pk=None):
        """
        Endpoint para extrato de todas as transações
        """
        try:
            conta: Conta = Conta.objects.get(pk=pk)
            transacoes = conta.transacao_set.all()
            serializer = TransacaoSerializer(transacoes, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Conta.DoesNotExist:
            raise exceptions.NotFound(detail="Conta não encontrada!")

    @action(methods=["post"], detail=True, url_path="extrato-por-periodo")
    def extrato_por_periodo(self, request, pk=None):
        """
        Endpoint para extrato de todas as transações
        """
        try:
            date_request = request.data.get("date", None)
            if not date_request:
                raise exceptions.ValidationError(
                    detail="A data não pode ficar em branco!"
                )
            isoDate = date.fromisoformat(date_request)
            if isoDate > date.today():
                raise exceptions.ValidationError(
                    detail="A data não pode ser maior que a data de hoje!"
                )
            conta: Conta = Conta.objects.get(pk=pk)
            transacoes = conta.transacao_set.filter(
                dataTransacao__date__gte=isoDate,
                dataTransacao__date__lte=date.today()
            )
            serializer = TransacaoSerializer(transacoes, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Conta.DoesNotExist:
            raise exceptions.NotFound(detail="Conta não encontrada!")
