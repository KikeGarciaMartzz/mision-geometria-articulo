# Entorno de verificación

Inventario de la máquina donde se ejecutaron las comprobaciones de `repro/` y la re-ejecución del render de la Misión 3. Registro del 12 de noviembre de 2026. Los valores legibles por máquina están en `entorno.json`.

**Advertencia de alcance.** Este inventario describe el equipo de verificación. No es el entorno original de producción de octubre de 2026: aquel no registró GPU, CUDA ni versiones de dependencias, y por eso no puede reconstruirse con exactitud. La diferencia importa: el audio sintetizado no puede reproducirse byte a byte sin ese entorno.

## 1. Equipo

| Componente | Valor |
|---|---|
| Sistema operativo | Windows 11 Pro 10.0.26200 (x86_64) |
| CPU | Intel Core i7-13620H, 10 núcleos físicos, 16 hilos lógicos |
| RAM | 15,7 GiB |
| GPU | NVIDIA GeForce RTX 5060 Laptop GPU, 8 151 MiB, compute capability 12.0 |
| Controlador NVIDIA | 591.86 |
| CUDA del controlador | 13.1 |

## 2. Herramientas

| Componente | Versión | Nota |
|---|---|---|
| Python | 3.14.5 | Ejecuta los scripts de `repro/` |
| Node.js | 24.16.0 | Requerido por HyperFrames |
| npm | 11.13.0 | |
| FFmpeg / FFprobe | 8.1.1 essentials (gyan.dev) | En `C:\Users\kikeFelizz\Downloads\ffmpeg\bin` |
| Google Chrome | 157.0.8103.52 | Motor de captura de HyperFrames y de las figuras |
| GreenSock (GSAP) | 3.14.2 | Fijado en `assets/vendor/gsap.min.js` del proyecto |
| HyperFrames CLI | 0.8.169 | Fijado en `package.json`; servido desde la caché de `npx` |

## 3. Paquetes de Python

| Paquete | Versión |
|---|---|
| torch | 2.14.1 |
| transformers | 5.19.0 |
| numpy | 2.5.4 |
| soundfile | 0.14.0 |
| huggingface_hub | 2.2.0 |

### Ausentes

| Paquete | Consecuencia |
|---|---|
| `qwen_tts` | **La síntesis de voz no puede re-ejecutarse en este equipo.** Las locuciones se verifican por hash, no regenerándolas. |
| `faster_whisper` | La transcripción de verificación no puede re-ejecutarse. Se conservan los JSON de transcripción ya producidos. |

Estas dos ausencias marcan el límite real de lo que este paquete demuestra. Cubre la composición, el montaje, la codificación y la integridad de los archivos; **no** cubre la generación del audio.

## 4. Procedencia del render integrado

Metadatos extraídos del MP4 adoptado (`app/media/mision03.mp4`):

| Campo | Valor |
|---|---|
| Codificador de video | Lavc62.28.101 libx264 |
| Muxer | Lavf62.12.101 |
| `hyperframes_version` | 0.8.169 |
| `hyperframes_renderer` | hyperframes |
| Duración del contenedor | 53,30000 s |
| SHA-256 | `161be9d332b3735da359cfb05b5b4b8f19c643cc1292a3640ff9915f7b9793c9` |

El render conservado en el proyecto (`renders/video-mision-3_2026-10-18_17-09-37.mp4`) tiene el mismo SHA-256 que el archivo integrado y que `renders/mision_03_intro.mp4`. La cadena render → integración no tiene pasos perdidos.

## 5. Insumos del render

| Archivo | SHA-256 |
|---|---|
| `index.html` | `6e28d04a50843a62f81db0821d47d42f82d54852adddac8183dc38cfcf5ad266` |
| `compositions/captions.html` | `6d0a012a547026f6d061999409fe6998ffab30257f20076428170be50a33b214` |
| `tools/sync.json` | `0c39a8bd36201f9f56408a1fb87de4a71aa24c9d4e8da413eefa41043269bf4a` |
| `assets/voice/duraciones.json` | `4a4a5bb9d255a2fa419779d262700f69a9770f86c784a58cd9ed8b035517ef99` |
| `assets/vendor/gsap.min.js` | `c174bfce53a729418d57a8ad8625e7247c793a22fef8e2851e3cfa3de9cd8280` |
| `metadata.json` | `63c58eb982fb9c3c46c1e94c92047b84582c87be7750dc93c82103b69b7d925f` |

## 6. Cómo se re-ejecutó el render

1. Se copió el proyecto a una carpeta temporal, excluyendo `renders/`, `qa/` y `.hyperframes/`.
2. Se verificó que las 70 copias fueran idénticas por SHA-256 al original (70/70).
3. Se ejecutó `npx --yes hyperframes@0.8.169 render . -o renders/replica.mp4` en la copia.

El proyecto original no se modificó. Los resultados de la comparación están en `RESULTADOS.md`, sección 5.

## 7. Comandos de referencia

```
ffmpeg -v error -xerror -threads 2 -i MP4 -map 0:v:0 -map 0:a:0 -f null -
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 MP4
npx --yes hyperframes@0.8.169 check
npx --yes hyperframes@0.8.169 render . -o renders/salida.mp4
```

## 8. Límites

- La GPU y el controlador son los del equipo de verificación, no necesariamente los de octubre de 2026.
- Chrome y FFmpeg cambiaron de versión entre el render original y esta re-ejecución; una diferencia de píxeles es esperable y no implica un error del método.
- La ausencia de `qwen_tts` impide afirmar que una re-ejecución de la síntesis reproduzca el mismo audio en otro equipo.
