from rest_framework import serializers
from ..models.transacao import Transacao


class TransacaoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transacao
        fields = ["idConta", "valor"]


class TransacaoSerializer(serializers.ModelSerializer):

    tipo = serializers.SerializerMethodField()

    class Meta:
        model = Transacao
        fields = ["idTransacao", "idConta", "valor", "dataTransacao", "tipo"]

    def get_tipo(self, obj: Transacao) -> str:

        return obj.TipoTransacao(obj.tipo).label
