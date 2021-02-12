from django.db import transaction
from ..models.conta import Conta
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from ..serializers.transacao import TransacaoCreateSerializer
from ..serializers.conta import ContaSerializer
from ..models.transacao import Transacao
from rest_framework.response import Response



class TransacaoViewSet(viewsets.ViewSet):

    @action(methods=["post"], detail=False)
    def sacar(self, request):
        serializer = TransacaoCreateSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                instance = serializer.validated_data
                transacao: Transacao = Transacao(
                    idConta=instance.get("idConta"),
                    valor=instance.get("valor"),
                    tipo=Transacao.TipoTransacao.SAQUE
                )
                Transacao.operacaoSaque(transacao.idConta, transacao.valor)
                transacao.save()
                response = ContaSerializer(transacao.idConta)
                return Response(data=response.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False)
    def depositar(self, request):
        serializer = TransacaoCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.validated_data
            transacao: Transacao = Transacao.objects.create(
                idConta=instance.get("idConta"),
                valor=instance.get("valor"),
                tipo=Transacao.TipoTransacao.DEPOSITO
            )
            conta: Conta = transacao.idConta
            conta.depositarConta(transacao.valor)
            response = ContaSerializer(transacao.idConta)
            return Response(data=response.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
