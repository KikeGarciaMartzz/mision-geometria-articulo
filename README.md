# Materiales de análisis de Misión Geometría

Material complementario en desarrollo del estudio Misión Geometría. Contiene documentación depurada y herramientas de análisis; no es todavía una réplica audiovisual completa de los diez videos. Los videos originales introducen y cierran misiones narrativas alrededor de una lección interactiva; no sustituyen la lección.

## Contenido

- `encargo-m3-real-depurado.txt`: encargo real, con dos rutas personales sustituidas. Los términos abreviados son literales históricos, no la nomenclatura del artículo.
- `metricas-sesiones.json`: conteos derivados de cinco sesiones de producción; no costos facturados ni tiempo humano.
- `extraer-proceso.py`: consulta de solo lectura de la base de OpenCode. No se distribuye la base.
- `manifiesto-videos.csv`: nombres y hashes de las versiones del corpus a evaluar.
- `Instrumento-revision.md`, matrices R1/R2 y bitácoras: instrumento de siete criterios con escala OK/Leve/Grave/NA/NE. Las matrices están vacías: son plantillas, no resultados.
- `analizar-revision.py`: cobertura y acuerdo descriptivo por criterio, sin imputación de respuestas.
- `flujo-produccion.png`: diagrama del procedimiento.
- `repro/`: paquete de verificación reproducible. Coteja hashes, decodifica los diez MP4, recalcula tiempos, revisa la corrección geométrica de la Misión 4 y compara un render re-ejecutado con el de referencia. No incluye medios.

Python 3.10 o superior, biblioteca estándar, es suficiente para los scripts de extracción y análisis. No requieren credenciales ni conexión de red. La extracción requiere una base local compatible con `session_message` y no modifica esa base.

Ejemplos:

```text
python extraer-proceso.py --db RUTA_LOCAL/opencode.db --out salida
python analizar-revision.py --r1 evaluacion-R1.csv --r2 evaluacion-R2.csv --out acuerdo.json
```

Las matrices distribuidas están vacías. Un informe de cero pares puntuados significa evaluación pendiente, no concordancia perfecta. Los valores NE y NA se informan aparte.

## Alcance y pendientes

Se excluyeron voces, MP4, imágenes de personas/personajes, fondos, música, escaneos del libro, biblioteca de artículos, bases completas de conversaciones, dependencias y credenciales. No se afirma que omitir estos archivos equivalga a sustituir voces: la producción de un ejemplo con referencias autorizadas y la comprobación de sus tiempos aún están pendientes.

La evaluación por dos revisores humanos está en curso; los resultados se incorporarán al manuscrito cuando concluya. Las licencias de reutilización se definen más abajo. Antes de añadir medios, se comprobarán su procedencia y las autorizaciones de distribución. Se mantendrán separados corpus histórico, corpus corregido y ejemplo público con voces sustituidas.

Los artículos se citan por DOI en el instrumento y el manuscrito; no se redistribuyen en este paquete. La atribución del complemento metodológico dentro del instrumento identifica la herramienta de asesoría utilizada y no implica autoría de sus creadores sobre el estudio.

## Reproducción del análisis

`extraer-proceso.py` contiene los identificadores de las cinco sesiones del caso. Una base de otro proyecto no reproduce esos registros: debe adaptarse explícitamente la selección de sesiones y los hitos usados para M3. La base original permanece privada. `metricas-sesiones.json` permite inspeccionar los resultados agregados y sus límites sin acceder a conversaciones completas.

## Licencias

Este repositorio mezcla materiales con regímenes distintos:

- **Texto, figuras y datos de verificación** — [CC BY 4.0](LICENCIA-CONTENIDO.md). Puedes copiarlos, adaptarlos y redistribuirlos citando la fuente.
- **Scripts y código** — [MIT](LICENSE).
- **Corpus audiovisual** (videos, grabaciones de referencia y locuciones) — no se distribuye con este repositorio y no está cubierto por las licencias anteriores. Su uso se rige por autorizaciones individuales de voz.

El detalle de la decisión, con la comparación de alternativas, está en [LICENCIAS.md](LICENCIAS.md).

### Cómo citar

> García Martínez, E., Badal García, E., Córdova García, R., & Ramón Morales, Y. (2026). *Producción agéntica de videos narrativos con HyperFrames y Qwen3-TTS para Misión Geometría* [Manuscrito]. https://github.com/KikeGarciaMartzz/mision-geometria-articulo
