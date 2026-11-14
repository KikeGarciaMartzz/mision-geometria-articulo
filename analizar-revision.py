"""Acuerdo por criterio entre dos matrices de revisión.

No rellena datos faltantes ni mezcla consenso con evaluación. Los códigos
NA y NE, y las celdas vacías, se cuentan aparte y nunca entran al cálculo
como aprobación.

Uso:
    python analizar-revision.py --r1 evaluacion-R1.csv --r2 evaluacion-R2.csv --out acuerdo.json
"""

import argparse
import csv
import json
from collections import Counter

VALIDOS = {'', 'OK', 'LEVE', 'GRAVE', 'NA', 'NE'}
PESO = {'OK': 0, 'LEVE': 1, 'GRAVE': 2}
NIVELES = (0, 1, 2)


def leer(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        filas = list(csv.DictReader(f))
    resultado = {}
    for r in filas:
        clave = (r['video'], r['sha256'], r['criterio'])
        if clave in resultado:
            raise ValueError('Fila duplicada: %s' % (clave,))
        valor = (r.get('valor') or '').strip().upper()
        if valor not in VALIDOS:
            raise ValueError('Código no válido: %r en %s' % (valor, clave))
        if valor in ('LEVE', 'GRAVE') and not (r.get('id_defecto') or '').strip():
            raise ValueError('Falta el identificador de defecto para %s' % (clave,))
        resultado[clave] = valor
    return resultado


def resumir(a, b):
    if set(a) != set(b):
        raise ValueError('Las matrices difieren en videos, hashes o criterios')
    salida = {}
    for criterio in sorted({k[2] for k in a}):
        claves = [k for k in a if k[2] == criterio]
        pares = [(PESO[a[k]], PESO[b[k]]) for k in claves
                 if a[k] in PESO and b[k] in PESO]
        n = len(pares)

        exactos = sum(1 for x, y in pares if x == y)

        kappa = None
        if n:
            ca = Counter(x for x, y in pares)
            cb = Counter(y for x, y in pares)
            observado = sum(abs(x - y) / 2.0 for x, y in pares) / n
            esperado = sum(ca[i] * cb[j] * abs(i - j) / 2.0
                           for i in NIVELES for j in NIVELES) / float(n * n)
            if esperado > 0:
                kappa = 1 - observado / esperado

        salida[criterio] = {
            'videos': len(claves),
            'pares_computables': n,
            'acuerdos_exactos': exactos,
            'proporcion_acuerdo': (exactos / n) if n else None,
            'kappa_ponderado_descriptivo': kappa,
            'codigos_R1': dict(Counter(a[k] or 'faltante' for k in claves)),
            'codigos_R2': dict(Counter(b[k] or 'faltante' for k in claves)),
        }
    return salida


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--r1', required=True)
    p.add_argument('--r2', required=True)
    p.add_argument('--out', required=True)
    args = p.parse_args()

    criterios = resumir(leer(args.r1), leer(args.r2))
    resultado = {
        'nota': ('Descriptivo por criterio. Escala OK/Leve/Grave; NA, NE y vacías '
                 'quedan fuera del cálculo. Kappa ponderado lineal, inestable con '
                 'diez videos. null significa no estimable.'),
        'criterios': criterios,
    }
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    total = sum(r['pares_computables'] for r in criterios.values())
    print('Pares computables:', total)
    for c, r in criterios.items():
        print('  %-3s %2d videos  acuerdo=%-5s kappa=%s' % (
            c, r['videos'],
            ('%.2f' % r['proporcion_acuerdo']) if r['proporcion_acuerdo'] is not None else '-',
            ('%.2f' % r['kappa_ponderado_descriptivo']) if r['kappa_ponderado_descriptivo'] is not None else '-'))


if __name__ == '__main__':
    main()
