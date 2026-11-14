# Resultados de la verificación

Ejecución del 12 de noviembre de 2026 sobre el corpus local
(`Proyectos/mision-geometria-curso/app/media`), con FFmpeg 8.1.1 y Python 3.14.

## 1. Hashes

```
archivo                 bytes  sha256            estado
bienvenida.mp4       12377736  d40908f657eb0484  OK
mision01.mp4          5640103  7515f21071d107d5  OK
entrega1.mp4         14515790  5567b161de201d93  OK
mision02.mp4          5551941  c09b92a7a7a3e2d9  OK
entrega2.mp4          8986205  abf002a72cc4914d  OK
mision03.mp4          6283504  161be9d332b3735d  OK
entrega3.mp4          9200775  bd0a4e177802eaa7  OK
mision04.mp4          6111231  12a7565a044a65de  OK
entrega4.mp4         10099743  72d424fd5cbb2347  OK
epilogo-curso.mp4    22202169  2add22f06bbe1075  OK

Coincidencias: 10/10
```

Cotejo adicional: los diez archivos descargados de la carpeta de Google Drive
«Misión Geometría - Videos del curso» coincidieron con estos mismos hashes (10/10).

## 2. Decodificación estricta

```
bienvenida.mp4       OK
mision01.mp4         OK
mision02.mp4         OK
mision03.mp4         OK
entrega1.mp4         OK
entrega2.mp4         OK
entrega3.mp4         OK
entrega4.mp4         OK
mision04.mp4         OK
epilogo-curso.mp4    OK

Decodifican sin errores: 10/10
```

## 3. Duración autorada de la Misión 3

```
Duración autorada recalculada: 53.28775 s
Duración declarada en sync.json: 53.28775 s
Desfase máximo en los inicios de parlamento: 0.00 ms
Duración del contenedor MP4: 53.30000 s (diferencia 12.2 ms)

RESULTADO: OK
```

La diferencia de 12,2 ms corresponde al redondeo del contenedor a 30 fotogramas
por segundo (53,28775 s = 1598,63 fotogramas).

## 4. Corrección geométrica de la Misión 4

```
Fotogramas
   44.000 s  OK  8fe806ae3d85e967
   48.200 s  OK  052168aa70dbdef9
   50.030 s  OK  2c7a95f252c33469
   52.587 s  OK  5c5c162c19633a99

Criterios registrados
  vertice_aguja_vs_centro_px             1.21  OK
  punta_termina_sobre_graduacion_50      True  OK
  etiquetas_ocluidas                     []    OK
  escala_dentro_del_encuadre             True  OK

RESULTADO: OK
```

## 5. Re-ejecución del render de la Misión 3

Se copió el proyecto de producción a una carpeta temporal, excluyendo `renders/`, `qa/` y `.hyperframes/`. Las 70 copias resultaron idénticas por SHA-256 al original (70/70). Sobre esa copia se ejecutó:

```
npx --yes hyperframes@0.8.169 render . -o renders/replica.mp4
```

El render terminó en 1 min 55 s, con captura por GPU y 630 de 1599 fotogramas reutilizados por deduplicación estática. El proyecto original no se modificó.

| Comparación | Referencia | Re-ejecución | Resultado |
|---|---|---|---|
| Duración del contenedor | 53,30000 s | 53,30000 s | Diferencia 0,00 ms |
| Audio decodificado (PCM 16 bits) | 10 235 904 bytes, `61af247b2d6507d1` | 10 235 904 bytes, `61af247b2d6507d1` | **Idéntico** |
| SSIM medio del video | — | — | **0,999990** |
| Fotogramas 5,0 / 20,0 / 40,0 / 52,0 s | — | — | **Byte a byte idénticos** |
| SHA-256 del archivo MP4 | `161be9d332b3…` | `f213bf48f916…` | **Distinto** |

La re-ejecución reproduce la duración, el audio y el contenido visual, pero no produce un archivo binariamente idéntico: cambia el contenedor. Es el resultado esperable cuando el codificador, las marcas de tiempo y los metadatos de sesión no están fijados, y confirma por qué el artículo no promete identidad binaria entre equipos.

## Alcance de estos resultados

Los cinco bloques verifican archivos ya producidos y, en el último caso, vuelven a ejecutar la composición desde sus insumos. No prueban que la síntesis reproduzca el mismo audio en otro equipo: `qwen_tts` no está instalado en el entorno de verificación y el entorno original no registró GPU ni versiones de dependencias. La re-ejecución se hizo en una copia, no en una instalación limpia.

## Archivos de la re-ejecución

| Archivo | Contenido |
|---|---|
| `expected/render-m3.json` | Salida de `compare_render.py`: duraciones, hashes de audio, SSIM y criterios. |
| `compare_render.py` | Script que produce esa comparación a partir de cualquier par de MP4. |
| `environment.md` y `entorno.json` | Equipo, versiones y hashes de los insumos del render. |

