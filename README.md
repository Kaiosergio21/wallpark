Turma: 88434

Aluno: Kaio Sergio Sales Nunes

Matéria:Implantação de Sistemas

Docente:Professor Anderson Lima



Abaixo está um exemplo de README para o seu projeto "Sistema de Estacionamento":

---

# Sistema de Estacionamento

Este é um sistema simples de estacionamento desenvolvido em Python usando o Tkinter para a interface gráfica e MySQL como banco de dados para armazenar as informações dos veículos, usuários, entradas, saídas e notificações.

## Funcionalidades

- **Login de Usuário**: Autenticação de usuários para acesso ao sistema.
- **Registro de Entrada de Veículos**: Permite registrar a entrada de veículos, incluindo informações como placa, modelo, cor e tipo de veículo.
- **Registro de Saída e Pagamento**: Permite registrar a saída de veículos, calcular o tempo estacionado e o valor a ser pago, além de registrar o pagamento.
- **Notificações**: O sistema envia notificações para o banco de dados, tanto para registros de entrada quanto de saída.
- **Histórico de Notificações**: Exibe um histórico de todas as notificações realizadas, com a opção de selecionar notificações para salvar ou imprimir.

## Requisitos

Para executar o sistema, é necessário:

- Python 3.x
- Tkinter (geralmente já vem instalado com o Python)
- MySQL
- Biblioteca `mysql-connector` para Python

Para instalar a biblioteca MySQL Connector:

```bash
pip install mysql-connector-python
```

## Configuração do Banco de Dados

1. **Criação do banco de dados e tabelas**:

   Execute o seguinte código SQL para configurar o banco de dados no MySQL:

```sql
CREATE DATABASE estacionamento;

USE estacionamento;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) UNIQUE NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    cor VARCHAR(30) NOT NULL,
    tipo ENUM('pequeno', 'grande') NOT NULL,
    entrada DATETIME NOT NULL
);

CREATE TABLE saidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) NOT NULL,
    hora_entrada DATETIME NOT NULL,
    hora_saida DATETIME NOT NULL,
    tipo ENUM('pequeno', 'grande') NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    pagamento VARCHAR(20) NOT NULL
);

CREATE TABLE notificacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mensagem TEXT NOT NULL,
    data DATETIME NOT NULL
);
```

2. **Inserir dados de usuários**: Insira usuários para o login usando comandos SQL, por exemplo:

```sql
INSERT INTO usuarios (login, senha) VALUES ('admin', '12345');
```

## Como Usar

1. **Login**: Ao iniciar o sistema, você verá a tela de login onde deverá informar seu usuário e senha.
2. **Registro de Entrada**: Após o login, você será redirecionado para o menu onde poderá registrar entradas de veículos, inserindo as informações de placa, modelo, cor e tipo de veículo.
3. **Registro de Saída e Pagamento**: Na mesma interface, você pode registrar a saída de veículos, calcular o tempo estacionado e o valor a ser pago.
4. **Notificações e Histórico**: Você pode acessar o histórico de notificações, visualizar todos os registros de entrada e saída de veículos, e salvar ou imprimir relatórios.

## Observações

- A pasta `wallpark` será criada automaticamente para armazenar os relatórios e notas.
- O sistema envia notificações tanto para o banco de dados quanto para arquivos locais em formato `.txt`.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Esse é um exemplo básico de README para documentar seu projeto. Se precisar de mais detalhes ou ajustes, só avisar!
