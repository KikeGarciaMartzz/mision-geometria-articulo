# Instrumento de revisión del corpus audiovisual

Versión de 13 de noviembre de 2026. Sustituye al instrumento de doce criterios, que se conserva en el archivo histórico del proyecto (`Revision-2026-11-11/Instrumento-revision.md`).

## Propósito y alcance

El instrumento registra la calidad observada en los diez videos de Misión Geometría. No mide aprendizaje, motivación ni eficacia educativa, y no evalúa si el método de producción es superior a otro. Describe lo que una persona ve y oye, con el video y el minuto como referencia.

## Personas y preparación

Cada revisor evalúa los diez videos por su cuenta, sin ver las respuestas del otro y sin conocer los resultados de la conciliación. Se identifica con un código (R1, R2) y firma una constancia de consentimiento que fija el uso de sus datos.

Los videos se identifican por nombre y SHA-256. Las matrices distribuidas están vacías: un informe con cero pares puntuados significa evaluación pendiente, no concordancia perfecta.

## Procedimiento

1. Ver el video completo, a velocidad normal y sin pausar. Anotar el minuto de cualquier distracción o confusión.
2. Volver a los momentos anotados y revisarlos con pausa.
3. Elegir **un solo valor por criterio** en la fila del video.
4. Por cada defecto Leve o Grave, añadir una fila en la bitácora de defectos.
5. Si se elige NA o NE, explicar el motivo en la nota de esa fila.

## Escala

| Valor | Significado |
|---|---|
| **OK** | Sin problema observado. |
| **Leve** | Problema que no impide seguir el mensaje. |
| **Grave** | Problema que impide entender la escena o transmite información incorrecta. |
| **NA** | Criterio no aplicable a ese video. |
| **NE** | Criterio no evaluado. |

Una afirmación matemática falsa se registra como Grave aunque dure un segundo. Las celdas NA, NE o vacías se tratan como datos faltantes; nunca como aprobación.

## Criterios

| Código | Criterio | Pregunta que responde | Qué anotar si hay problema |
|---|---|---|---|
| C1 | Matemática correcta | Lo que se dice, se escribe y se dibuja (ángulos, escalas, figuras, etiquetas) es correcto. | Frase o figura exacta y cuál debería ser. |
| C2 | Función narrativa | La introducción plantea el conflicto, o el cierre reconoce el avance, sin explicar de más; la invitación a la actividad se entiende. | Qué falta, qué sobra o qué confunde. |
| C3 | Continuidad | Personajes, voces y la pieza del mapa son consistentes con los otros videos y con la aplicación. | Qué cambia respecto a otro video o a la app. |
| C4 | Voz clara | Se entiende cada parlamento a velocidad normal y la música o los efectos no lo tapan. | Palabra o frase poco clara, cortes, ruido, volumen. |
| C5 | Subtítulos fieles | Los subtítulos coinciden con lo que se oye y con quién lo dice. | Palabra omitida, añadida o mal atribuida. |
| C6 | Sincronía | Lo que se señala o aparece en pantalla coincide con lo que se dice, sin adelantos ni retrasos que confundan. | Qué aparece y qué frase le corresponde. |
| C7 | Legibilidad visual | El texto se alcanza a leer antes de desaparecer y nada tapa, recorta o vuelve difícil de ver lo importante. | Qué elemento y cuánto dura en pantalla. |

Los criterios C1 y C2 provienen de los requisitos del caso; C3 traduce la continuidad de recursos compartidos; C4 a C7 recogen claridad perceptiva y correspondencia audiovisual, apoyadas en Mayer y Moreno (2003) y Brame (2016). Esa relación conceptual no valida por sí misma los ítems ni establece efectos sobre estudiantes de cuarto grado.

## Bitácora de defectos

Una fila por defecto, en `defectos.csv`. Campos: revisor, video, SHA-256, criterio, identificador del defecto, intervalo en segundos, observación, consecuencia prevista, severidad, evidencia y corrección propuesta.

Ejemplo ficticio, no un hallazgo del corpus: R1; mision03.mp4; C5; D001; 12,3-14,1 s; el subtítulo omite una negación audible; cambia el sentido de la frase; Grave; captura y transcripción; restituir la negación.

## Cierre individual y comparación

Cada revisor entrega su matriz completa antes de ver la del otro. La conciliación se registra aparte, en `conciliacion.csv`, y no modifica las matrices individuales: si hay desacuerdo, se conserva y se explica, no se promedia.

`analizar-revision.py` calcula cobertura por criterio, proporción de acuerdos exactos y un kappa ponderado descriptivo sobre los valores OK, Leve y Grave. Los códigos NA, NE y las celdas vacías se informan aparte y nunca entran al cálculo como aprobación.

## Cómo incorporar los resultados al artículo

Los resultados se presentan como descripción de la calidad observada en este corpus: cobertura por criterio, defectos registrados y acuerdos. No se convierten en evidencia de aprendizaje ni en validación del método. Si un revisor no terminó, se informa su cobertura y no se le imputan valores.

## Información y consentimiento de revisores

Se recoge únicamente el perfil profesional pertinente: formación, experiencia con materiales educativos o audiovisuales y familiaridad con el nivel escolar. No se recogen datos personales innecesarios. Cada revisor firma una constancia que explica el uso previsto, la conservación y su derecho a retirarse.

## Referencias

Brame, C. J. (2016). Effective educational videos: Principles and guidelines for maximizing student learning from video content. *CBE—Life Sciences Education, 15*(4), es6. https://doi.org/10.1187/cbe.16-03-0125

Mayer, R. E., & Moreno, R. (2003). Nine ways to reduce cognitive load in multimedia learning. *Educational Psychologist, 38*(1), 43-52. https://doi.org/10.1207/S15326985EP3801_6

## Atribución de la herramienta metodológica

La estructura de este instrumento se apoya en la herramienta de asesoría metodológica del proyecto. Esa atribución identifica la herramienta utilizada y no implica autoría de sus creadores sobre el estudio.
