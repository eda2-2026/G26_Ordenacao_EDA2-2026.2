"""Regras de negócio e persistência atômica em um único JSON."""
import copy
import json
import math
import os
import tempfile
from datetime import date, timedelta
from pathlib import Path

class Acervo:
    def __init__(self, arquivo):
        self.arquivo = Path(arquivo)
        self.dados = json.loads(self.arquivo.read_text(encoding='utf-8')) if self.arquivo.exists() else {'livros': [], 'leitores': [], 'emprestimos': []}

    def _commit(self, dados):
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)
        fd, nome = tempfile.mkstemp(dir=self.arquivo.parent, suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            os.replace(nome, self.arquivo)
        finally:
            if os.path.exists(nome): os.unlink(nome)
        self.dados = dados

    @staticmethod
    def _texto(value, campo):
        value = str(value).strip() if value is not None else ''
        if not value: raise ValueError(f'{campo} é obrigatório.')
        return value

    @staticmethod
    def _id(rows):
        return max((x['id'] for x in rows), default=0) + 1

    @staticmethod
    def _get(rows, id):
        for row in rows:
            if row['id'] == id: return row
        raise ValueError('Registro não encontrado.')

    def leitor(self, nome, matricula, contato, id=None):
        nome = self._texto(nome, 'Nome')
        matricula = self._texto(matricula, 'Matrícula')
        contato = self._texto(contato, 'Contato')
        data = copy.deepcopy(self.dados)
        if any(x['matricula'].casefold() == matricula.casefold() and x['id'] != id for x in data['leitores']):
            raise ValueError('Matrícula já cadastrada.')
        row = self._get(data['leitores'], id) if id is not None else {'id': self._id(data['leitores'])}
        row.update(nome=nome, matricula=matricula, contato=contato)
        if id is None: data['leitores'].append(row)
        self._commit(data)
        return row['id']

    def livro(self, titulo, autor, genero, ano, total, id=None):
        """Cadastra um livro (id=None) ou edita o livro de `id`. O ID nunca muda."""
        titulo = self._texto(titulo, 'Título'); autor = self._texto(autor, 'Autor')
        genero = self._texto(genero, 'Gênero')
        try: ano, total = int(ano), int(total)
        except (ValueError, TypeError): raise ValueError('Ano e exemplares devem ser inteiros.')
        if not 1 <= ano <= 9999 or total < 1: raise ValueError('Ano deve estar entre 1 e 9999; exemplares devem ser positivos.')
        data = copy.deepcopy(self.dados)
        if id is None:
            row = dict(id=self._id(data['livros']), titulo=titulo, autor=autor, genero=genero, ano=ano, total=total)
            data['livros'].append(row)
        else:
            row = self._get(data['livros'], id)
            emprestados = sum(x['livro_id'] == id and x['devolvido_em'] is None for x in data['emprestimos'])
            if total < emprestados:
                raise ValueError(f'Há {emprestados} exemplar(es) emprestado(s); o total não pode ser menor que isso.')
            row.update(titulo=titulo, autor=autor, genero=genero, ano=ano, total=total)
        self._commit(data)
        return row['id']

    def livros(self):
        result = copy.deepcopy(self.dados['livros'])
        for book in result:
            loans = [x for x in self.dados['emprestimos'] if x['livro_id'] == book['id']]
            book['disponiveis'] = book['total'] - sum(x['devolvido_em'] is None for x in loans)
            book['popularidade'] = len(loans)
            ratings = [x['nota'] for x in loans if x['nota'] is not None]
            book['nota_media'] = sum(ratings)/len(ratings) if ratings else None
        return result

    def emprestar(self, leitor_id, livro_id):
        self._get(self.dados['leitores'], leitor_id)
        book = self._get(self.livros(), livro_id)
        if book['disponiveis'] < 1: raise ValueError('Não há exemplar disponível.')
        if any(x['leitor_id'] == leitor_id and x['livro_id'] == livro_id and x['devolvido_em'] is None for x in self.dados['emprestimos']):
            raise ValueError('Este leitor já tem um empréstimo ativo desta obra.')
        data = copy.deepcopy(self.dados)
        row = dict(id=self._id(data['emprestimos']), leitor_id=leitor_id, livro_id=livro_id, emprestado_em=date.today().isoformat(), previsto_em=(date.today()+timedelta(days=14)).isoformat(), devolvido_em=None, nota=None)
        data['emprestimos'].append(row); self._commit(data)
        return row['id']

    def devolver(self, id, nota=None):
        if nota is not None:
            try: nota = float(nota)
            except (ValueError, TypeError): raise ValueError('Nota inválida.')
            if not math.isfinite(nota) or not 0 <= nota <= 5: raise ValueError('Nota deve estar entre 0 e 5.')
        data = copy.deepcopy(self.dados)
        row = self._get(data['emprestimos'], id)
        if row['devolvido_em'] is not None: raise ValueError('Empréstimo já devolvido.')
        row.update(devolvido_em=date.today().isoformat(), nota=nota)
        self._commit(data)

    def demonstracao(self):
        if any(self.dados.values()): return
        self.livro('Dom Casmurro', 'Machado de Assis', 'Romance', 1899, 2)
        self.livro('O Cortiço', 'Aluísio Azevedo', 'Romance', 1890, 1)
        self.livro('Capitães da Areia', 'Jorge Amado', 'Romance', 1937, 3)
        self.leitor('Ana Silva', '2026001', 'ana@example.com')
        self.leitor('Bruno Souza', '2026002', 'bruno@example.com')
        id = self.emprestar(1, 1); self.devolver(id, 4.5)
