import random
import unittest

from algoritmos import ordenar, quick_sort, radix_sort_msd


def livro(id, titulo='T', autor='A', genero='G', ano=2000, disponiveis=1, popularidade=0, nota_media=None):
    return dict(id=id, titulo=titulo, autor=autor, genero=genero, ano=ano,
                disponiveis=disponiveis, popularidade=popularidade, nota_media=nota_media)


class TestQuickSort(unittest.TestCase):
    def test_lista_vazia_e_unitaria(self):
        self.assertEqual(quick_sort([]), [])
        self.assertEqual(quick_sort([7]), [7])

    def test_casos_basicos(self):
        casos = [[3, 1, 2], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [2, 2, 2, 2], [4, 1, 4, 1, 3, 3, 0]]
        for caso in casos:
            self.assertEqual(quick_sort(caso), sorted(caso))
            self.assertEqual(quick_sort(caso, reverse=True), sorted(caso, reverse=True))

    def test_aleatorio_contra_sorted(self):
        rng = random.Random(26)
        for _ in range(300):
            dados = [rng.randint(-20, 20) for _ in range(rng.randint(0, 60))]
            self.assertEqual(quick_sort(dados), sorted(dados))
            self.assertEqual(quick_sort(dados, reverse=True), sorted(dados, reverse=True))

    def test_nao_altera_entrada(self):
        dados = [3, 1, 2]
        quick_sort(dados)
        self.assertEqual(dados, [3, 1, 2])

    def test_entradas_grandes_sem_estouro_de_pilha(self):
        n = 20000
        for dados in (list(range(n)), list(range(n, 0, -1)), [1] * n):
            self.assertEqual(quick_sort(dados), sorted(dados))
            self.assertEqual(quick_sort(dados, reverse=True), sorted(dados, reverse=True))

    def test_key_preserva_elementos(self):
        dados = [('b', 1), ('a', 2), ('b', 3), ('a', 4)]
        r = quick_sort(dados, key=lambda x: x[0])
        self.assertEqual(sorted(r), sorted(dados))
        self.assertEqual([x[0] for x in r], ['a', 'a', 'b', 'b'])


class TestRadixSortMSD(unittest.TestCase):
    def test_lista_vazia_e_unitaria(self):
        self.assertEqual(radix_sort_msd([]), [])
        self.assertEqual(radix_sort_msd([1899]), [1899])

    def test_casos_basicos(self):
        casos = [[1937, 1890, 1899], [1, 9999, 0, 10, 100, 1000], [1900] * 5, [2020, 2019, 2018, 2017]]
        for caso in casos:
            self.assertEqual(radix_sort_msd(caso), sorted(caso))
            self.assertEqual(radix_sort_msd(caso, reverse=True), sorted(caso, reverse=True))

    def test_aleatorio_contra_sorted(self):
        rng = random.Random(26)
        for _ in range(300):
            dados = [rng.randint(1, 9999) for _ in range(rng.randint(0, 80))]
            self.assertEqual(radix_sort_msd(dados), sorted(dados))
            self.assertEqual(radix_sort_msd(dados, reverse=True), sorted(dados, reverse=True))

    def test_estavel_nos_dois_sentidos(self):
        dados = [(1990, 'a'), (1985, 'b'), (1990, 'c'), (1985, 'd'), (1990, 'e')]
        self.assertEqual(radix_sort_msd(dados, key=lambda x: x[0]), sorted(dados, key=lambda x: x[0]))
        self.assertEqual(radix_sort_msd(dados, key=lambda x: x[0], reverse=True),
                         sorted(dados, key=lambda x: x[0], reverse=True))

    def test_nao_altera_entrada(self):
        dados = [3, 1, 2]
        radix_sort_msd(dados)
        self.assertEqual(dados, [3, 1, 2])

    def test_dominio_invalido(self):
        for invalido in ([-1], [10000], [2000.5], ['2000'], [None], [True]):
            with self.assertRaises(ValueError, msg=repr(invalido)):
                radix_sort_msd(invalido)


class TestOrdenarIntegracao(unittest.TestCase):
    def setUp(self):
        self.livros = [
            livro(1, 'dom casmurro', 'Machado', 'Romance', 1899, 2, 3, 4.5),
            livro(2, 'Átomos', 'Zélia', 'Ciência', 1890, 1, 1, None),
            livro(3, 'Capitães', 'Amado', 'Romance', 1937, 3, 2, 3.0),
            livro(4, 'Dom Casmurro', 'Outro', 'Romance', 1937, 0, 0, None),
            livro(5, 'brás', 'Azevedo', 'Conto', 1890, 5, 3, 5.0),
        ]
        self.campos = ['id', 'titulo', 'autor', 'genero', 'ano', 'disponiveis', 'popularidade', 'nota_media']

    def ids(self, lista):
        return [x['id'] for x in lista]

    def test_quick_sort_todos_os_campos_nos_dois_sentidos(self):
        for campo in self.campos:
            for crescente in (True, False):
                r = ordenar(self.livros, campo, crescente, 'Quick Sort')
                self.assertEqual(sorted(self.ids(r)), [1, 2, 3, 4, 5])
                com_valor = [x[campo] for x in r if x[campo] is not None]
                norm = [v.casefold() if isinstance(v, str) else v for v in com_valor]
                self.assertEqual(norm, sorted(norm, reverse=not crescente), (campo, crescente))

    def test_sem_nota_ao_final_nos_dois_sentidos(self):
        for crescente in (True, False):
            r = ordenar(self.livros, 'nota_media', crescente, 'Quick Sort')
            self.assertEqual(sorted(self.ids(r)[-2:]), [2, 4])

    def test_radix_ano_igual_ao_merge_sort(self):
        for crescente in (True, False):
            self.assertEqual(self.ids(ordenar(self.livros, 'ano', crescente, 'Radix Sort MSD')),
                             self.ids(ordenar(self.livros, 'ano', crescente, 'Merge Sort')))

    def test_radix_somente_para_ano(self):
        with self.assertRaises(ValueError):
            ordenar(self.livros, 'titulo', True, 'Radix Sort MSD')

    def test_lista_vazia(self):
        for algoritmo in ('Heap Sort', 'Merge Sort', 'Quick Sort'):
            self.assertEqual(ordenar([], 'titulo', True, algoritmo), [])
        self.assertEqual(ordenar([], 'ano', True, 'Radix Sort MSD'), [])

    def test_empates_e_repetidos_nao_perdem_livros(self):
        repetidos = [livro(i, 'Mesmo', ano=2001) for i in range(1, 30)]
        for algoritmo, campo in (('Quick Sort', 'titulo'), ('Quick Sort', 'ano'), ('Radix Sort MSD', 'ano')):
            r = ordenar(repetidos, campo, False, algoritmo)
            self.assertEqual(sorted(self.ids(r)), list(range(1, 30)))

    def test_ordem_inversa_de_entrada(self):
        livros = [livro(i, f'T{i:03d}', ano=1000 + i) for i in range(100, 0, -1)]
        self.assertEqual(self.ids(ordenar(livros, 'titulo', True, 'Quick Sort')), list(range(1, 101)))
        self.assertEqual(self.ids(ordenar(livros, 'ano', True, 'Radix Sort MSD')), list(range(1, 101)))

    def test_campo_e_algoritmo_invalidos(self):
        with self.assertRaises(ValueError):
            ordenar(self.livros, 'preco', True, 'Quick Sort')
        with self.assertRaises(ValueError):
            ordenar(self.livros, 'titulo', True, 'Bubble Sort')


if __name__ == '__main__':
    unittest.main()
