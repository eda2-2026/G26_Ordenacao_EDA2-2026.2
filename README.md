# Acervo Bibliográfico - Algoritmos de Ordenação

## Objetivo do Projeto

O objetivo deste projeto é organizar um acervo bibliográfico por meio de algoritmos de ordenação implementados manualmente. A aplicação permite cadastrar livros e leitores, registrar empréstimos e devoluções e ordenar os livros por diferentes critérios em uma interface gráfica.

O trabalho pertence ao **Grupo 26**, da disciplina de **Estruturas de Dados 2**, no semestre **2026.2**.

## Características dos Dados e da Arquitetura

* **Acervo:** livros com ID, título, autor, gênero, ano de publicação e total de exemplares, com cadastro e edição.
* **Leitores:** cadastro com ID, nome, matrícula única e contato, com edição dos dados.
* **Circulação:** empréstimos vinculados ao livro e ao leitor, com prazo de 14 dias e registro da devolução.
* **Avaliações:** nota opcional de 0 a 5 na devolução; a média é calculada a partir do histórico.
* **Ordenação:** Heap Sort, Merge Sort, Quick Sort e Radix Sort MSD (apenas ano), com seleção de campo e sentido crescente ou decrescente.
* **Interface gráfica:** três abas desenvolvidas em Python com Tkinter.
* **Persistência:** armazenamento local em JSON, com substituição atômica do arquivo para cada operação.
* **Medição:** exibição do tempo de preparação e ordenação da listagem atual em milissegundos. Essa medição não constitui um benchmark controlado.

### Origem dos Dados

A aplicação inicia com três obras, dois leitores fictícios e uma devolução avaliada para demonstrar o funcionamento. Os registros de leitores utilizam contatos de exemplo. Novos cadastros podem ser feitos pela interface.

Os dados ficam em `dados/acervo.json`, criado automaticamente durante o uso. Esse arquivo não é versionado.

## Divisão de Responsabilidades

O trabalho foi organizado em duas frentes:

* **Acervo e ordenação (Pessoa 1):** cadastro e edição de livros, listagem, Quick Sort, Radix Sort MSD, seleção dos critérios de ordenação, integração da tabela e testes do acervo e desses algoritmos.
* **Leitores e circulação (Pessoa 2):** cadastro e edição de leitores, empréstimos, devoluções, avaliações, Heap Sort, Merge Sort e testes das regras.

### Responsabilidade Compartilhada

* Integração das funcionalidades na interface.
* Revisão das regras de negócio e dos resultados das ordenações.
* Testes, documentação e apresentação do projeto.

## Como Funcionam as Ordenações

### Heap Sort

O algoritmo organiza os elementos em uma estrutura de heap e extrai sucessivamente os extremos para produzir a lista ordenada. Sua complexidade de tempo é `O(n log n)` no melhor, médio e pior caso. Não garante preservar a ordem original dos elementos com a mesma chave.

A implementação trabalha sobre uma cópia da lista, preservando a entrada. Embora a ordenação interna do Heap Sort use espaço auxiliar constante, essa cópia utiliza `O(n)` de memória.

### Merge Sort

O algoritmo divide a lista em duas partes, ordena cada parte recursivamente e intercala os resultados. Sua complexidade de tempo é `O(n log n)`, com espaço auxiliar `O(n)` no pico de utilização.

A implementação preserva a ordem dos elementos com a mesma chave, tanto na ordenação crescente quanto na decrescente.

### Quick Sort

Escolhe o pivô pela mediana de três e particiona em três vias (menores, iguais e maiores), o que mantém bom desempenho com chaves repetidas e com listas já ordenadas ou invertidas. É iterativo, com pilha de no máximo `O(log n)` entradas. Complexidade média `O(n log n)` e pior caso teórico `O(n²)`. Não é estável.

### Radix Sort MSD

Ordena o ano de publicação (inteiros de 0 a 9999) distribuindo os livros em baldes pelo dígito mais significativo e refinando cada balde pelos dígitos seguintes. Custa `O(d · n)` com `d = 4`, é estável nos dois sentidos e rejeita valores fora do domínio. Na interface, ao escolhê-lo o campo fica fixo em `ano`.

A estrutura de dados do acervo e as regras de ordenação por texto e ano estão detalhadas em [`docs/acervo_e_ordenacao.md`](docs/acervo_e_ordenacao.md).

### Critérios Disponíveis

Heap Sort, Merge Sort e Quick Sort podem ordenar por título, autor, gênero, ano, ID, exemplares disponíveis, quantidade de empréstimos ou nota média. A comparação de texto ignora diferenças entre maiúsculas e minúsculas e mantém os acentos. Livros sem avaliação aparecem no final nos dois sentidos.

## 💻 Como Baixar e Executar

### Pré-requisitos

* Python 3.10 ou superior, com Tkinter instalado.
* No Windows, o instalador padrão do Python inclui Tkinter quando a opção Tcl/Tk é selecionada.
* Não são necessários pacotes externos.

### Opção mais simples: baixar pelo navegador

