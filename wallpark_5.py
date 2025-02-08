import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector
import os

# Configuração do banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Insira sua senha do MySQL
        database="estacionamento"
        port=3306  # Adicione a porta, caso seja necessário
    )

# Função para login
def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE login=%s AND senha=%s", (usuario, senha))
    resultado = cursor.fetchone()
    conexao.close()
    
    if resultado:
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        root.destroy()
        abrir_menu()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")

# Função para registrar entrada de veículos
def registrar_entrada(entry_placa, entry_modelo, entry_cor, entry_tipo_veiculo):
    placa = entry_placa.get()
    modelo = entry_modelo.get()
    cor = entry_cor.get()
    tipo = entry_tipo_veiculo.get().strip().lower()

    if not placa or not modelo or not cor or tipo not in ["pequeno", "grande"]:
        messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
        return
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute("INSERT INTO veiculos (placa, modelo, cor, tipo, entrada) VALUES (%s, %s, %s, %s, %s)",
                       (placa, modelo, cor, tipo, datetime.now()))
        conexao.commit()

        # Inserir notificação no banco de dados
        cursor.execute("INSERT INTO notificacoes (mensagem, data) VALUES (%s, %s)", 
                       (f"Entrada registrada: {placa}", datetime.now()))
        conexao.commit()

        messagebox.showinfo("Entrada Registrada", f"\nPlaca: {placa}\nEntrada registrada com sucesso!")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao registrar entrada: {err}")
    finally:
        conexao.close()

    atualizar_lista_veiculos()

