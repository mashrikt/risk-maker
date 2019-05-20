from rest_framework.generics import RetrieveAPIView, CreateAPIView

from risk_maker.risk.models import RiskType, Risk
from risk_maker.risk.serializers import RiskTypeSerializer, RiskSerializer


class RiskTypeRetrieveView(RetrieveAPIView):
    queryset = RiskType.objects.all()
    serializer_class = RiskTypeSerializer


class RiskCreateView(CreateAPIView):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer
