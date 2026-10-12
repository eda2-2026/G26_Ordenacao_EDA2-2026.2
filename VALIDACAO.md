# Validação

Em 11/10/2026, os 13 testes automatizados passaram no ambiente de desenvolvimento.

## Cobertura

* 4 testes dos algoritmos: ordenação, preservação da entrada, estabilidade, notas ausentes e validação de parâmetros.
* 8 testes de serviço: circulação, médias, validações, edição, referências, persistência, falha de gravação e dados de demonstração.
* 1 teste de interface: cadastro e edição pelos formulários, empréstimo, devolução, tabelas, seleção de algoritmo, mensagens de erro e persistência.

## Executar Novamente

```bash
python -m unittest -v
```

Os testes usam bases temporárias e não alteram os dados cadastrados na aplicação. O teste de interface requer ambiente gráfico e usa uma janela oculta. Ele não substitui a inspeção visual manual em diferentes resoluções.
