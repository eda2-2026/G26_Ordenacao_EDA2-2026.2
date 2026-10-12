"""Integração dos formulários com o serviço em uma janela oculta."""
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch
from app import App
from servico import Acervo

class InterfaceTest(unittest.TestCase):
    def test_fluxo_dos_formularios(self):
        with tempfile.TemporaryDirectory() as folder:
            root=tk.Tk(); root.withdraw()
            try:
                app=App(root,Acervo(Path(folder)/'test.json'))
                for key,value in [('Título','Livro UI'),('Autor','Autor'),('Gênero','Romance'),('Ano','2000'),('Exemplares','1')]: app.bvars[key].set(value)
                app.save_book()
                for key,value in [('Nome','Ana UI'),('Matrícula','1'),('Contato','ana@example.com')]: app.rvars[key].set(value)
                app.save_reader(); app.refresh(); root.update_idletasks()
                self.assertEqual(len(app.booktree.get_children()),1)
                app.readertree.selection_set('1'); app.edit_reader()
                app.rvars['Nome'].set('Ana Editada'); app.save_reader(); app.refresh()
                self.assertEqual(app.service.dados['leitores'][0]['nome'],'Ana Editada')
                app.readerbox.current(0); app.bookbox.current(0); app.borrow(); app.refresh()
                self.assertEqual(app.service.livros()[0]['disponiveis'],0)
                app.loantree.selection_set('1'); app.rating.set('4,5'); app.return_book(); app.refresh()
                self.assertEqual(app.service.livros()[0]['nota_media'],4.5)
                for algorithm in ('Heap Sort','Merge Sort'):
                    for direction in ('Crescente','Decrescente'):
                        app.algorithm.set(algorithm); app.direction.set(direction); app.refresh_books()
                        self.assertEqual(len(app.booktree.get_children()),1)
                app.loantree.selection_set('1')
                with patch('app.messagebox.showerror') as error:
                    app.act(app.return_book); error.assert_called_once()
                self.assertEqual(Acervo(app.service.arquivo).livros()[0]['disponiveis'],1)
            finally: root.destroy()
