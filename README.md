<div>
    <h1 style="color:green" text-align="center">
    CT Traker
	</h1>
</div>


-------
Projeto construído para o Centro de treinamento do Coritiba Football Clube, para fins didáticos, com o objetivo de colocar em prática os conhecimentos em Python.

## 💻 Tecnologia
- Python



### Descrição do Projeto: Controle de Entradas e Saídas

O projeto "Controle de Entradas e Saídas" é um sistema desenvolvido em Python com uma interface gráfica (GUI) criada usando a biblioteca Tkinter. 
Ele permite o gerenciamento de entradas e saídas de veículos e pessoas, registrando informações em planilhas do Excel para fácil consulta, adição, 
edição e exclusão de dados.

#### Funcionalidades Principais:
1. **Cadastro de Pessoas e Veículos**: O usuário pode cadastrar nomes e detalhes dos veículos associados (marca, modelo, placa, cor).
2. **Pesquisa**: Permite pesquisar por nome ou placa, exibindo os resultados encontrados.
3. **Edição de Dados**: Dados pessoais e veículos associados podem ser alterados ou excluídos diretamente pela interface.
4. **Listagem de Veículos**: Veículos associados a uma pessoa são exibidos para fácil visualização e gerenciamento.
5. **Controle de Acesso e Expiração**: O programa verifica a última execução e expiração do software para evitar tentativas de uso fora do período autorizado.

#### Estrutura do Projeto:
- **ct_tracker.py**: Script principal que gerencia a interface, funções de busca, edição, adição e controle de expiração.
- **generate_key.py**: Script auxiliar usado para gerar a chave de criptografia.
- **Planilhas Excel**: As informações de pessoas e veículos são armazenadas em duas planilhas Excel: "pessoas.xlsx" e "veiculos.xlsx".

### Detalhes da Criptografia:
A criptografia é utilizada para garantir que o programa só seja usado durante o período autorizado e para registrar a última execução de maneira segura.
A criptografia é feita utilizando a biblioteca `cryptography` com o módulo Fernet, que oferece criptografia simétrica com segurança robusta.

#### Componentes da Criptografia:
1. **Chave de Criptografia**:
   - Uma chave secreta é gerada usando o script `generate_key.py`, que cria um arquivo `secret.key` contendo a chave necessária para encriptação e decriptação.
   - Esta chave é utilizada pelo programa principal para criptografar e descriptografar as datas de execução.

2. **Controle de Expiração**:
   - O arquivo `ct_tracker.py` verifica se a data atual está dentro do prazo permitido para o uso do software, utilizando a data de expiração definida no código.
   - Se a data atual for superior à data de expiração, o programa mostra uma mensagem ao usuário e encerra a execução.

3. **Registro da Última Execução**:
   - O programa armazena a data da última execução em um arquivo `last_use.txt`, que é criptografado com a chave secreta.
   - Durante a inicialização, o programa descriptografa este arquivo para verificar a data da última execução, prevenindo tentativas de alteração indevida do sistema.

#### Fluxo da Criptografia:
- **Geração da Chave**: A chave é gerada uma vez pelo script `generate_key.py` e armazenada em `secret.key`.
- **Encriptação**: Quando o programa registra a data de execução, ele criptografa essa data antes de armazená-la.
- **Decriptação**: Ao iniciar, o programa lê e descriptografa a data para garantir que o uso do software está dentro dos limites permitidos.

### Segurança:
A criptografia adiciona uma camada extra de segurança ao sistema, evitando que usuários não autorizados manipulem os arquivos de data para prolongar o uso indevido do programa.

### Configurações:

O arquivo `instrução.txt` contém todas as informações detalhadas sobre a configuração do ambiente de trabalho para o projeto. Ele inclui as orientações necessárias para a instalação das bibliotecas e dependências, e também a geração do arquivo executável, garantindo que o ambiente esteja corretamente preparado para o funcionamento do sistema.
