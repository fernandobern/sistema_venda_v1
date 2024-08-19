import sqlite3
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('sistema_vendas.db')

# Criar tabela de produtos se não existir
conn.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    estoque INTEGER NOT NULL,
    preco_fab REAL NOT NULL,
    valor_venda REAL NOT NULL
)
''')

# Criar tabela de vendas se não existir
conn.execute('''
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_nome TEXT NOT NULL,
    cliente_telefone TEXT NOT NULL,
    data_venda TEXT NOT NULL,
    valor_total REAL NOT NULL
)
''')

# Criar tabela de vendas_produto se não existir
conn.execute('''
CREATE TABLE IF NOT EXISTS vendas_produto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (venda_id) REFERENCES vendas (id),
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
)
''')


# Criar tabela de vendas se não existir
conn.execute('''
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_nome TEXT NOT NULL,
    cliente_telefone TEXT NOT NULL,
    data_venda TEXT NOT NULL,
    valor_total REAL NOT NULL
)
''')

# ...

# Função para adicionar um novo produto ao estoque
def adicionar_produto(nome, estoque, preco_fab, valor_venda):
    conn.execute('INSERT INTO produtos (nome, estoque, preco_fab, valor_venda) VALUES (?, ?, ?, ?)',
                 (nome, estoque, preco_fab, valor_venda))
    conn.commit()

# Função para realizar uma venda
def realizar_venda(cliente_nome, cliente_telefone, carrinho):
    data_hora_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    valor_total = 0.0

    # Inserir informações do cliente na tabela de vendas
    conn.execute('INSERT INTO vendas (cliente_nome, cliente_telefone, data_venda, valor_total) VALUES (?, ?, ?, ?)',
                 (cliente_nome, cliente_telefone, data_hora_venda, valor_total))
    conn.commit()

    # Obter o ID da venda recém-inserida
    venda_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

    # Iterar sobre os itens do carrinho e registrar as vendas
    for produto_id, quantidade in carrinho:
        cursor = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
        produto = cursor.fetchone()

        if produto and produto[2] >= quantidade:
            # Calcular o valor total do produto
            valor_total_produto = quantidade * produto[4]  # quantidade * valor_venda
            valor_total += valor_total_produto

            # Registrar a venda na tabela de vendas_produto
            conn.execute('INSERT INTO vendas_produto (venda_id, produto_id, quantidade) VALUES (?, ?, ?)',
                         (venda_id, produto_id, quantidade))
            
            # Atualizar o estoque do produto
            novo_estoque = produto[2] - quantidade
            conn.execute('UPDATE produtos SET estoque = ? WHERE id = ?', (novo_estoque, produto_id))
            
            conn.commit()

    # Atualizar o valor total da venda
    conn.execute('UPDATE vendas SET valor_total = ? WHERE id = ?', (valor_total, venda_id))
    conn.commit()

    messagebox.showinfo("Venda realizada", f"Venda realizada com sucesso. Data e hora da venda: {data_hora_venda}. Valor total: {valor_total}")

# Função para exibir o estoque atual
def exibir_estoque():
    estoque_df = pd.read_sql_query('SELECT * FROM produtos', conn)
    return estoque_df

# Função para criar a interface gráfica usando Tkinter
class SistemaVendasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Vendas")

        # Configuração da tela principal
        self.frame_vendas = tk.Frame(root)
        self.frame_vendas.pack(padx=10, pady=10)

        self.frame_estoque = tk.Frame(root)
        self.frame_estoque.pack(padx=10, pady=10)

        # Componentes para a tela de vendas
        self.label_produto_venda = tk.Label(self.frame_vendas, text="ID do Produto:")
        self.label_produto_venda.grid(row=0, column=0, padx=5, pady=5)
        self.entry_produto_venda = tk.Entry(self.frame_vendas)
        self.entry_produto_venda.grid(row=0, column=1, padx=5, pady=5)

        self.label_quantidade_venda = tk.Label(self.frame_vendas, text="Quantidade:")
        self.label_quantidade_venda.grid(row=1, column=0, padx=5, pady=5)
        self.entry_quantidade_venda = tk.Entry(self.frame_vendas)
        self.entry_quantidade_venda.grid(row=1, column=1, padx=5, pady=5)

        self.label_cliente_nome = tk.Label(self.frame_vendas, text="Nome do Cliente:")
        self.label_cliente_nome.grid(row=2, column=0, padx=5, pady=5)
        self.entry_cliente_nome = tk.Entry(self.frame_vendas)
        self.entry_cliente_nome.grid(row=2, column=1, padx=5, pady=5)

        self.label_cliente_telefone = tk.Label(self.frame_vendas, text="Telefone do Cliente:")
        self.label_cliente_telefone.grid(row=3, column=0, padx=5, pady=5)
        self.entry_cliente_telefone = tk.Entry(self.frame_vendas)
        self.entry_cliente_telefone.grid(row=3, column=1, padx=5, pady=5)

        self.button_adicionar_carrinho = tk.Button(self.frame_vendas, text="Adicionar ao Carrinho", command=self.adicionar_carrinho)
        self.button_adicionar_carrinho.grid(row=4, column=0, columnspan=2, pady=10)

        self.label_carrinho = tk.Label(self.frame_vendas, text="Carrinho de Compras:")
        self.label_carrinho.grid(row=5, column=0, columnspan=2, pady=5)

        self.text_carrinho = tk.Text(self.frame_vendas, height=5, width=40)
        self.text_carrinho.grid(row=6, column=0, columnspan=2, pady=5)

        self.button_finalizar_compra = tk.Button(self.frame_vendas, text="Finalizar Compra", command=self.finalizar_compra)
        self.button_finalizar_compra.grid(row=7, column=0, columnspan=2, pady=10)

        # Componentes para a tela de estoque
        self.label_estoque = tk.Label(self.frame_estoque, text="Estoque Atual:")
        self.label_estoque.grid(row=0, column=0, padx=5, pady=5)

        self.text_estoque = tk.Text(self.frame_estoque, height=10, width=40)
        self.text_estoque.grid(row=1, column=0, padx=5, pady=5)

        # Botões para cadastro e consulta
        self.button_cadastro = tk.Button(self.frame_estoque, text="Cadastrar Produto", command=self.cadastrar_produto)
        self.button_cadastro.grid(row=2, column=0, pady=5)

        self.label_consulta = tk.Label(self.frame_estoque, text="Consulta de Produto:")
        self.label_consulta.grid(row=3, column=0, pady=5)

        self.entry_consulta = tk.Entry(self.frame_estoque)
        self.entry_consulta.grid(row=4, column=0, pady=5)

        self.button_consulta = tk.Button(self.frame_estoque, text="Consultar Produto", command=self.consultar_produto)
        self.button_consulta.grid(row=5, column=0, pady=5)

        # Chamar a função criar_produtos_teste ao iniciar
        self.atualizar_estoque()

        # Lista para armazenar os produtos no carrinho
        self.carrinho = []

    def adicionar_carrinho(self):
        produto_id = self.entry_produto_venda.get()
        quantidade = int(self.entry_quantidade_venda.get())

        cursor = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
        produto = cursor.fetchone()

        if produto and produto[2] >= quantidade:
            self.carrinho.append((produto_id, quantidade))
            self.atualizar_carrinho()
            messagebox.showinfo("Produto Adicionado", "Produto adicionado ao carrinho.")
        else:
            messagebox.showwarning("Erro ao Adicionar", "Produto não encontrado ou quantidade insuficiente em estoque.")

    def finalizar_compra(self):
        cliente_nome = self.entry_cliente_nome.get()
        cliente_telefone = self.entry_cliente_telefone.get()

        if not cliente_nome or not cliente_telefone:
            messagebox.showwarning("Dados do Cliente", "Por favor, preencha o nome e o telefone do cliente.")
            return

        for produto_id, quantidade in self.carrinho:
            realizar_venda(cliente_nome, cliente_telefone, [(produto_id, quantidade)])
        self.carrinho = []  # Limpar o carrinho após a compra
        self.atualizar_carrinho()
        self.atualizar_estoque()

    def cadastrar_produto(self):
        nome_produto = simpledialog.askstring("Cadastrar Produto", "Nome do Produto:")
        estoque_produto = simpledialog.askinteger("Cadastrar Produto", "Quantidade em Estoque:")
        preco_fab_produto = simpledialog.askfloat("Cadastrar Produto", "Preço de Fábrica:")
        valor_venda_produto = simpledialog.askfloat("Cadastrar Produto", "Valor de Venda:")
        
        if nome_produto and estoque_produto is not None and preco_fab_produto is not None and valor_venda_produto is not None:
            adicionar_produto(nome_produto, estoque_produto, preco_fab_produto, valor_venda_produto)
            messagebox.showinfo("Produto Cadastrado", "Produto cadastrado com sucesso.")
            self.atualizar_estoque()

    def consultar_produto(self):
        produto_id = int(self.entry_consulta.get())
        cursor = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
        produto = cursor.fetchone()

        print(produto)  # Adicione esta linha para imprimir a tupla no console

        if produto:
            messagebox.showinfo(
                "Consulta de Produto",
                f"ID: {produto[0]}\nNome: {produto[1]}\nEstoque: {produto[2]}\nPreço de Fábrica: {produto[3]}\nValor de Venda: {produto[4]}"
            )
        else:
            messagebox.showwarning("Produto não encontrado", "Produto não encontrado.")


    def atualizar_carrinho(self):
        self.text_carrinho.delete(1.0, tk.END)  # Limpar o texto atual no carrinho
        for produto_id, quantidade in self.carrinho:
            self.text_carrinho.insert(tk.END, f"ID: {produto_id}, Quantidade: {quantidade}\n")

    def atualizar_estoque(self):
        estoque_df = exibir_estoque()
        self.text_estoque.delete(1.0, tk.END)  # Limpar o texto atual no estoque
        self.text_estoque.insert(tk.END, estoque_df.to_string(index=False))

# Criar a instância da aplicação Tkinter
root = tk.Tk()
app = SistemaVendasApp(root)

# Iniciar o loop principal
root.mainloop()

# Fechar a conexão com o banco de dados ao final do programa
conn.close()
