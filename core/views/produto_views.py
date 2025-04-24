from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Produto
from ..serializers import ProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def list(self, request):
        produtos = Produto.objects.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        produto = Produto.objects.get(pk=pk)
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        produto = Produto.objects.get(pk=pk)
        serializer = ProdutoSerializer(produto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        produto = Produto.objects.get(pk=pk)
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
