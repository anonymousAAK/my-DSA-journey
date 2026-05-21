> Esta es una traducción del original en inglés. Si algo no queda claro, consulta la [versión en inglés](../../QUICKSTART.md).

# Quickstart — 4 horas para ver si este repo funciona para ti

Si 30 semanas te parece intimidante: no empieces ahí. Dedica 4 horas enfocadas a este camino curado. Al final habrás practicado toda la metodología en 8 problemas representativos de 5 niveles de dificultad. Si el bucle te funciona, el camino largo es solo más repeticiones del mismo.

El bucle es el mismo que se enseña en [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md):

> Entender → Planificar (fuerza bruta → mejor → óptimo) → Ejecutar → Revisar (journal).

Hoy harás ese bucle ocho veces.

---

## Antes de empezar (10 min)

1. Lee [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) — al menos hojea las secciones **"Los cuatro pasos de Polya"** y **"La escalera fuerza bruta → mejor → óptimo"**.
2. Copia [`docs/SOLUTION_JOURNAL.md`](../../docs/SOLUTION_JOURNAL.md) a `my_journal.md` en tu directorio de trabajo (sin commitear). Añadirás una entrada por problema.
3. Pon un temporizador de 4 horas. Si te excedes del presupuesto por más de 5 minutos en cualquier problema, detente, mira el archivo de referencia y sigue. Hoy el objetivo es *cobertura del bucle*, no soluciones perfectas.
4. Abre tu editor scratch con dos paneles: el problema a la izquierda, tu journal a la derecha.

> **Una regla, no negociable.** Intenta cada problema *antes* de abrir el archivo de referencia. Leer la respuesta primero convierte esto de entrenamiento en entretenimiento.

---

## Hora 1 — Foundations (reconocer un patrón)

Objetivo: sentir la diferencia entre fuerza bruta y la "herramienta correcta". Dos problemas cortos, luego un drill de patrones.

### Problema 1: Two Sum (15 min, Fácil)
- **Referencia (mira solo después de intentarlo)**: [`Week 16/java/1.HashingAndHashMap.java`](../../Week%2016/java/1.HashingAndHashMap.java) — hojea solo la función `twoSum` (alrededor de la línea 43).
- **Spec**: dados `nums` y `target`, devuelve los dos índices cuyos valores sumen `target`. Asume exactamente una solución.
- **Tarea**: resuélvelo en tu lenguaje preferido SIN mirar. Escribe primero el `O(N²)` por fuerza bruta, luego la versión hash-map `O(N)`.
- **Journal (2 min)**: ¿Qué patrón usaste? ¿Por qué la fuerza bruta era `O(N²)`? Escribe la *idea clave* en una oración — esa oración es lo que se transfiere.

### Problema 2: Subarray máximo / Kadane (15 min, Fácil)
- **Referencia**: [`Week 6/python/4.prefix_sum_and_kadane.py`](../../Week%206/python/4.prefix_sum_and_kadane.py) — Parte B, algoritmo de Kadane.
- **Spec**: dado un array de enteros (los valores pueden ser negativos), encuentra el subarray contiguo con suma máxima. Devuelve la suma.
- **Tarea**: fuerza bruta primero (cada par `(i, j)`, O(N²) o O(N³)), luego deriva la recurrencia running-best `O(N)` de Kadane. No mires hasta tener ambos escritos.
- **Journal (2 min)**: ¿Qué trabajo desperdiciaba la fuerza bruta? ¿Qué invariante mantiene Kadane en cada paso?

### Problema 3: Drill de reconocimiento de patrones (10 min)
- Abre [`Week 6/patterns.md`](../../Week%206/patterns.md). Haz los **drills 1–5** en frío (no mires el resto del archivo ni ninguna solución).
- Para cada uno, escribe una línea: qué patrón (dos punteros / ventana deslizante / suma prefijo / Kadane / Dutch flag / hash) y una justificación de una oración.
- Luego verifícate con la clave de respuestas al final del mismo archivo.

