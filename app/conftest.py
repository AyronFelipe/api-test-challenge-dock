import pytest
from core.models import Pessoa
from core.models import Conta
from rest_framework.test import APIClient


@pytest.fixture
def pessoa(db):

    pessoa = Pessoa.objects.create(
        nome="Benedita Lívia Martins",
        cpf="18088451701",
        dataNascimento="1997-09-29",
    )
    return pessoa


@pytest.fixture
def conta(pessoa):

    conta = Conta.objects.create(
        idPessoa=pessoa,
        saldo=1500.0,
        limiteSaqueDiario="700",
        flagAtivo=True,
        tipoConta=Conta.TipoConta.CONTA_CORRENTE,
    )
    return conta


@pytest.fixture
def api_client():

    return APIClient()
