import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from algoritmos import heap_sort, merge_sort, ordenar
from servico import Acervo

class AlgoritmosTest(unittest.TestCase):
    def test_ordem_e_preservacao(self):
        rng=random.Random(41)
        for algorithm in (heap_sort,merge_sort):
            for data in ([],[1],[3,3,1,2],list(range(100)),list(range(100,-1,-1)),[rng.randint(-100,100) for _ in range(1000)]):
                original=data[:]
                for reverse in (False,True): self.assertEqual(algorithm(data,reverse=reverse),sorted(data,reverse=reverse))
                self.assertEqual(data,original)

    def test_merge_estavel_nos_dois_sentidos(self):
        rows=[(2,'a'),(1,'b'),(2,'c'),(1,'d')]
        for reverse in (False,True):
            self.assertEqual(merge_sort(rows,key=lambda x:x[0],reverse=reverse),sorted(rows,key=lambda x:x[0],reverse=reverse))

    def test_notas_e_ausentes(self):
        rows=[{'id':1,'nota_media':None},{'id':2,'nota_media':0},{'id':3,'nota_media':4.5}]
        for algorithm in ('Heap Sort','Merge Sort'):
            self.assertEqual([x['id'] for x in ordenar(rows,'nota_media',True,algorithm)],[2,3,1])
            self.assertEqual([x['id'] for x in ordenar(rows,'nota_media',False,algorithm)],[3,2,1])

    def test_texto_e_parametros(self):
        self.assertEqual([x['titulo'] for x in ordenar([{'titulo':'z'},{'titulo':'Ana'}])],['Ana','z'])
        with self.assertRaises(ValueError): ordenar([], 'inexistente')
        with self.assertRaises(ValueError): ordenar([], algoritmo='inexistente')


if __name__=='__main__': unittest.main()

