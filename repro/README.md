# Paquete de verificación reproducible — Misión Geometría

Este paquete permite repetir las comprobaciones que el artículo reporta sobre los
archivos conservados y volver a renderizar la composición de la Misión 3 desde sus
insumos. No sintetiza voces.

## Qué demuestra

1. Que los diez MP4 del corpus son los descritos, con su tamaño y su SHA-256.
2. Que los diez archivos decodifican sin errores en modo estricto.
3. Que la duración autorada de la introducción de la Misión 3 se recalcula desde
   los WAV por parlamento y las reglas de montaje, y coincide con el MP4.
4. Que los fotogramas que sustentan la corrección geométrica de la Misión 4 son
   los mismos y que los cuatro criterios registrados se cumplen.
5. Que la composición de la Misión 3, re-renderizada desde sus insumos en una
   copia aislada del proyecto, reproduce la misma duración y el mismo audio, y
   un resultado visual prácticamente idéntico.

## Qué no demuestra

- No sintetiza voces ni regenera el audio: lo valida por hash.
- No acredita identidad binaria entre equipos.
- No reemplaza una réplica independiente en una instalación limpia.
- No evalúa calidad percibida ni aprendizaje: eso corresponde a la revisión experta.

## Requisitos

- Python 3.9 o superior, sin dependencias externas.
- FFmpeg y FFprobe en el `PATH`, o indicados con `--ffmpeg` y `--ffprobe`.
- Para la re-ejecución del render: Node.js y HyperFrames 0.8.169.

## Uso

```bash
python verify_hashes.py --media /ruta/app/media
python decode_all.py    --media /ruta/app/media
python recompute_timing.py --proyecto /ruta/video-mision-3 --mp4 /ruta/app/media/mision03.mp4
python check_geometry_m4.py --mp4 /ruta/app/media/mision04.mp4
python compare_render.py --ref /ruta/mision03.mp4 --new /ruta/replica.mp4
```

Cada script imprime una tabla y termina con `RESULTADO: OK` o `RESULTADO: FALLA`.
El código de salida es 0 cuando todo coincide y 1 cuando algo difiere.

## Contenido

| Archivo | Función |
|---|---|
| `manifest.csv` | Diez piezas con función, duración, tamaño, SHA-256 y profundidad documental. |
| `verify_hashes.py` | Coteja cada archivo con el manifiesto. |
| `decode_all.py` | Decodificación completa en modo de error estricto. |
| `recompute_timing.py` | Recálculo de la duración autorada de la Misión 3. |
| `check_geometry_m4.py` | Fotogramas y criterios de la corrección de la Misión 4. |
| `compare_render.py` | Compara un render re-ejecutado con el de referencia: duración, audio y SSIM. |
| `expected/timing-m3.json` | Reglas de montaje y valores esperados de la Misión 3. |
| `expected/qa-m4.json` | Hashes de píxeles y criterios esperados de la Misión 4. |
| `expected/render-m3.json` | Resultado de la re-ejecución del render de la Misión 3. |
| `environment.md` | Inventario del equipo y las herramientas usadas. |
| `entorno.json` | El mismo inventario, legible por máquina. |
| `RESULTADOS.md` | Salida de la última ejecución sobre el corpus local. |

## Medios

El paquete no incluye los MP4, los WAV ni las imágenes: solo metadatos, scripts y
resultados esperados. Los videos se comparten por separado con los revisores.

## Licencia

Los scripts de este paquete se distribuyen bajo licencia MIT (véase `../LICENSE`).
Los datos y resultados esperados, bajo CC BY 4.0 (véase `../LICENCIA-CONTENIDO.md`).
La decisión completa, con su justificación, está en `../LICENCIAS.md`.
