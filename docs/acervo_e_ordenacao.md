# Acervo e ordenação por texto e ano

Documentação da frente **Acervo e ordenação** (Pessoa 1): estrutura de dados do acervo, Quick Sort e Radix Sort MSD.

## 1. Estrutura de dados do acervo

Todo o estado fica em um único JSON (`dados/acervo.json`), com três listas:

```json
{
  "livros":      [{"id": 1, "titulo": "...", "autor": "...", "genero": "...", "ano": 1899, "total": 2}],
  "leitores":    [{"id": 1, "nome": "...", "matricula": "...", "contato": "..."}],
  "emprestimos": [{"id": 1, "leitor_id": 1, "livro_id": 1, "emprestado_em": "AAAA-MM-DD",
                   "previsto_em": "AAAA-MM-DD", "devolvido_em": null, "nota": null}]
}
```

Regras do livro (`Acervo.livro` em `servico.py`):

* **ID** único, sequencial (maior ID + 1) e imutável: a edição passa `id=` e nunca o altera.
* **Título, autor e gênero** são obrigatórios (espaços nas pontas são removidos).
* **Ano** é inteiro de 1 a 9999; **total** é inteiro positivo.
* Só o `total` de exemplares é gravado. `disponiveis`, `popularidade` e `nota_media` são **derivados** dos empréstimos em `Acervo.livros()`, então não há como ficarem inconsistentes com o histórico.
* Editar o `total` para um valor menor que os empréstimos ativos é bloqueado.
* Toda gravação trabalha numa cópia e substitui o arquivo de forma atômica; se a validação falhar, nada é alterado.

A interface chama `ordenar(livros, campo, crescente, algoritmo)` sobre o resultado de `Acervo.livros()`. Cada linha da tabela usa o ID do livro como identificador, então editar ou reordenar não troca o livro selecionado.

## 2. Quick Sort

Usado para qualquer campo (texto, ID, popularidade, etc.).

* **Pivô:** mediana de três (primeiro, meio, último). Evita o pior caso em listas já ordenadas ou em ordem inversa.
* **Partição em três vias** (menores | iguais | maiores): chaves repetidas ficam todas no bloco central e não são reprocessadas.
* **Iterativo com pilha explícita:** a parte maior é empilhada e a menor é tratada primeiro, então a pilha tem no máximo `O(log n)` entradas e não há erro de recursão.
* **Complexidade:** `O(n log n)` no caso médio; `O(n²)` no pior caso teórico (entradas construídas contra a mediana de três). Espaço auxiliar: `O(n)` para o par (chave, item) mais `O(log n)` de pilha.
* **Não é estável:** livros com a mesma chave podem sair em ordem diferente da original.
* Não altera a lista de entrada.

## 3. Radix Sort MSD (campo ano)

* Aceita **somente `ano`**; qualquer outro campo gera `ValueError`.
* **Domínio:** inteiros de 0 a 9999 (4 dígitos decimais). Valores fora do intervalo, não inteiros, `bool` ou `None` geram `ValueError`.
* **Funcionamento:** distribui os livros em 10 baldes pelo dígito mais significativo (milhar) e ordena cada balde recursivamente pelo dígito seguinte, até a unidade. No sentido decrescente apenas a ordem de visita dos baldes se inverte (9 → 0).
* **Complexidade:** `O(d · n)` com `d = 4` dígitos, ou seja, linear em `n`; espaço `O(n)`.
* **Estável** nos dois sentidos: anos iguais mantêm a ordem original.
* Na interface, escolher Radix Sort MSD fixa o campo em `ano`.

## 4. Ordenação por texto e por ano — regras adotadas

| Situação | Tratamento |
| --- | --- |
| Maiúsculas/minúsculas | Ignoradas (`casefold`), em todos os algoritmos. |
| Acentos | Mantidos: a comparação é por código de caractere, então "Átomos" vem depois de "Zebra". Mesma regra dos demais algoritmos. |
| Campo ausente (`None`) | Vai para o final nos dois sentidos (hoje só ocorre em `nota_media`). |
| Empates | Merge Sort e Radix MSD preservam a ordem original; Heap Sort e Quick Sort não garantem. |
| Lista vazia ou com um item | Retorna a própria lista (cópia), sem erro. |
| Decrescente | Mesma função com a comparação invertida; o resultado nunca é obtido invertendo o crescente. |

## 5. Testes

* `test_quick_radix.py`: Quick Sort e Radix MSD contra `sorted` (listas vazias, repetidas, ordem inversa, 20 mil elementos), estabilidade do Radix, domínio inválido e integração via `ordenar`.
* `test_acervo.py`: cadastro, edição, persistência após reabrir, validações, regra do total versus empréstimos ativos e ordenação após cadastrar/editar.

```bash
python -m unittest -v test_quick_radix test_acervo
```
