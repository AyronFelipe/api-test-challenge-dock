import pytest
from ..models.conta import Conta
from ..models.transacao import Transacao
from rest_framework.exceptions import PermissionDenied


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_criar_transacao(conta: Conta):

    Transacao.objects.create(
        idConta=conta,
        valor="500.00",
        tipo=Transacao.TipoTransacao.SAQUE,
    )

    assert Transacao.objects.count() == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.parametrize(
    "valor, saldo", [
        (100.0, 1400.0),
        (500.0, 1000.0),
    ]
)
def test_transacao_sacar(conta: Conta, valor: float, saldo: float):

    temp: Conta = Transacao.operacaoSaque(conta, valor)
    assert temp.saldo == saldo


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transacao_sacar_alem_limite(conta: Conta):

    with pytest.raises(PermissionDenied) as e:
        Transacao.operacaoSaque(conta, 1000.0)
    assert "Esse valor ultrapassa o limite de saque diário!" in str(e.value)
