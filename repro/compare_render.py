#!/usr/bin/env python3
"""Compara un render re-ejecutado contra el render de referencia.

No exige identidad binaria: mide si el MP4 nuevo dura lo mismo, si el audio
coincide muestra a muestra y cuánto se parecen los fotogramas.

Uso:
    python compare_render.py --ref renders/original.mp4 --new renders/replica.mp4

Devuelve 0 si duración y audio coinciden y el SSIM medio supera 0.99; 1 si no.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys


def duracion(ffprobe, ruta):
    res = subprocess.run(
        [ffprobe, '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', ruta],
        capture_output=True, text=True)
    return float(res.stdout.strip())


def pcm(ffmpeg, ruta):
    """Decodifica el primer flujo de audio a PCM 16 bits y lo resume."""
    res = subprocess.run(
        [ffmpeg, '-v', 'error', '-i', ruta, '-map', '0:a:0',
         '-f', 's16le', '-acodec', 'pcm_s16le', '-'],
        capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.decode('utf-8', 'replace')[:300])
    return res.stdout


def ssim(ffmpeg, ref, new):
    """SSIM medio entre los dos videos, calculado por FFmpeg."""
    res = subprocess.run(
        [ffmpeg, '-v', 'info', '-i', new, '-i', ref,
         '-lavfi', '[0:v][1:v]ssim', '-f', 'null', '-'],
        capture_output=True, text=True)
    salida = res.stderr or ''
    m = re.search(r'All:\s*([0-9.]+)', salida)
    lineas = [l for l in salida.splitlines() if 'SSIM' in l]
    return (float(m.group(1)) if m else None), (lineas[-1].strip() if lineas else '')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ref', required=True)
    p.add_argument('--new', required=True)
    p.add_argument('--ffmpeg', default='ffmpeg')
    p.add_argument('--ffprobe', default='ffprobe')
    p.add_argument('--json')
    args = p.parse_args()

    d_ref = duracion(args.ffprobe, args.ref)
    d_new = duracion(args.ffprobe, args.new)
    a_ref = pcm(args.ffmpeg, args.ref)
    a_new = pcm(args.ffmpeg, args.new)
    s, linea = ssim(args.ffmpeg, args.ref, args.new)

    h_ref = hashlib.sha256(a_ref).hexdigest()
    h_new = hashlib.sha256(a_new).hexdigest()

    print(f"Duración referencia : {d_ref:.5f} s")
    print(f"Duración re-ejecución: {d_new:.5f} s   (diferencia {abs(d_ref - d_new) * 1000:.2f} ms)")
    print(f"Audio PCM referencia : {len(a_ref):>9} bytes  {h_ref[:16]}")
    print(f"Audio PCM re-ejecución: {len(a_new):>9} bytes  {h_new[:16]}  {'IDÉNTICO' if h_ref == h_new else 'DISTINTO'}")
    print(f"SSIM medio          : {s}")
    if linea:
        print(f"  {linea}")

    ok_duracion = abs(d_ref - d_new) <= 0.04
    ok_audio = h_ref == h_new
    ok_visual = s is not None and s >= 0.99
    print('\nRESULTADO:', 'OK' if (ok_duracion and ok_audio and ok_visual) else 'REVISAR')

    if args.json:
        datos = {
            'referencia': os.path.basename(args.ref),
            're_ejecucion': os.path.basename(args.new),
            'duracion_ref_s': d_ref,
            'duracion_new_s': d_new,
            'diferencia_ms': abs(d_ref - d_new) * 1000,
            'audio_pcm_sha256_ref': h_ref,
            'audio_pcm_sha256_new': h_new,
            'audio_identico': ok_audio,
            'ssim_medio': s,
            'ssim_detalle': linea,
            'criterios': {
                'duracion_tol_40ms': ok_duracion,
                'audio_identico': ok_audio,
                'ssim_min_0_99': ok_visual,
            },
        }
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        print(f"Guardado en {args.json}")

    return 0 if (ok_duracion and ok_audio and ok_visual) else 1


if __name__ == '__main__':
    sys.exit(main())
