import requests
from rest_framework import serializers
from .models import Produto, Venda, ItemVenda

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'codigo', 'nome', 'preco']

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

        # Consulta estoque externo
        url = f"http://outra-api.com/estoque/{produto.codigo}/"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Garante que qualquer erro HTTP será levantado
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
class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaCreateSerializer(many=True)  # Relaciona os itens à venda
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  # Total da venda é somente leitura

    class Meta:
        model = Venda
        fields = ['id', 'itens', 'total', 'data']

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

            # Verificação do estoque na API externa
            url_estoque = f"http://outra-api.com/estoque/{produto.codigo}/"
            try:
                response = requests.get(url_estoque)
                response.raise_for_status()
            except requests.RequestException:
                raise serializers.ValidationError(f"Erro ao consultar estoque para o produto {produto.nome}.")

            if response.status_code != 200:
                raise serializers.ValidationError(f"Erro ao consultar estoque externo para o produto {produto.nome}.")

            dados_estoque = response.json()
            qtd_estoque = dados_estoque.get('quantidade', 0)

            if quantidade > qtd_estoque:
                raise serializers.ValidationError(
                    f"Estoque insuficiente para o produto {produto.nome}. Estoque disponível: {qtd_estoque}."
                )

            # Criação do ItemVenda
            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco  # Armazenando o preço unitário
            )

            # Atualiza o total da venda
            total += quantidade * produto.preco

            # Atualização do estoque
            nova_quantidade = qtd_estoque - quantidade
            estoque_data = {"quantidade": nova_quantidade, "produto_id": produto.codigo}
            try:
                put_response = requests.put(url_estoque, json=estoque_data)
                put_response.raise_for_status()
            except requests.RequestException:
                raise serializers.ValidationError(f"Erro ao atualizar estoque para o produto {produto.nome}.")

            if put_response.status_code != 200:
                raise serializers.ValidationError(f"Erro ao atualizar estoque para o produto {produto.nome}.")

        venda.total = total
        venda.save()

        return venda