1. Abra o repositório `eda2-2026/G26_Ordenacao_EDA2-2026.2` no GitHub.
2. Clique em **Code > Download ZIP**.
3. Extraia o arquivo.
4. Dê dois cliques em `iniciar.bat` no Windows.

### Clonando o Projeto

```bash
git clone https://github.com/eda2-2026/G26_Ordenacao_EDA2-2026.2.git
cd G26_Ordenacao_EDA2-2026.2
python app.py
```

Se o comando `python` não estiver disponível no Windows, use `py app.py`. No Linux ou macOS, use `python3 app.py`; Tkinter pode precisar ser instalado pelo gerenciador de pacotes do sistema.

### Executando pela IDE

1. Abra a pasta no VS Code ou PyCharm.
2. Selecione um interpretador Python 3.10 ou superior com Tkinter.
3. Execute `app.py`.

### Base de Teste Independente

```bash
python app.py --dados dados/teste.json
```

Para iniciar uma nova base vazia, sem os exemplos:

```bash
python app.py --dados dados/vazio.json --sem-demo
```

## Executando os Testes

Execute `python -m unittest -v` na pasta do projeto ou abra `testes.bat` no Windows.

Os testes de Quick Sort, Radix Sort MSD e do acervo ficam em `test_quick_radix.py` e `test_acervo.py` e não precisam de ambiente gráfico. Os 13 testes da outra frente verificam ordenação, estabilidade do Merge Sort, listas vazias e repetidas, notas ausentes, cadastro e edição de leitores, validações, empréstimos, devoluções, médias, persistência e falha de gravação. Um teste adicional à lógica de serviço, incluído nesse total, exercita os formulários em uma janela oculta; por isso, a suíte completa precisa de um ambiente gráfico disponível.

Para executar somente os testes que não abrem componentes gráficos:

```bash
python -m unittest -v test_algoritmos test_servico test_quick_radix test_acervo
```

## 🎥 Demonstração Visual

Ao executar `app.py`, o sistema abre o painel do acervo. A partir dele, é possível:

1. Na aba **Acervo e ordenação**, cadastrar um livro e ordenar a tabela por campo, algoritmo e direção.
2. Na aba **Leitores**, cadastrar um leitor ou selecionar um registro para editar.
3. Na aba **Empréstimos e devoluções**, escolher livro e leitor para registrar um empréstimo.
4. Selecionar um empréstimo e registrar a devolução, com avaliação opcional.
5. Voltar ao acervo para conferir disponibilidade, popularidade e nota média.

### Apresentação em Vídeo

[Assista à apresentação do Acervo Bibliográfico no YouTube](https://www.youtube.com/watch?v=47OzSPtXssw).

### Capturas de Tela

**Acervo e ordenação:** cadastro e edição de livros, seleção do algoritmo e critérios de ordenação.

![Interface de cadastro e ordenação do acervo](docs/imagens/acervo.png)

**Leitores:** cadastro e edição dos dados dos leitores.

![Interface de cadastro de leitores](docs/imagens/leitores.png)

**Empréstimos e devoluções:** controle da circulação dos livros e registro de avaliações.

![Interface de empréstimos e devoluções](docs/imagens/emprestimos-devolucoes.png)

**Heap Sort por nota média:** livros ordenados pelas avaliações, em ordem decrescente.

![Resultado do Heap Sort por nota média em ordem decrescente](docs/imagens/heap-sort-notas.png)

### Roteiro de Validação Manual

Empreste o único exemplar de **O Cortiço** para um leitor e tente emprestá-lo a outro. A segunda operação deve ser bloqueada. Devolva o livro com nota e confira a atualização da disponibilidade e da média. Uma nova devolução do mesmo empréstimo também deve ser bloqueada.

## Estrutura do Projeto

```text
app.py                 Interface gráfica
servico.py             Regras de negócio e persistência
algoritmos.py          Heap Sort, Merge Sort, Quick Sort, Radix Sort MSD e seleção da ordenação
test_algoritmos.py     Testes dos algoritmos
test_quick_radix.py    Testes do Quick Sort e do Radix Sort MSD
test_acervo.py         Testes de cadastro, edição e persistência de livros
docs/                  Estrutura de dados e ordenação por texto e ano
test_servico.py        Testes das regras de negócio
test_interface.py      Teste dos formulários
iniciar.bat            Inicializador para Windows
testes.bat             Executor de testes para Windows
VALIDACAO.md           Resultado e limites da validação
```

## Limites da Versão

O sistema foi desenvolvido para uso local por uma instância de cada vez. Não inclui autenticação, exclusão de registros ou comparação estatística de desempenho. As datas de circulação seguem a data local do computador.

## Equipe de Desenvolvimento

| Gabriel Ferreira | Maria Laura Cabral |
| :---: | :---: |
| <img src="https://github.com/diangellis.png" width="120" alt="Gabriel Ferreira" /> | <img src="https://github.com/Maria-Laura-Regis.png" width="120" alt="Maria Laura Cabral" /> |
| Matrícula: **242004671** | Matrícula: **232005361** |
| [@diangellis](https://github.com/diangellis) | [@Maria-Laura-Regis](https://github.com/Maria-Laura-Regis) |


