from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import Venda
from ..serializers import VendaSerializer, VendaCreateSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

    # Método GET - Listar todas as vendas
    def list(self, request):
        vendas = Venda.objects.all()
        serializer = VendaSerializer(vendas, many=True)
        return Response(serializer.data)

    # Método GET - Detalhar uma venda específica
    def retrieve(self, request, pk=None):
        venda = Venda.objects.get(pk=pk)
        serializer = VendaSerializer(venda)
        return Response(serializer.data)

    # Método POST - Criar uma nova venda
    def create(self, request):
        serializer = VendaCreateSerializer(data=request.data)
        if serializer.is_valid():
            venda = serializer.save()  # Cria a venda e atualiza o estoque
            return Response(VendaSerializer(venda).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Método PUT - Atualizar uma venda
    def update(self, request, pk=None):
        venda = Venda.objects.get(pk=pk)
        serializer = VendaSerializer(venda, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Método DELETE - Excluir uma venda
    def destroy(self, request, pk=None):
        venda = Venda.objects.get(pk=pk)
        venda.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
