from rest_framework import routers
from .viewsets.conta import ContaViewSet
from .viewsets.transacao import TransacaoViewSet


router = routers.SimpleRouter()
router.register(r'conta', ContaViewSet, basename="conta")
router.register(r'transacao', TransacaoViewSet, basename="transacao")