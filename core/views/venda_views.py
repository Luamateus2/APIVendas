from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Venda
from ..serializers import VendaSerializer, VendaCreateSerializer

class VendaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

    def list(self, request):
        vendas = Venda.objects.all()
        serializer = VendaSerializer(vendas, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        venda = Venda.objects.get(pk=pk)
        serializer = VendaSerializer(venda)
        return Response(serializer.data)

    def create(self, request):
        serializer = VendaCreateSerializer(data=request.data)
        if serializer.is_valid():
            venda = serializer.save() 
            return Response(VendaSerializer(venda).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        venda = Venda.objects.get(pk=pk)
        serializer = VendaSerializer(venda, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        venda = Venda.objects.get(pk=pk)
        venda.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
