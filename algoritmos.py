"""Algoritmos próprios; não alteram a entrada."""

def heap_sort(items, key=lambda x: x, reverse=False):
    data = list(items)
    def greater(a, b):
        return key(a) < key(b) if reverse else key(a) > key(b)
    def sift(root, size):
        while 2 * root + 1 < size:
            child = 2 * root + 1
            if child + 1 < size and greater(data[child + 1], data[child]):
                child += 1
            if not greater(data[child], data[root]):
                break
            data[root], data[child] = data[child], data[root]
            root = child
    for root in range(len(data)//2 - 1, -1, -1):
        sift(root, len(data))
    for end in range(len(data)-1, 0, -1):
        data[0], data[end] = data[end], data[0]
        sift(0, end)
    return data

def merge_sort(items, key=lambda x: x, reverse=False):
    data = list(items)
    if len(data) < 2:
        return data
    middle = len(data)//2
    left = merge_sort(data[:middle], key, reverse)
    right = merge_sort(data[middle:], key, reverse)
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        take_left = key(left[i]) >= key(right[j]) if reverse else key(left[i]) <= key(right[j])
        if take_left:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]

def quick_sort(items, key=lambda x: x, reverse=False):
    # Quick Sort iterativo com partição em três vias e pivô mediana de três cresce no máximo O(log n).

    pares = [(key(x), x) for x in items]
    def antes(a, b):
        return a > b if reverse else a < b
    def mediana(a, b, c):
        if antes(a, b):
            if antes(b, c): return b
            return c if antes(a, c) else a
        if antes(a, c): return a
        return c if antes(b, c) else b
    pilha = [(0, len(pares) - 1)]
    while pilha:
        lo, hi = pilha.pop()
        while lo < hi:
            pivo = mediana(pares[lo][0], pares[(lo + hi) // 2][0], pares[hi][0])
            menor, i, maior = lo, lo, hi
            while i <= maior:
                k = pares[i][0]
                if antes(k, pivo):
                    pares[menor], pares[i] = pares[i], pares[menor]; menor += 1; i += 1
                elif antes(pivo, k):
                    pares[i], pares[maior] = pares[maior], pares[i]; maior -= 1
                else:
                    i += 1
            # [lo, menor) antes do pivô; [menor, maior] iguais ao pivô; (maior, hi] depois
            if menor - lo < hi - maior:
                pilha.append((maior + 1, hi)); hi = menor - 1
            else:
                pilha.append((lo, menor - 1)); lo = maior + 1
    return [item for _, item in pares]

def radix_sort_msd(items, key=lambda x: x, reverse=False, digitos=4):
    # Radix Sort MSD em base 10 para inteiros de 0 a 10**digitos - 1.

    limite = 10 ** digitos
    pares = []
    for item in items:
        k = key(item)
        if isinstance(k, bool) or not isinstance(k, int) or not 0 <= k < limite:
            raise ValueError(f'Radix Sort MSD aceita inteiros de 0 a {limite - 1}.')
        pares.append((k, item))
    resultado = []
    def distribuir(grupo, posicao):
        if len(grupo) < 2 or posicao < 0:
            resultado.extend(item for _, item in grupo); return
        baldes = [[] for _ in range(10)]
        for par in grupo:
            baldes[(par[0] // 10 ** posicao) % 10].append(par)
        for d in (range(9, -1, -1) if reverse else range(10)):
            if baldes[d]: distribuir(baldes[d], posicao - 1)
    distribuir(pares, digitos - 1)
    return resultado

def ordenar(livros, campo='titulo', crescente=True, algoritmo='Merge Sort'):
    if campo not in {'id', 'titulo', 'autor', 'genero', 'ano', 'disponiveis', 'popularidade', 'nota_media'}:
        raise ValueError('Campo de ordenação inválido.')
    if algoritmo not in ALGORITMOS:
        raise ValueError('Algoritmo inválido.')
    if algoritmo == 'Radix Sort MSD' and campo != 'ano':
        raise ValueError('Radix Sort MSD ordena apenas o campo ano.')
    with_value = [x for x in livros if x.get(campo) is not None]
    missing = [x for x in livros if x.get(campo) is None]
    def key(item):
        value = item[campo]
        return value.casefold() if isinstance(value, str) else value
    sort = ALGORITMOS[algoritmo]
    return sort(with_value, key=key, reverse=not crescente) + missing

ALGORITMOS = {'Heap Sort': heap_sort, 'Merge Sort': merge_sort, 'Quick Sort': quick_sort, 'Radix Sort MSD': radix_sort_msd}
