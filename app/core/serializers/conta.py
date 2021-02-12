from django.db.models import fields
from rest_framework import serializers
from ..models.conta import Conta


class CreateContaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conta
        fields = ["idPessoa", "saldo", "limiteSaqueDiario", "tipoConta"]


class ContaSerializer(serializers.ModelSerializer):

    tipo = serializers.SerializerMethodField()

    class Meta:
        model = Conta
        fields = [
            "idConta",
            "idPessoa" ,
            "saldo",
            "limiteSaqueDiario",
            "flagAtivo",
            "dataCriacao",
            "tipo",
        ]

    def get_tipo(self, obj: Conta) -> str:

        return obj.TipoConta(obj.tipoConta).label