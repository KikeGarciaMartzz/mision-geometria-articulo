#!/usr/bin/env python3
"""Recalcula la duración autorada de la introducción de la Misión 3.

Toma las duraciones reales de los WAV por parlamento y las reglas de montaje
documentadas (0,55 s antes del primer parlamento, 0,55 s entre parlamentos,
0,45 s de cola final), y las compara con tools/sync.json y con el MP4.

Uso:
    python recompute_timing.py --proyecto C:/ruta/video-mision-3
    python recompute_timing.py --proyecto C:/ruta/video-mision-3 --mp4 C:/ruta/mision03.mp4

Devuelve 0 si los valores coinciden dentro de la tolerancia; 1 en caso contrario.
"""

import argparse
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
LEAD = 0.55
GAP = 0.55
TAIL = 0.45
TOLERANCIA = 1e-3


def duracion_mp4(ffprobe, ruta):
    res = subprocess.run(
        [ffprobe, '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', ruta],
        capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip())
    return float(res.stdout.strip())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--proyecto', required=True, help='Carpeta video-mision-3')
    p.add_argument('--mp4', help='MP4 integrado, para comparar la duración del contenedor')
    p.add_argument('--ffprobe', default='ffprobe')
    p.add_argument('--expected', default=os.path.join(AQUI, 'expected', 'timing-m3.json'))
    args = p.parse_args()

    sync_path = os.path.join(args.proyecto, 'tools', 'sync.json')
    dur_path = os.path.join(args.proyecto, 'assets', 'voice', 'duraciones.json')
    sync = json.load(open(sync_path, encoding='utf-8'))
    lineas = json.load(open(dur_path, encoding='utf-8'))

    inicios = []
    t = LEAD
    for linea in lineas:
        inicios.append(round(t, 6))
        t += float(linea['duration']) + GAP
    fin = round(t + TAIL, 6)

    print(f"{'parlamento':<12}{'hablante':<10}{'duración':>10}{'inicio':>12}")
    for linea, ini in zip(lineas, inicios):
        print(f"{linea['id']:<12}{linea['speaker']:<10}{linea['duration']:>10.4f}{ini:>12.4f}")

    print(f"\nDuración autorada recalculada: {fin:.5f} s")
    print(f"Duración declarada en sync.json: {sync['duration']:.5f} s")

    ok = abs(fin - float(sync['duration'])) <= TOLERANCIA
    if not ok:
        print('  DISCREPANCIA con sync.json')

    desfase = max(abs(a - b) for a, b in zip(inicios, sync['line_starts']))
    print(f"Desfase máximo en los inicios de parlamento: {desfase * 1000:.2f} ms")
    if desfase > TOLERANCIA:
        ok = False

    if args.mp4:
        d = duracion_mp4(args.ffprobe, args.mp4)
        print(f"Duración del contenedor MP4: {d:.5f} s (diferencia {abs(d - fin) * 1000:.1f} ms)")
        if abs(d - fin) > 0.05:
            ok = False

    if os.path.exists(args.expected):
        exp = json.load(open(args.expected, encoding='utf-8'))
        print(f"Duración esperada en expected/: {exp['duracion_autorada']:.5f} s")
        if abs(exp['duracion_autorada'] - fin) > TOLERANCIA:
            ok = False

    print('\nRESULTADO:', 'OK' if ok else 'FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
