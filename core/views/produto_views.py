from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import Produto
from ..serializers import ProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    # Método GET - Listar todos os produtos
    def list(self, request):
        produtos = Produto.objects.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)

    # Método GET - Detalhar um produto específico
    def retrieve(self, request, pk=None):
        produto = Produto.objects.get(pk=pk)
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)

    # Método POST - Criar um novo produto
    def create(self, request):
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Método PUT - Atualizar um produto
    def update(self, request, pk=None):
        produto = Produto.objects.get(pk=pk)
        serializer = ProdutoSerializer(produto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Método DELETE - Excluir um produto
    def destroy(self, request, pk=None):
        produto = Produto.objects.get(pk=pk)
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
