from rest_framework import serializers
from ..models.conta import Conta


class SaldoContaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conta
        fields = ["saldo"]