import tkinter as tk
from tkinter import messagebox, simpledialog
from sistema_vendas import SistemaVendas

class VendaInterface:
    def __init__(self, root, sistema_vendas):
        self.root = root
        self.root.title("Sistema de Vendas")

        self.sistema_vendas = sistema_vendas
        self.carrinho = []

        # Componentes para a tela de vendas
        self.label_produto_id = tk.Label(self.root, text="ID do Produto:")
        self.label_produto_id.grid(row=0, column=0, padx=5, pady=5)
        
        self.entry_produto_id = tk.Entry(self.root)
        self.entry_produto_id.grid(row=0, column=1, padx=5, pady=5)

        self.button_buscar_produto = tk.Button(self.root, text="Buscar Produto", command=self.buscar_produto)
        self.button_buscar_produto.grid(row=0, column=2, padx=5, pady=5)

        self.label_produto_info = tk.Label(self.root, text="Informações do Produto:")
        self.label_produto_info.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.button_adicionar_carrinho = tk.Button(self.root, text="Adicionar ao Carrinho", command=self.adicionar_carrinho)
        self.button_adicionar_carrinho.grid(row=2, column=0, columnspan=3, pady=10)

        self.label_carrinho = tk.Label(self.root, text="Carrinho de Compras:")
        self.label_carrinho.grid(row=3, column=0, columnspan=3, pady=5)

        self.text_carrinho = tk.Text(self.root, height=5, width=40)
        self.text_carrinho.grid(row=4, column=0, columnspan=3, pady=5)

        self.button_finalizar_compra = tk.Button(self.root, text="Finalizar Compra", command=self.finalizar_compra)
        self.button_finalizar_compra.grid(row=5, column=0, columnspan=3, pady=10)

    def buscar_produto(self):
        produto_id = self.entry_produto_id.get()

        if not produto_id:
            messagebox.showwarning("Campo Vazio", "Por favor, insira o ID do produto.")
            return

        try:
            produto_id = int(produto_id)
        except ValueError:
            messagebox.showwarning("ID Inválido", "O ID do produto deve ser um número inteiro.")
            return

        produto = self.sistema_vendas.obter_produto_por_id(produto_id)

        if produto:
            self.label_produto_info.config(text=f"Informações do Produto: ID: {produto[0]}, Nome: {produto[1]}, Estoque: {produto[2]}, Preço: {produto[4]:.2f}")
        else:
            messagebox.showwarning("Produto não Encontrado", "Produto não encontrado.")

    def adicionar_carrinho(self):
        produto_id = self.entry_produto_id.get()

        if not produto_id:
            messagebox.showwarning("Campo Vazio", "Por favor, insira o ID do produto.")
            return

        try:
            produto_id = int(produto_id)
        except ValueError:
            messagebox.showwarning("ID Inválido", "O ID do produto deve ser um número inteiro.")
            return

        produto = self.sistema_vendas.obter_produto_por_id(produto_id)

        if produto:
            self.carrinho.append(produto)
            self.atualizar_carrinho()
            messagebox.showinfo("Produto Adicionado", "Produto adicionado ao carrinho.")
        else:
            messagebox.showwarning("Produto não Encontrado", "Produto não encontrado.")

    def finalizar_compra(self):
        if not self.carrinho:
            messagebox.showwarning("Carrinho Vazio", "O carrinho está vazio. Adicione produtos antes de finalizar a compra.")
            return

        cliente_nome = simpledialog.askstring("Dados do Cliente", "Nome do Cliente:")
        
        if cliente_nome:
            self.sistema_vendas.realizar_venda(cliente_nome, self.carrinho)
            messagebox.showinfo("Venda Finalizada", "Venda realizada com sucesso!")
            self.carrinho = []  # Limpar o carrinho após a compra
            self.atualizar_carrinho()

    def atualizar_carrinho(self):
        self.text_carrinho.delete(1.0, tk.END)  # Limpar o texto atual no carrinho
        for produto in self.carrinho:
            self.text_carrinho.insert(tk.END, f"ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[4]:.2f}\n")

if __name__ == "__main__":
    root = tk.Tk()
    sistema_vendas = SistemaVendas()
    venda_interface = VendaInterface(root, sistema_vendas)
    root.mainloop()