### Cierre Hora 1 (5 min)
En tu journal, escribe 3 oraciones respondiendo:
1. ¿Con qué luchaste — reformular el problema, elegir el patrón, o codificarlo?
2. ¿Qué problema se sintió "obvio en retrospectiva"? ¿Por qué no era obvio al inicio?
3. ¿Realmente escribiste fuerza bruta primero en el Problema 2, o saltaste a Kadane?

---

## Hora 2 — Structures (construir la herramienta correcta)

Objetivo: ver que *elegir la estructura de datos* a menudo *es* el algoritmo.

### Problema 4: Fusionar dos listas enlazadas ordenadas (25 min, Medio)
- **Referencia**: [`Week 11/python/2.MergeSortedListsAndLRU.py`](../../Week%2011/python/2.MergeSortedListsAndLRU.py) — solo la función merge. NO leas la sección LRU todavía.
- **Spec**: dadas dos listas enlazadas simples ordenadas, devuelve una lista ordenada fusionada. Reutiliza nodos (sin copiar).
- **Tarea**: primero bosqueja en papel. Dibuja dos listas, dos punteros, y traza qué nodo empalmas a continuación. Luego programa. Usa un dummy/sentinel head — elimina el caso "el primer nodo es especial".
- **Journal (3 min)**: ¿Por qué un dummy head acorta el código? ¿Cuál es la complejidad de tiempo y espacio, y dónde va el espacio?

### Problema 5: Árbol binario — profundidad máxima (15 min, Fácil-Medio)
- **Referencia**: [`Week 14/python/1.BinaryTree.py`](../../Week%2014/python/1.BinaryTree.py) — encuentra la función de profundidad / altura.
- **Spec**: dada la raíz de un árbol binario, devuelve su profundidad (número de nodos en el camino raíz-a-hoja más largo).
- **Tarea**: escríbelo recursivo en tres líneas. Luego escribe la versión iterativa usando una cola (level-order, contar niveles).
- **Journal (2 min)**: Escribe la recurrencia en una línea: `depth(root) = ...`. Esta es la misma forma que una recurrencia DP; la verás de nuevo.

### Cierre Hora 2 (5 min)
- ¿Qué estructura te sorprendió — la lista enlazada o el árbol?
- ¿Podrías haber resuelto el Problema 5 con el mismo hábito de recursión que usaste en [`Week 5/python/3.recursion_basics.py`](../../Week%205/python/3.recursion_basics.py)? Ábrelo brevemente y confírmalo — la recursión *es* el hilo conductor.

---

## Hora 3 — Algoritmos (elegir el enfoque correcto)

Objetivo: graduarse de "¿cuál es la estructura de datos?" a "¿cuál es la *técnica*?"

### Problema 6: Subcadena más larga con K caracteres distintos (25 min, Medio)
- **Referencia**: [`Week 30/python/sliding_window.py`](../../Week%2030/python/sliding_window.py) — la plantilla de ventana de tamaño variable.
- **Spec**: dada una cadena `s` y entero `k`, devuelve la longitud de la subcadena más larga que contiene como máximo `k` caracteres distintos.
- **Tarea**: fuerza bruta primero (cada subcadena, contar distintos → `O(N²)` o `O(N³)`). Luego deriva la ventana deslizante: expandir derecha, contraer izquierda mientras el conteo de distintos exceda `k`, llevar mejor longitud. `O(N)`.
- **Journal (3 min)**: ¿Qué invariante mantiene la ventana? ¿Por qué cada carácter se visita como máximo dos veces (una por `right`, una por `left`)?

### Problema 7a (calentamiento antes del reto abierto): razonamiento BFS (15 min, Medio)
- **Referencia**: [`Week 17/python/1.GraphRepresentations.py`](../../Week%2017/python/1.GraphRepresentations.py) — función BFS.
- **Spec**: dado un grafo no dirigido sin pesos como lista de adyacencia y dos nodos `s` y `t`, devuelve el número de aristas en un camino más corto, o `-1` si es inalcanzable.
- **Tarea**: escribe BFS desde cero. Usa una cola y un conjunto visitados. Trackea la profundidad ya sea almacenando tuplas `(node, depth)` o procesando la cola un nivel a la vez.
- **Journal (2 min)**: ¿Por qué BFS da caminos más cortos *sin pesos* pero no *con pesos*? (Si no lo sabes, esa es tu señal hacia la Semana 22.)

