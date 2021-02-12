import pytest
from django import urls
from rest_framework.test import APIClient

from ..models.conta import Conta
from ..models.pessoa import Pessoa
from ..models.transacao import Transacao
from datetime import datetime, timedelta


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_criar_conta(pessoa: Pessoa):

    Conta.objects.create(
        idPessoa=pessoa,
        saldo="1500",
        limiteSaqueDiario="700",
        flagAtivo=True,
        tipoConta=Conta.TipoConta.CONTA_CORRENTE
    )

    assert Conta.objects.count() == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_conta_deposito(conta: Conta):

    valor: float = 1000.0
    conta.depositarConta(valor)
    assert conta.saldo == 2500.0


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_conta_saque(conta: Conta):

    valor: float = 1000.0
    conta.sacarConta(valor)
    assert conta.saldo == 500.0


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_api_criar_conta(api_client: APIClient, pessoa: Pessoa):

    url = urls.reverse("conta-list")
    data = {
        "idPessoa": pessoa.pk,
        "saldo": 1500.0,
        "limiteSaqueDiario": 500.0 ,
        "tipoConta": Conta.TipoConta.CONTA_CORRENTE,
    }
    response = api_client.post(url, data=data)
    assert response.status_code == 201
    assert Conta.objects.count() == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_api_saldo_conta(api_client: APIClient, conta: Conta):

    url = urls.reverse("conta-saldo", args=[conta.pk])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data.get("saldo") == "1500.00"

    url = urls.reverse("conta-saldo", args=[100])
    response = api_client.get(url)
    assert response.status_code == 404
    assert response.data.get("detail") == "Conta não encontrada!"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_api_acao_conta(api_client: APIClient, conta: Conta):

    url = urls.reverse("conta-acao", args=[conta.pk])
    response = api_client.patch(url)
    assert response.status_code == 200
    assert conta.flagAtivo == True

    url = urls.reverse("conta-acao", args=[100])
    response = api_client.patch(url)
    assert response.status_code == 404
    assert response.data.get("detail") == "Conta não encontrada!"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_api_extrato_conta(api_client: APIClient, conta: Conta):

    url = urls.reverse("conta-extrato", args=[conta.pk])
    Transacao.objects.create(
        idConta=conta,
        valor="1500.00",
        dataTransacao=datetime.today(),
        tipo=Transacao.TipoTransacao.DEPOSITO,
    )
    Transacao.objects.create(
        idConta=conta,
        valor="2500.00",
        dataTransacao=datetime.today(),
        tipo=Transacao.TipoTransacao.DEPOSITO,
    )
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.parametrize(
    "date, status", [
        ("", 400),
        ("2021-02-12", 200),
        ("2021-02-11", 200),
    ]
)
def test_api_extrato_por_periodo_conta(
    api_client: APIClient,
    conta: Conta,
    date: str,
    status: int
):

    url = urls.reverse("conta-extrato-por-periodo", args=[conta.pk])
    Transacao.objects.create(
        idConta=conta,
        valor="1500.00",
        tipo=Transacao.TipoTransacao.DEPOSITO,
    )
    Transacao.objects.create(
        idConta=conta,
        valor="2500.00",
        tipo=Transacao.TipoTransacao.DEPOSITO,
    )
    data = {
        "date": date
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.parametrize(
    "valor, saldo", [
        (400.0, 1900.0),
        (500.0, 2000.0),
        (200.0, 1700.0),
    ]
)
def test_conta_depositar(conta: Conta, valor: float, saldo: float):

    temp: Conta = conta.depositarConta(valor)
    assert temp.saldo == saldo
