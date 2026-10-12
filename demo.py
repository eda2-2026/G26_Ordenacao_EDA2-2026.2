"""Cria uma base de demonstração

Uso (dentro da pasta do projeto):
    python3 popular_demo.py                  # ~45 livros reais, 8 leitores, empréstimos e notas
    python3 popular_demo.py --extra 500      # adiciona 500 livros sintéticos para testar escala
    python3 app.py --dados dados/demo.json   # abre o programa com essa base

O arquivo dados/demo.json é recriado a cada execução; os dados reais (acervo.json) não são tocados.
"""
import argparse
import random
from pathlib import Path

from servico import Acervo

LIVROS = [
    # título, autor, gênero, ano, exemplares
    ('Dom Casmurro', 'Machado de Assis', 'Romance', 1899, 3),
    ('Memórias Póstumas de Brás Cubas', 'Machado de Assis', 'Romance', 1881, 2),
    ('Quincas Borba', 'Machado de Assis', 'Romance', 1891, 1),
    ('O Cortiço', 'Aluísio Azevedo', 'Romance', 1890, 1),
    ('O Guarani', 'José de Alencar', 'Romance', 1857, 2),
    ('Iracema', 'José de Alencar', 'Romance', 1865, 3),
    ('Senhora', 'José de Alencar', 'Romance', 1875, 1),
    ('O Ateneu', 'Raul Pompeia', 'Romance', 1888, 2),
    ('Vidas Secas', 'Graciliano Ramos', 'Romance', 1938, 4),
    ('São Bernardo', 'Graciliano Ramos', 'Romance', 1934, 2),
    ('Capitães da Areia', 'Jorge Amado', 'Romance', 1937, 3),
    ('Gabriela, Cravo e Canela', 'Jorge Amado', 'Romance', 1958, 2),
    ('Grande Sertão: Veredas', 'Guimarães Rosa', 'Romance', 1956, 2),
    ('Sagarana', 'Guimarães Rosa', 'Contos', 1946, 1),
    ('A Hora da Estrela', 'Clarice Lispector', 'Romance', 1977, 3),
    ('Perto do Coração Selvagem', 'Clarice Lispector', 'Romance', 1943, 2),
    ('O Quinze', 'Rachel de Queiroz', 'Romance', 1930, 2),
    ('Macunaíma', 'Mário de Andrade', 'Romance', 1928, 1),
    ('Triste Fim de Policarpo Quaresma', 'Lima Barreto', 'Romance', 1915, 2),
    ('Casa-Grande & Senzala', 'Gilberto Freyre', 'Ensaio', 1933, 1),
    ('Dom Quixote', 'Miguel de Cervantes', 'Romance', 1605, 2),
    ('1984', 'George Orwell', 'Ficção científica', 1949, 5),
    ('A Revolução dos Bichos', 'George Orwell', 'Sátira', 1945, 4),
    ('Fahrenheit 451', 'Ray Bradbury', 'Ficção científica', 1953, 3),
    ('Admirável Mundo Novo', 'Aldous Huxley', 'Ficção científica', 1932, 3),
    ('O Hobbit', 'J. R. R. Tolkien', 'Fantasia', 1937, 4),
    ('O Senhor dos Anéis', 'J. R. R. Tolkien', 'Fantasia', 1954, 3),
    ('Orgulho e Preconceito', 'Jane Austen', 'Romance', 1813, 3),
    ('Frankenstein', 'Mary Shelley', 'Terror', 1818, 2),
    ('Drácula', 'Bram Stoker', 'Terror', 1897, 2),
    ('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 'Infantil', 1943, 5),
    ('Alice no País das Maravilhas', 'Lewis Carroll', 'Fantasia', 1865, 3),
    ('O Morro dos Ventos Uivantes', 'Emily Brontë', 'Romance', 1847, 1),
    ('Crime e Castigo', 'Fiódor Dostoiévski', 'Romance', 1866, 2),
    ('Os Miseráveis', 'Victor Hugo', 'Romance', 1862, 2),
    ('A Metamorfose', 'Franz Kafka', 'Ficção', 1915, 3),
    ('O Estrangeiro', 'Albert Camus', 'Romance', 1942, 2),
    ('Cem Anos de Solidão', 'Gabriel García Márquez', 'Romance', 1967, 3),
    ('Ensaio sobre a Cegueira', 'José Saramago', 'Romance', 1995, 2),
    ('O Alquimista', 'Paulo Coelho', 'Romance', 1988, 4),
    ('Introduction to Algorithms', 'Thomas H. Cormen et al.', 'Técnico', 1990, 2),
    ('The Art of Computer Programming, Vol. 3', 'Donald Knuth', 'Técnico', 1973, 1),
]

LEITORES = [
    ('Ana Silva', 'ana@example.com'), ('Bruno Souza', 'bruno@example.com'),
    ('Carla Mendes', 'carla@example.com'), ('Diego Lima', 'diego@example.com'),
    ('Elisa Rocha', 'elisa@example.com'), ('Felipe Costa', 'felipe@example.com'),
    ('Giulia Prado', 'giulia@example.com'), ('Hugo Alves', 'hugo@example.com'),
]

SILABAS = ['ca', 'lu', 'mar', 'ven', 'to', 'sol', 'nor', 'de', 'ri', 'a', 'fo', 'gen', 'pa', 'lis', 'tra', 'mon']
GENEROS = ['Romance', 'Contos', 'Ficção científica', 'Fantasia', 'Terror', 'Ensaio', 'Técnico', 'Infantil']


def palavra(rng):
    return ''.join(rng.choice(SILABAS) for _ in range(rng.randint(2, 4))).capitalize()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--extra', type=int, default=0, help='livros sintéticos adicionais')
    p.add_argument('--saida', type=Path, default=Path(__file__).parent / 'dados' / 'demo.json')
    args = p.parse_args()
    rng = random.Random(26)
    if args.saida.exists():
        args.saida.unlink()
    s = Acervo(args.saida)

    for titulo, autor, genero, ano, total in LIVROS:
        s.livro(titulo, autor, genero, ano, total)
    for i in range(args.extra):
        s.livro(f'{palavra(rng)} {palavra(rng)}', f'{palavra(rng)} {palavra(rng)}',
                rng.choice(GENEROS), rng.randint(1500, 2025), rng.randint(1, 5))
    for i, (nome, contato) in enumerate(LEITORES, start=1):
        s.leitor(nome, f'2026{i:03d}', contato)

    # Histórico: empréstimos devolvidos (alguns com nota, outros sem) e alguns ainda ativos.
    livros = s.livros()
    for livro in livros[:len(LIVROS)]:
        for leitor_id in rng.sample(range(1, len(LEITORES) + 1), rng.randint(0, 5)):
            id = s.emprestar(leitor_id, livro['id'])
            s.devolver(id, rng.choice([None, 2, 3, 3.5, 4, 4.5, 5]))
    for livro in rng.sample(livros[:len(LIVROS)], 8):
        try:
            s.emprestar(rng.randint(1, len(LEITORES)), livro['id'])
        except ValueError:
            pass

    final = s.livros()
    com_nota = sum(b['nota_media'] is not None for b in final)
    print(f'{args.saida}: {len(final)} livros ({com_nota} com nota), {len(s.dados["leitores"])} leitores, '
          f'{len(s.dados["emprestimos"])} empréstimos')


if __name__ == '__main__':
    main()