# Função para registrar saída e calcular pagamento
def registrar_saida(entry_placa, var_pagamento):
    placa = entry_placa.get()
    pagamento = var_pagamento.get()
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM veiculos WHERE placa=%s", (placa,))
    entrada_info = cursor.fetchone()

    if not entrada_info:
        messagebox.showerror("Erro", "Placa não registrada!")
        conexao.close()
        return

    tipo_veiculo = entrada_info[4]  # Alterado para refletir a posição correta da coluna "tipo"
    hora_entrada = entrada_info[5]  # A posição da coluna "entrada" é 5 (ajuste conforme seu banco de dados)
    
    hora_saida = datetime.now()
    tempo_estacionado = (hora_saida - hora_entrada).total_seconds() / 3600  # Calcular tempo estacionado em horas
    precos = {"pequeno": 5, "grande": 10}
    valor = round(tempo_estacionado * precos[tipo_veiculo], 2)

    hora_entrada_str = hora_entrada.strftime('%Y-%m-%d %H:%M:%S')
    hora_saida_str = hora_saida.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute(""" 
        INSERT INTO saidas (placa, hora_entrada, hora_saida, tipo, valor, pagamento) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (placa, hora_entrada_str, hora_saida_str, tipo_veiculo, valor, pagamento))
    
    cursor.execute("DELETE FROM veiculos WHERE placa=%s", (placa,))
    conexao.commit()

    # Inserir notificação no banco de dados
    cursor.execute("INSERT INTO notificacoes (mensagem, data) VALUES (%s, %s)", 
                   (f"Saída registrada: {placa} - Pagamento: R$ {valor:.2f}", datetime.now()))
    conexao.commit()

    conexao.close()

    messagebox.showinfo("Pagamento Concluído", f"Placa: {placa}\nValor: R$ {valor:.2f}\nPagamento: {pagamento}")

    atualizar_lista_veiculos()

# Função para atualizar lista de veículos na tela
def atualizar_lista_veiculos():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT placa, modelo, cor, tipo FROM veiculos")
    veiculos = cursor.fetchall()
    conexao.close()

    listbox_veiculos.delete(0, tk.END)
    for v in veiculos:
        listbox_veiculos.insert(tk.END, f"{v[0]} | {v[1]} | {v[2]} | {v[3]}")

# Função para exibir histórico de notificações
def exibir_historico_notificacoes():
    historico_window = tk.Toplevel()
    historico_window.title("Histórico de Notificações")

    tk.Label(historico_window, text="Histórico de Notificações").pack()

    listbox_historico = tk.Listbox(historico_window, width=80, height=20, selectmode=tk.EXTENDED)
    listbox_historico.pack()

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT mensagem, data FROM notificacoes")
    notificacoes = cursor.fetchall()
    conexao.close()

    for notificacao in notificacoes:
        listbox_historico.insert(tk.END, f"{notificacao[0]} - {notificacao[1]}")

    def selecionar_todos():
        listbox_historico.select_set(0, tk.END)

    def salvar_relatorio():
        if not notificacoes:
            messagebox.showwarning("Aviso", "Não há notificações para salvar!")
            return

        pasta_destino = "wallpark"
        os.makedirs(pasta_destino, exist_ok=True)

        data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = os.path.join(pasta_destino, f"wallpark_{data_atual}.txt")

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write("RELATÓRIO DE MOVIMENTAÇÃO DO ESTACIONAMENTO\n")
            arquivo.write("===========================================\n\n")
            for notificacao in notificacoes:
                arquivo.write(f"{notificacao[0]} - {notificacao[1]}\n")

        messagebox.showinfo("Relatório Salvo", f"Relatório salvo em:\n{nome_arquivo}")
        
    def imprimir_selecionados():
        selecionados = listbox_historico.curselection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Nenhuma notificação selecionada!")
            return

        # Criar diretório para relatórios se não existir
        pasta_destino = "wallpark"
        os.makedirs(pasta_destino, exist_ok=True)

        for i in selecionados:
            notificacao = listbox_historico.get(i)
            
            try:
                placa = notificacao.split(" | ")[0].split(":")[1].strip()
            except IndexError:
                placa = "desconhecido"

            data_notificacao = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_arquivo = os.path.join(pasta_destino, f"nota_{placa}_{data_notificacao}.txt")

            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write(notificacao)
            
            print(f"Notificação salva em: {nome_arquivo}")

        texto_imprimir = "\n".join([listbox_historico.get(i) for i in selecionados])
        print("Imprimindo:\n", texto_imprimir)
        messagebox.showinfo("Impressão", "Tickets selecionados foram enviados para impressão!")

    tk.Button(historico_window, text="Imprimir Selecionados", command=imprimir_selecionados).pack(pady=5)
    tk.Button(historico_window, text="Selecionar Todos", command=selecionar_todos).pack(pady=5)
    tk.Button(historico_window, text="Salvar Relatório", command=salvar_relatorio).pack(pady=5)

# Função para abrir o menu principal
def abrir_menu():
    global listbox_veiculos

    menu_window = tk.Tk()
    menu_window.title("Sistema de Estacionamento")

    tk.Label(menu_window, text="Placa:").grid(row=0, column=0)
    entry_placa = tk.Entry(menu_window)
    entry_placa.grid(row=0, column=1)

    tk.Label(menu_window, text="Modelo:").grid(row=1, column=0)
    entry_modelo = tk.Entry(menu_window)
    entry_modelo.grid(row=1, column=1)

    tk.Label(menu_window, text="Cor:").grid(row=2, column=0)
    entry_cor = tk.Entry(menu_window)
    entry_cor.grid(row=2, column=1)

    tk.Label(menu_window, text="Tipo (pequeno/grande):").grid(row=3, column=0)
    entry_tipo_veiculo = tk.Entry(menu_window)
    entry_tipo_veiculo.grid(row=3, column=1)

    tk.Button(menu_window, text="Registrar Entrada", command=lambda: registrar_entrada(entry_placa, entry_modelo, entry_cor, entry_tipo_veiculo)).grid(row=4, column=0, columnspan=2)

    tk.Label(menu_window, text="Forma de Pagamento:").grid(row=5, column=0)
    var_pagamento = tk.StringVar(value="À vista")
    tk.OptionMenu(menu_window, var_pagamento, "À vista", "Cartão de Débito", "Mensal").grid(row=5, column=1)

    tk.Button(menu_window, text="Registrar Saída e Pagamento", command=lambda: registrar_saida(entry_placa, var_pagamento)).grid(row=6, column=0, columnspan=2)

    tk.Label(menu_window, text="Lista de Veículos:").grid(row=7, column=0)
    listbox_veiculos = tk.Listbox(menu_window, width=60)
    listbox_veiculos.grid(row=7, column=1)

    atualizar_lista_veiculos()

    tk.Button(menu_window, text="Ver Histórico de Notificações", command=exibir_historico_notificacoes).grid(row=8, column=0, columnspan=2)

    menu_window.mainloop()

# Interface de login
root = tk.Tk()
root.title("Login - Sistema de Estacionamento")

tk.Label(root, text="Usuário:").pack()
entry_usuario = tk.Entry(root)
entry_usuario.pack()

tk.Label(root, text="Senha:").pack()
entry_senha = tk.Entry(root, show="*")
entry_senha.pack()

tk.Button(root, text="Login", command=verificar_login).pack(pady=5)

root.mainloop()
