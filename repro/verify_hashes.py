#!/usr/bin/env python3
"""Coteja los diez MP4 contra el manifiesto de hashes.

Uso:
    python verify_hashes.py --media RUTA_A_APP_MEDIA
    python verify_hashes.py --media RUTA --manifest otro.csv --json salida.json

Devuelve 0 si los diez archivos existen y coinciden; 1 en caso contrario.
"""

import argparse
import csv
import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def sha256(ruta, bloque=1 << 20):
    h = hashlib.sha256()
    with open(ruta, 'rb') as f:
        for trozo in iter(lambda: f.read(bloque), b''):
            h.update(trozo)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--media', required=True, help='Carpeta que contiene los diez MP4')
    p.add_argument('--manifest', default=os.path.join(AQUI, 'manifest.csv'))
    p.add_argument('--json', help='Guardar el resultado en JSON')
    args = p.parse_args()

    with open(args.manifest, encoding='utf-8-sig') as f:
        filas = list(csv.DictReader(f))

    resultados = []
    fallos = 0
    ancho = max(len(r['archivo']) for r in filas) + 2
    print(f"{'archivo':<{ancho}}{'bytes':>10}  {'sha256':<16}  estado")
    print('-' * (ancho + 40))

    for r in filas:
        ruta = os.path.join(args.media, r['archivo'])
        if not os.path.exists(ruta):
            estado = 'FALTA'
            got, tam = None, None
        else:
            got = sha256(ruta)
            tam = os.path.getsize(ruta)
            if got != r['sha256']:
                estado = 'DIFERENTE'
            elif tam != int(r['bytes']):
                estado = 'TAMAÑO DISTINTO'
            else:
                estado = 'OK'
        if estado != 'OK':
            fallos += 1
        print(f"{r['archivo']:<{ancho}}{str(tam or '-'):>10}  {(got or '-')[:16]:<16}  {estado}")
        resultados.append({
            'archivo': r['archivo'],
            'sha256_esperado': r['sha256'],
            'sha256_obtenido': got,
            'bytes_esperados': int(r['bytes']),
            'bytes_obtenidos': tam,
            'estado': estado,
        })

    print(f"\nCoincidencias: {len(filas) - fallos}/{len(filas)}")
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        print(f"Resultado guardado en {args.json}")
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.exit(main())
