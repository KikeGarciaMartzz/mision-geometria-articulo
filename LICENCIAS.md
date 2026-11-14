# Licencias del proyecto

Documento de decisión. Explica qué licencia se aplica a cada tipo de material, por qué, y qué falta hacer para que la declaración sea cierta.

Fecha: 12 de noviembre de 2026.

---

## 1. Recomendación

El repositorio no contiene una sola clase de material. Aplicar una licencia única obliga a elegir entre dos males: abrir el código con una licencia de contenido, que es torpe para software, o cerrar el texto con una licencia de código, que impide la reutilización académica normal.

La recomendación es **tres regímenes separados por tipo de material**:

| Material | Licencia | Por qué |
|---|---|---|
| Texto del manuscrito, figuras y datos de verificación (`.md`, `.png`, `.csv`, `.json`) | **CC BY 4.0** | Es el estándar de la publicación académica abierta. Permite citar, reutilizar y adaptar con atribución, sin fricción para revistas, repositorios institucionales o docentes que quieran reutilizar las figuras. |
| Scripts y código de las figuras (`repro/*.py`, `outputs/figuras/*.html`) | **MIT** | Es la licencia permisiva más corta y más entendida en investigación. Permite verificar y reutilizar el código sin obligar a nadie a adoptar nuestro marco legal completo. |
| Corpus audiovisual: los diez MP4, las grabaciones de referencia de voz y las locuciones sintetizadas | **Sin licencia de redistribución** | Contiene voces clonadas de personas reales. Su difusión se rige por las autorizaciones individuales (`Autorizacion-uso-de-voz.md`), no por una licencia de contenido. |

## 2. Por qué CC BY 4.0 y no otra

| Opción | Qué implica | Veredicto |
|---|---|---|
| **CC BY 4.0** | Cualquiera puede copiar, adaptar y redistribuir con atribución, incluso con fines comerciales. | **Elegida.** Es la licencia que hacen suponer las revistas de acceso abierto y los repositorios institucionales. No pierdes la autoría: la atribución es obligatoria y los derechos morales siguen intactos. |
| CC BY-NC 4.0 / CC BY-NC-SA 4.0 | Prohíbe el uso comercial. | No recomendada. La cláusula «no comercial» es ambigua en la práctica (¿una universidad que cobra matrícula es comercial?), algunas revistas y repositorios la rechazan, y no protege nada que aquí importe: no hay un producto comercial que defender. |
| CC BY-ND 4.0 | Permite copiar pero no adaptar. | No recomendada. Impide traducir el artículo o reutilizar una figura modificada, que es justo lo que un docente querría hacer. |
| CC0 | Renuncia a todo derecho. | No recomendada. Es más de lo necesario y dificulta exigir atribución, que en un trabajo de clase sí importa. |
| Todos los derechos reservados | Nadie puede reutilizar sin permiso. | Contradice la sección de disponibilidad del manuscrito y el espíritu del paquete reproducible. |

## 3. Por qué MIT y no Apache-2.0 o GPL

- **MIT**: dos párrafos, sin ambigüedad, compatible con todo. Es lo que usa la mayoría del código de investigación.
- **Apache-2.0**: añade una concesión explícita de patentes. Aporta poco aquí: los scripts no implementan nada patentable, solo verifican archivos.
- **GPL**: obligaría a quien reutilice los scripts a abrir su propio código. Es una carga innecesaria para un paquete de verificación de treinta líneas por archivo.

## 4. Un matiz que conviene decidir

La **Figura 2** es un fotograma del video de la Misión 3. Si las figuras quedan bajo CC BY 4.0, esa imagen concreta pasa a ser reutilizable por terceros, aunque los videos no lo sean.

Es una decisión consciente, no un descuido: el fotograma no contiene audio ni la voz clonada, y permitir su reutilización con atribución es coherente con el resto de las figuras. Si el equipo prefiere lo contrario, la alternativa es marcar la Figura 2 como «reproducida con fines de estudio» y excluirla de CC BY; en ese caso hay que decirlo en la nota de la figura.

**Recomendación:** dejarla bajo CC BY 4.0. La inconsistencia sería mayor si una figura del artículo no se pudiera reutilizar como las demás.

## 5. Textos listos para usar

### 5.1 Archivo `LICENSE` (código)

Contenido completo en `LICENSE`, con la línea de copyright ya escrita: Enrique García Martínez, Emanuel Badal García, Renán Córdova García y Yuliana Ramón Morales.

### 5.2 Archivo `LICENCIA-CONTENIDO.md` (texto, figuras y datos)

Contenido completo en `LICENCIA-CONTENIDO.md`.

### 5.3 Sección para el README del repositorio público

```markdown
## Licencias

Este repositorio mezcla materiales con regímenes distintos:

- **Texto, figuras y datos de verificación** — [CC BY 4.0](LICENCIA-CONTENIDO.md).
  Puedes copiarlos, adaptarlos y redistribuirlos citando la fuente.
- **Scripts y código de las figuras** — [MIT](LICENSE).
- **Corpus audiovisual** (videos, grabaciones de referencia y locuciones) —
  no se distribuye con este repositorio y no está cubierto por las licencias
  anteriores. Su uso se rige por autorizaciones individuales de voz.

### Cómo citar

> [Apellidos, N.], et al. (2026). *Producción agéntica de videos narrativos con
> HyperFrames y Qwen3-TTS para Misión Geometría* [Manuscrito]. Repositorio del
> proyecto. https://github.com/KikeGarciaMartzz/mision-geometria-articulo
```

Si GitHub detecta `LICENSE` en la raíz, mostrará «MIT license» en la barra lateral del repositorio. Eso es correcto y no entra en conflicto con `LICENCIA-CONTENIDO.md`: el archivo `LICENSE` cubre el código y el otro documento declara el alcance del contenido.

### 5.4 Línea de atribución para quien reutilice una figura

> «Figura tomada de [Apellidos] et al. (2026), *Producción agéntica de videos narrativos con HyperFrames y Qwen3-TTS para Misión Geometría*, CC BY 4.0.»

## 6. Lo que ya quedó declarado en el manuscrito

El apartado «Ética y licencias» de `Manuscrito-Mision-Geometria-v4.md` incluye el párrafo que fija estos tres regímenes. La declaración ya lleva los nombres de los autores en los archivos de licencia. Falta un paso para que sea del todo cierta: copiar `LICENSE`, `LICENCIA-CONTENIDO.md` y `LICENCIAS.md` al repositorio público.

## 7. Pasos para cerrar el punto

1. ~~Escribir los nombres de los autores en la línea de copyright.~~ Hecho el 12 de noviembre de 2026.
2. Copiar `LICENSE`, `LICENCIA-CONTENIDO.md` y `LICENCIAS.md` al repositorio público `mision-geometria-articulo`, en la raíz.
3. Añadir la sección del README (5.3).
4. Verificar en GitHub que la barra lateral muestra «MIT license».
5. Registrar la fecha de publicación de la licencia en `Registro-de-evidencia.md`.

## 8. Advertencia

Esto es una recomendación técnica y editorial, no asesoría jurídica. Si el trabajo se presenta ante una institución, conviene que su oficina de propiedad intelectual o su asesoría legal revise el texto. Para un trabajo de clase con tres o cuatro integrantes, el riesgo de estas licencias es bajo: no ceden la autoría, no transfieren derechos patrimoniales y son revocables en el sentido de que pueden cambiarse en versiones futuras del repositorio (aunque no en las copias que terceros ya hayan descargado).
