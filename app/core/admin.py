from django.contrib import admin
from .models.conta import Conta
from .models.transacao import Transacao
from .models.pessoa import Pessoa


admin.site.register(Conta)

admin.site.register(Transacao)

admin.site.register(Pessoa)
