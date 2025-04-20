import requests
from rest_framework import serializers
from .models import Produto, Venda, ItemVenda


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'codigo', 'nome', 'preco']


# Serializer para criação de itens
class ItemVendaCreateSerializer(serializers.ModelSerializer):
    produto_id = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all(), source='produto')

    class Meta:
        model = ItemVenda
        fields = ['produto_id', 'quantidade']

    def validate_quantidade(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("A quantidade deve ser um número inteiro.")
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value

    def validate(self, data):
        produto = data['produto']
        quantidade = data['quantidade']

        url = f"http://127.0.0.1:8004/estoques/codigo/{produto.codigo}/"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException:
            raise serializers.ValidationError("Erro de conexão com a API de estoque.")

        if response.status_code != 200:
            raise serializers.ValidationError("Erro ao consultar estoque externo.")

        dados_estoque = response.json()
        qtd_disponivel = dados_estoque.get('quantidade', 0)

        if quantidade > qtd_disponivel:
            raise serializers.ValidationError(
                f"Estoque insuficiente para o produto '{produto.nome}': disponível {qtd_disponivel}."
            )

        return data


# ✅ Serializer de leitura dos itens
class ItemVendaReadSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade', 'preco_unitario', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()


# ✅ Serializer de leitura da venda
class VendaSerializer(serializers.ModelSerializer):
    itens = serializers.SerializerMethodField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Venda
        fields = ['id', 'itens', 'total', 'data']

    def get_itens(self, obj):
        itens = ItemVenda.objects.filter(venda=obj)
        return ItemVendaReadSerializer(itens, many=True).data


# ✅ Serializer de criação da venda
class VendaCreateSerializer(serializers.ModelSerializer):
    itens = ItemVendaCreateSerializer(many=True)

    class Meta:
        model = Venda
        fields = ['itens']
        read_only_fields = ['total']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        venda = Venda.objects.create(total=0)

        total = 0
        for item_data in itens_data:
            produto = item_data['produto']
            quantidade = item_data['quantidade']

            # Verificação do estoque na API FastAPI
            url_get_estoque = f"http://127.0.0.1:8004/estoques/codigo/{produto.codigo}/"
            try:
                response = requests.get(url_get_estoque)
                response.raise_for_status()
            except requests.RequestException:
                raise serializers.ValidationError(f"Erro ao consultar estoque para o produto '{produto.nome}'.")

            dados_estoque = response.json()
            qtd_estoque = dados_estoque.get('quantidade', 0)

            if quantidade > qtd_estoque:
                raise serializers.ValidationError(
                    f"Estoque insuficiente para o produto '{produto.nome}'. Estoque disponível: {qtd_estoque}."
                )

            # Criação do ItemVenda
            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco
            )

            # Atualiza o total da venda
            total += quantidade * produto.preco

            # Atualização do estoque via PATCH usando o código do produto
            nova_quantidade = qtd_estoque - quantidade
            url_patch_estoque = f"http://127.0.0.1:8004/estoques/codigo/{produto.codigo}?quantidade={nova_quantidade}"

            try:
                patch_response = requests.patch(url_patch_estoque)
                patch_response.raise_for_status()
            except requests.RequestException as e:
                raise serializers.ValidationError(
                    f"Erro ao atualizar estoque para o produto '{produto.nome}'. Detalhes do erro: {e}"
                )

            if patch_response.status_code not in [200, 204]:
                raise serializers.ValidationError(
                    f"Falha ao atualizar estoque do produto '{produto.nome}'. Erro: {patch_response.status_code} - {patch_response.text}"
                )

        venda.total = total
        venda.save()
        return venda