### Cierre Hora 3 (5 min)
Ventana deslizante y BFS son ambos "expandir una frontera cuidadosamente". Anota en tu journal: qué comparten, y qué los hace diferentes (uno se mueve a lo largo de un array 1-D, el otro por un grafo arbitrario).

---

## Hora 4 — Síntesis (hacerlo bajo presión simulada)

Objetivo: combinar el bucle de extremo a extremo en un problema en el que no te han llevado de la mano.

### Problema 8: Reto abierto (40 min, Difícil)
Elige **un** reto de [`Week 8/challenges.md`](../../Week%208/challenges.md) — recomendado: **Reto 1 (Closest Element in a Rotated Sorted Array)** si has visto búsqueda binaria antes, si no, **Reto 2** del mismo archivo.

Reglas:
1. Reformula la spec con tus palabras al inicio de tu entrada de journal. Anota las restricciones.
2. Bosqueja el enfoque en 2 oraciones *antes* de escribir código.
3. Implementa. Sin mirar ningún archivo bajo `Week 8/python/`, `Week 8/java/`, etc.
4. Prueba contra las entradas dadas en el archivo del reto.
5. Solo después de que funcione (o tras 40 min, lo que ocurra primero), compara tu solución con la canónica. ¿Qué hiciste diferente?

### Problema 9: Autorrevisión de mock interview (15 min)
Lee [`mock_interviews/01_two_sum_warm_up.md`](../../mock_interviews/01_two_sum_warm_up.md) — la transcripción anotada completa del primer problema de la Hora 1.

- Compara tu proceso de pensamiento de la Hora 1 con los buenos hábitos anotados de la transcripción (los callouts).
- ¿Qué hiciste *tú* que la transcripción marcó como "bueno"? (p.ej. preguntar por duplicados, reformular el problema, narrar tradeoffs.)
- ¿Qué saltaste? (p.ej. ¿anunciaste tu complejidad? ¿mencionaste la fuerza bruta antes de resolver?)

### Cierre Hora 4 (5 min)
Escribe en tu journal:
- ¿Tu solución del reto de la Hora 4 estuvo más cerca de fuerza bruta, "mejor", u óptima? ¿Por qué?
- ¿Cuál de los cuatro pasos de Polya saltaste más hoy? (La mayoría salta el paso 4, "revisar".)
- ¿Qué harías diferente la próxima vez?

---

## ¿Y ahora qué?

Acabas de hacer un microcosmos del currículo completo. Ocho problemas, cinco niveles de dificultad, cada capa del bucle. Si te resultó valioso:

- **Haz el diagnóstico** ([`docs/diagnostic.md`](../../docs/diagnostic.md)) para encontrar tu punto de partida real. Salta las semanas que ya dominas.
- **8 semanas de preparación enfocada para entrevistas**: sigue [Learning Path 2 (Interview Prep)](../../README.md#path-2-interview-prep-8-weeks) en el README raíz — Semanas 6, 8, 11, 14, 16, 17, 18, 30.
- **30 semanas completas**: empieza en la Semana 1 y haz journal de cada problema. La mayoría de quienes terminan lo hacen así.
- **Programación competitiva**: sigue [Path 3](../../README.md#path-3-competitive-programming-10-weeks).

Si no te resultó valioso, antes de irte, revisa honestamente:

- ¿Realmente intentaste cada problema antes de mirar?
- ¿Hiciste journal, o solo leíste?
- ¿Escribiste fuerza bruta *primero* en los Problemas 2, 6 y 7a — o saltaste a la solución astuta?
- ¿Comparaste tu código con la versión canónica en el Problema 8?

La mayoría de los resultados "esto no me funcionó" se rastrean a un salto específico: el paso del journal. El journal es donde realmente vive la metodología. El código es el subproducto.

---

> Una vez que hayas hecho el bucle ocho veces, lo has hecho ocho veces. Eso no es nada. Así empieza el hábito.
