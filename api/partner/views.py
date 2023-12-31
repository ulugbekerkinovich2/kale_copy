from django.db.models import Q
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView

from api.paginator import CustomPagination
from api.partner.serializers import PartnerCreateSerializer, PartnerListSerializer, PartnerDetailSerializer
from api.permissions import IsAdmin
from common.partner.models import Partner


class PartnerCreateAPIView(CreateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerCreateSerializer
    permission_classes = [IsAdmin]


class PartnerListAPIView(ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        others = self.request.query_params.get('others')
        guid = self.request.query_params.get('guid')
        if others and guid:
            try:
                queryset = queryset.exclude(guid=guid)
            except:
                pass
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class PartnerDetailAPIView(RetrieveAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerDetailSerializer
    lookup_field = 'guid'


class PartnerUpdateAPIView(UpdateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'


class PartnerDeleteAPIView(DestroyAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
