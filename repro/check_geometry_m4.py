#!/usr/bin/env python3
"""Verifica los fotogramas y los criterios de la corrección geométrica de la Misión 4.

Qué hace:
  1. Extrae los cuatro fotogramas documentados (44,000 / 48,200 / 50,030 / 52,587 s)
     del MP4 y calcula el SHA-256 de los píxeles RGB, sin depender del codificador PNG.
  2. Compara esos hashes con los de expected/qa-m4.json.
  3. Revisa que las mediciones archivadas cumplan los cuatro criterios del informe.

Qué no hace:
  No vuelve a detectar agujas ni rótulos con visión por computadora. Comprueba que
  los fotogramas analizados son los mismos y que los criterios registrados se cumplen
  con las mediciones conservadas.

Uso:
    python check_geometry_m4.py --mp4 C:/ruta/mision04.mp4
    python check_geometry_m4.py --mp4 C:/ruta/mision04.mp4 --ffmpeg C:/ruta/ffmpeg.exe

Devuelve 0 si todo coincide; 1 en caso contrario.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CRITERIOS = {
    'vertice_aguja_vs_centro_px_max': 2.0,
}
TOL_HASH = 0


def hash_fotograma(ffmpeg, mp4, segundo):
    cmd = [ffmpeg, '-v', 'error', '-ss', str(segundo), '-i', mp4,
           '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.decode('utf-8', 'replace')[:400])
    return hashlib.sha256(res.stdout).hexdigest(), len(res.stdout)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mp4', required=True)
    p.add_argument('--ffmpeg', default='ffmpeg')
    p.add_argument('--expected', default=os.path.join(AQUI, 'expected', 'qa-m4.json'))
    args = p.parse_args()

    exp = json.load(open(args.expected, encoding='utf-8'))
    ok = True

    print('Fotogramas')
    for muestra in exp['fotogramas']:
        got, n = hash_fotograma(args.ffmpeg, args.mp4, muestra['segundo'])
        coincide = got == muestra['raw_rgb24_sha256']
        ok = ok and coincide
        print(f"  {muestra['segundo']:>7} s  {'OK' if coincide else 'DIFERENTE'}  {got[:16]}  ({n} bytes)")

    print('\nCriterios registrados')
    for c in exp['criterios']:
        nombre, valor = c['nombre'], c['valor']
        if nombre == 'vertice_aguja_vs_centro_px':
            cumple = valor <= CRITERIOS['vertice_aguja_vs_centro_px_max']
        elif nombre == 'etiquetas_ocluidas':
            cumple = len(valor) == 0
        else:
            cumple = bool(valor)
        ok = ok and cumple
        print(f"  {nombre:<38} {str(valor):<10} {'OK' if cumple else 'FALLA'}")

    print('\nRESULTADO:', 'OK' if ok else 'FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
