import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from algoritmos import heap_sort, merge_sort, ordenar
from servico import Acervo

class ServicoTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'acervo.json'; self.s=Acervo(self.path)
        self.book=self.s.livro('Livro','Autor','Romance',2000,1)
        self.reader=self.s.leitor('Ana','001','ana@example.com')
        self.other=self.s.leitor('Bruno','002','bruno@example.com')

    def test_fluxo_persistente(self):
        loan=self.s.emprestar(self.reader,self.book)
        self.assertEqual(self.s.livros()[0]['disponiveis'],0)
        with self.assertRaises(ValueError): self.s.emprestar(self.other,self.book)
        self.s.devolver(loan,0)
        book=Acervo(self.path).livros()[0]
        self.assertEqual((book['disponiveis'],book['popularidade'],book['nota_media']),(1,1,0))
        with self.assertRaises(ValueError): self.s.devolver(loan,5)
        self.assertEqual(self.s.livros()[0]['nota_media'],0)

    def test_media_e_devolucao_sem_nota(self):
        for rating in (4,5,None): self.s.devolver(self.s.emprestar(self.reader,self.book),rating)
        self.assertEqual(self.s.livros()[0]['nota_media'],4.5)
        self.assertEqual(self.s.livros()[0]['popularidade'],3)

    def test_validacoes_nao_alteram_dados(self):
        loan=self.s.emprestar(self.reader,self.book)
        original=self.path.read_bytes()
        for nota in (-1,6,'abc',float('nan'),float('inf')):
            with self.assertRaises(ValueError): self.s.devolver(loan,nota)
            self.assertEqual(self.path.read_bytes(),original)
        for nome,matricula,contato in [('', '3','x'),('X','001','x'),('X','','x'),('X','3','')]:
            with self.assertRaises(ValueError): self.s.leitor(nome,matricula,contato)
        self.assertEqual(self.path.read_bytes(),original)

    def test_edicao_id_e_matricula(self):
        self.s.leitor('Ana editada','001','novo',id=self.reader)
        self.assertEqual(self.s.dados['leitores'][0]['id'],self.reader)
        with self.assertRaises(ValueError): self.s.leitor('Ana','002','novo',id=self.reader)
        with self.assertRaises(ValueError): self.s.leitor('X','3','x',id=99)

    def test_referencias_e_duplicidade(self):
        self.s.livro('Outro','Autor','Romance',2000,2)
        self.s.emprestar(self.reader,2)
        with self.assertRaises(ValueError): self.s.emprestar(self.reader,2)
        for reader,book in [(99,1),(1,99)]:
            with self.assertRaises(ValueError): self.s.emprestar(reader,book)
        with self.assertRaises(ValueError): self.s.devolver(99)

    def test_erro_gravacao_preserva_estado(self):
        original=json.loads(self.path.read_text(encoding='utf-8'))
        with patch('servico.os.replace',side_effect=OSError('Falha simulada')):
            with self.assertRaises(OSError): self.s.emprestar(self.reader,self.book)
        self.assertEqual(self.s.dados,original)
        self.assertEqual(json.loads(self.path.read_text(encoding='utf-8')),original)
        self.assertEqual(list(self.path.parent.glob('*.tmp')),[])

    def test_validacao_livros(self):
        for year,total in [('abc',1),(0,1),(2000,0),(2000,-1)]:
            with self.assertRaises(ValueError): self.s.livro('X','Y','Z',year,total)

    def test_demonstracao_idempotente(self):
        path=Path(self.temp.name)/'demo.json'; s=Acervo(path); s.demonstracao()
        original=path.read_bytes(); s.demonstracao(); self.assertEqual(path.read_bytes(),original)
        self.assertEqual(len(s.livros()),3)

if __name__=='__main__': unittest.main()

