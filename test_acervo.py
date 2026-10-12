import tempfile
import unittest
from pathlib import Path

from algoritmos import ordenar
from servico import Acervo


class TestAcervoLivros(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.arquivo = Path(self.tmp.name) / 'acervo.json'
        self.s = Acervo(self.arquivo)

    def tearDown(self):
        self.tmp.cleanup()

    def test_cadastro_gera_ids_unicos_e_sequenciais(self):
        a = self.s.livro('A', 'X', 'G', 2000, 1)
        b = self.s.livro('B', 'Y', 'G', 2001, 2)
        self.assertEqual((a, b), (1, 2))

    def test_cadastro_e_edicao_persistem_apos_reabrir(self):
        id = self.s.livro('Dom Casmurro', 'Machado', 'Romance', 1899, 2)
        self.s.livro('O Cortiço', 'Aluísio', 'Romance', 1890, 1)
        self.s.livro('Dom Casmurro (2ª ed.)', 'Machado de Assis', 'Romance', 1900, 4, id=id)
        outro = Acervo(self.arquivo)
        livros = {x['id']: x for x in outro.livros()}
        self.assertEqual(set(livros), {1, 2})
        self.assertEqual(livros[1]['titulo'], 'Dom Casmurro (2ª ed.)')
        self.assertEqual((livros[1]['autor'], livros[1]['ano'], livros[1]['total']), ('Machado de Assis', 1900, 4))
        self.assertEqual(livros[2]['titulo'], 'O Cortiço')

    def test_edicao_nao_cria_nem_remove_livros_e_mantem_id(self):
        id = self.s.livro('A', 'X', 'G', 2000, 1)
        self.assertEqual(self.s.livro('A2', 'X', 'G', 2000, 1, id=id), id)
        self.assertEqual(len(self.s.livros()), 1)

    def test_campos_obrigatorios_e_dominios(self):
        invalidos = [('', 'A', 'G', 2000, 1), ('T', ' ', 'G', 2000, 1), ('T', 'A', '', 2000, 1),
                     ('T', 'A', 'G', 'abc', 1), ('T', 'A', 'G', 2000, 'x'), ('T', 'A', 'G', 0, 1),
                     ('T', 'A', 'G', 10000, 1), ('T', 'A', 'G', 2000, 0), ('T', 'A', 'G', None, 1)]
        for args in invalidos:
            with self.assertRaises(ValueError, msg=repr(args)):
                self.s.livro(*args)
        self.assertEqual(self.s.livros(), [])
        self.assertFalse(self.arquivo.exists())

    def test_edicao_invalida_nao_altera_dados(self):
        id = self.s.livro('A', 'X', 'G', 2000, 2)
        with self.assertRaises(ValueError):
            self.s.livro('Novo', 'X', 'G', 'abc', 2, id=id)
        self.assertEqual(self.s.livros()[0]['titulo'], 'A')
        self.assertEqual(Acervo(self.arquivo).livros()[0]['titulo'], 'A')

    def test_editar_id_inexistente(self):
        with self.assertRaises(ValueError):
            self.s.livro('A', 'X', 'G', 2000, 1, id=99)

    def test_total_nao_pode_ficar_abaixo_dos_emprestimos_ativos(self):
        id = self.s.livro('A', 'X', 'G', 2000, 3)
        self.s.leitor('Ana', '1', 'a@x.com'); self.s.leitor('Bia', '2', 'b@x.com')
        self.s.emprestar(1, id); self.s.emprestar(2, id)
        with self.assertRaises(ValueError):
            self.s.livro('A', 'X', 'G', 2000, 1, id=id)
        self.s.livro('A', 'X', 'G', 2000, 2, id=id)
        self.assertEqual(self.s.livros()[0]['disponiveis'], 0)
        self.s.livro('A', 'X', 'G', 2000, 5, id=id)
        self.assertEqual(self.s.livros()[0]['disponiveis'], 3)

    def test_emprestimo_devolvido_nao_trava_reducao_do_total(self):
        id = self.s.livro('A', 'X', 'G', 2000, 2)
        self.s.leitor('Ana', '1', 'a@x.com')
        self.s.devolver(self.s.emprestar(1, id), 4)
        self.s.livro('A', 'X', 'G', 2000, 1, id=id)
        self.assertEqual(self.s.livros()[0]['disponiveis'], 1)

    def test_ordenacao_reflete_cadastro_e_edicao_e_preserva_id(self):
        a = self.s.livro('Beta', 'X', 'G', 2000, 1)
        b = self.s.livro('Alfa', 'Y', 'G', 1990, 1)
        for algoritmo, campo in (('Quick Sort', 'titulo'), ('Radix Sort MSD', 'ano')):
            self.assertEqual([x['id'] for x in ordenar(self.s.livros(), campo, True, algoritmo)], [b, a])
        c = self.s.livro('Aaa', 'Z', 'G', 1800, 1)
        self.s.livro('Zzz', 'X', 'G', 2010, 1, id=b)
        por_titulo = ordenar(self.s.livros(), 'titulo', True, 'Quick Sort')
        self.assertEqual([x['id'] for x in por_titulo], [c, a, b])
        por_ano = ordenar(self.s.livros(), 'ano', False, 'Radix Sort MSD')
        self.assertEqual([x['id'] for x in por_ano], [b, a, c])
        self.assertEqual(por_ano[0]['titulo'], 'Zzz')

    def test_ordenar_acervo_vazio(self):
        self.assertEqual(ordenar(self.s.livros(), 'titulo', True, 'Quick Sort'), [])
        self.assertEqual(ordenar(self.s.livros(), 'ano', True, 'Radix Sort MSD'), [])


if __name__ == '__main__':
    unittest.main()
