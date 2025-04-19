from django.db import models

class Produto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)  # novo campo
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"



class Venda(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    produtos = models.ManyToManyField(Produto, through='ItemVenda')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venda #{self.id} - {self.data.strftime('%d/%m/%Y %H:%M')}"


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} na Venda #{self.venda.id}"
