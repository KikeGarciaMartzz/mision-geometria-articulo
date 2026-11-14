#!/usr/bin/env python3
"""Decodifica los diez MP4 en modo de error estricto.

Uso:
    python decode_all.py --media RUTA_A_APP_MEDIA
    python decode_all.py --media RUTA --ffmpeg C:/ruta/ffmpeg.exe

Reproduce la comprobación reportada en el artículo:
    ffmpeg -v error -xerror -threads 2 -i MP4 -map 0:v:0 -map 0:a:0 -f null -

Devuelve 0 si los diez archivos decodifican sin errores; 1 en caso contrario.
"""

import argparse
import csv
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--media', required=True)
    p.add_argument('--ffmpeg', default='ffmpeg')
    p.add_argument('--manifest', default=os.path.join(AQUI, 'manifest.csv'))
    args = p.parse_args()

    with open(args.manifest, encoding='utf-8-sig') as f:
        filas = list(csv.DictReader(f))

    fallos = 0
    for r in filas:
        ruta = os.path.join(args.media, r['archivo'])
        if not os.path.exists(ruta):
            print(f"{r['archivo']:<20} FALTA")
            fallos += 1
            continue
        cmd = [args.ffmpeg, '-v', 'error', '-xerror', '-threads', '2',
               '-i', ruta, '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-']
        res = subprocess.run(cmd, capture_output=True, text=True)
        salida = (res.stderr or '').strip()
        if res.returncode == 0 and not salida:
            print(f"{r['archivo']:<20} OK")
        else:
            print(f"{r['archivo']:<20} ERROR ({res.returncode})")
            if salida:
                print('   ' + salida.replace('\n', '\n   ')[:800])
            fallos += 1

    print(f"\nDecodifican sin errores: {len(filas) - fallos}/{len(filas)}")
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.exit(main())
