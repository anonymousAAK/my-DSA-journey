> Esta es una traducción del original en inglés. Si algo no queda claro, consulta la [versión en inglés](../../PROBLEM_SOLVING.md).

# Resolución de problemas — El manifiesto de mentalidad

> Un currículo de 30 semanas de DSA puede enseñarte *qué* son los algoritmos. Este archivo trata sobre *cómo pensar* cuando un problema que nunca has visto aparece en tu pantalla. Léelo una vez. Léelo de nuevo después de la Semana 10. Y otra vez después de la Semana 20.

> **¿Quieres sentir esto en la práctica antes de comprometerte a 30 semanas?** Dedica 4 horas al [Quickstart](QUICKSTART.md) — ocho problemas curados que te llevan a través del bucle completo descrito a continuación. O haz el [Diagnóstico](diagnostic.md) para encontrar dónde encajas realmente en el currículo.

---

## Por qué existe esto

Este repositorio enseña estructuras de datos y algoritmos. Eso no es lo mismo que enseñar resolución de problemas.

Un **programador** conoce la sintaxis, la biblioteca estándar y un catálogo de algoritmos con nombre. Dale un problema con la palabra clave correcta ("array ordenado" → búsqueda binaria) y entrega solución.

Un **resolvedor de problemas** es algo distinto. Se sienta frente a un enunciado desconocido y no entra en pánico. Lo reformula hasta que deja de ser escurridizo. Construye un ejemplo pequeño a mano. Escribe una solución por fuerza bruta que sabe que es demasiado lenta, *a propósito*, porque esa solución expone la estructura del problema. Luego se hace la única pregunta que impulsa cada optimización en ciencia de la computación: *¿qué trabajo se está desperdiciando?* Su respuesta es el algoritmo.

No estás aquí para memorizar 200 patrones de LeetCode. Estás aquí para convertirte en alguien que, ante un problema que nadie ha resuelto, aún puede avanzar. Los patrones son andamiaje. La mentalidad es lo importante.

---

## Los cuatro pasos de Polya

*How to Solve It* (1945) de George Polya es más antiguo que cualquier libro de texto de tu lista de lectura y más útil que la mayoría. Los cuatro pasos:

### 1. Entender el problema
Léelo dos veces. Luego tres veces. Escribe, con tus propias palabras:
- ¿Cuáles son las entradas? (tipos, rangos, ¿están ordenadas, pueden tener duplicados, pueden estar vacías?)
- ¿Cuál es la salida? (un único valor, una estructura, todas las configuraciones válidas)
- ¿Qué significa "válido" o "mejor" aquí?
- ¿Qué *no* dice el problema? (a menudo la pregunta más importante)

**Ejemplo.** "Encuentra la subcadena más larga con como máximo K caracteres distintos." Antes de hacer nada: ¿se garantiza K ≥ 1? ¿Los caracteres son ASCII o Unicode? Si la cadena está vacía, ¿la respuesta es 0 o indefinida? ¿"Subcadena" es contigua (sí, por convención) o "subsecuencia" (no contigua)? Si saltas este paso, resolverás el problema equivocado y no lo notarás durante veinte minutos.

### 2. Diseñar un plan
Antes de escribir una línea de código, articula el enfoque en español (o inglés). "Voy a usar una ventana deslizante donde el puntero derecho expande hasta que la ventana tenga K+1 caracteres distintos, luego el puntero izquierdo se contrae hasta que vuelva a tener K. Voy llevando el máximo a lo largo del camino." Si no puedes decirlo en dos oraciones, todavía no tienes un plan.

Aquí es también donde conectas el problema nuevo con los viejos. "Esto se parece a 'minimum window substring'." "Esto es solo BFS sobre un grafo implícito." El reconocimiento de patrones es una habilidad de planificación, no de memorización.

### 3. Ejecutar el plan
Ahora escribes código. La traducción del plan al código debe ser mecánica. Si te encuentras tomando grandes decisiones mientras tecleas, detente — saltaste el paso 2.

### 4. Revisar (looking back)
El paso que todos saltan. Después de que pase:
- ¿Puedo derivar una cota de complejidad más ajustada?
- ¿Puedo simplificar el código? (renombrar variables, colapsar casos especiales, eliminar una rama no usada)
- ¿Cuál fue la *idea clave*? Escríbela en una oración. Esa oración es lo que se transfiere al siguiente problema.
- ¿A qué familia pertenece esto? Añádelo a tu índice mental.

**Ejemplo trabajado — Two Sum.**
1. *Entender.* Dado `nums` y `target`, devolver los índices de dos números que sumen `target`. Hay exactamente una solución. No se puede usar el mismo elemento dos veces. Índices, no valores.
2. *Plan.* Fuerza bruta es O(n²) pares. Mejor: para cada `x`, necesitamos `target - x`. La búsqueda es O(1) con un hash. Recorre una vez, pregunta al hash si `target - nums[i]` ya se vio, si no, guarda `nums[i] → i`.
3. *Ejecutar.* Diez líneas de código.
4. *Revisar.* Idea clave: *no necesitamos buscar el par; necesitamos preguntar si el complemento existe*. Ese replanteamiento — "búsqueda → consulta de existencia" — es exactamente el movimiento detrás de 3Sum, 4Sum, two-pointers en arrays ordenados, etc. La técnica es portable; recuerda el movimiento, no el código.

---

## Reformulando problemas ambiguos

Los problemas reales — en el trabajo, en investigación, en entrevistas — llegan vagos. Practica afinarlos.

| Enunciado vago | Versión afinada |
|---|---|
| "Encuentra duplicados en este array." | "Devuelve el conjunto de valores que aparecen más de una vez. El orden no importa. El array cabe en memoria. Los valores son enteros de 32 bits." |
| "Programa las reuniones." | "Dada una lista de intervalos `(start, end)`, devuelve el número máximo de intervalos mutuamente no superpuestos. Dos intervalos que solo comparten un extremo no se superponen." |
| "Encuentra el camino más corto." | "Grafo no dirigido sin pesos con hasta 10⁵ nodos; devuelve el número de aristas en el camino más corto de `s` a `t`, o `-1` si es inalcanzable." |
| "Comprime esta cadena." | "Reemplaza cada secuencia de `k ≥ 2` caracteres idénticos por `c` seguido del conteo en decimal. Las secuencias de longitud 1 se dejan como están. La salida debe ser más corta que la entrada; de lo contrario, devuelve la entrada sin cambios." |
| "Encuentra la mejor ruta." | "*Mejor* según qué métrica — distancia, tiempo, combustible, menos transbordos? ¿Las aristas tienen peso? ¿Los pesos pueden ser negativos? ¿El grafo es denso o disperso?" |

Nota el patrón: los enunciados vagos tienen **restricciones implícitas** que quien pregunta tiene en su cabeza y tú no. Hasta que las restricciones estén en papel, el problema no es un problema — es un deseo.

Cuando trabajes solo (sin nadie a quien interrogar), reformula el problema a ti mismo y **fija las restricciones**. Escríbelas al inicio de tu archivo borrador. Ahora son parte de la especificación.

---

## Identificar restricciones — qué te dice cada una

Las restricciones son la parte menos leída de un enunciado. Y también las pistas más ruidosas en la sala. Léelas como un compilador lee tipos.

**Tamaño de entrada N.** Este único número acota tu clase de algoritmo más que cualquier otra información.

| N hasta | Algoritmos que caben (~1 seg de presupuesto) |
|---|---|
| ~10 | Cualquier cosa. Incluso fuerza bruta O(N!). Backtracking, permutaciones. |
| ~20 | Bitmask DP O(2^N), meet-in-the-middle. |
| ~500 | O(N³) está bien — Floyd-Warshall, interval DP. |
| ~5,000 | O(N²) está bien — DP cuadrático, all-pairs scans. |
| ~10⁵ | O(N log N) — ordenamiento, segment trees, Dijkstra con heap. |
| ~10⁶ | O(N) u O(N log log N) — recorridos lineales, cribas, hashing. |
| ~10⁸+ | O(log N) u O(1) por consulta — preprocesado, matemáticas, o estás haciendo streaming. |

Si el problema dice `N ≤ 20` y estás pensando en DP polinómica, estás pensando demasiado. Si `N ≤ 10⁶` y tu plan es O(N²), estás pensando muy poco.

**Límite de tiempo.** "2 segundos" combinado con N te cuenta la misma historia desde el otro lado. Las máquinas modernas hacen aproximadamente 10⁸–10⁹ operaciones simples por segundo. Multiplica tu N por tu big-O y verifica que el producto encaje.

**Límite de memoria.** 256 MB son aproximadamente 6×10⁷ ints. Si el problema te da N=10⁶ y pide una tabla N×N, necesitas espacio O(N) u O(log N) — eso te empuja hacia DP optimizado en espacio, arrays rodantes, o algoritmos in-place.

**Orden / estar ordenado.** "El array está ordenado" es un cartel gigante parpadeando que dice *búsqueda binaria, dos punteros o merge*. "Los valores son distintos" elimina casos de duplicados. "La entrada es una permutación de 1..N" abre la puerta a descomposición en ciclos y trucos de conteo.

**Mutabilidad.** ¿Puedes modificar la entrada? Si sí, los trucos in-place (negative-marking, swap-to-index) se vuelven gratis. Si no, necesitas espacio auxiliar O(N) como mínimo.

**Números reales vs. enteros.** Solo enteros abre counting sort, bitmask, aritmética modular y comparación exacta. Los floats te obligan a pensar en precisión, comparaciones con epsilon y formulaciones numéricamente estables.

**Online vs. offline.** Offline significa que ves todas las consultas de antemano — puedes reordenarlas, agruparlas, hacer sweep. Online significa que debes responder cada consulta antes de ver la siguiente — segment trees, BSTs balanceados, estructuras persistentes.

**Lee las restricciones primero, luego el problema.** No es un error tipográfico. Las restricciones a menudo te dicen la forma de la respuesta antes de que hayas leído cuál es la pregunta.

---

## La escalera fuerza bruta → mejor → óptimo

El hábito más importante de todo este documento.

**Paso 1 — Fuerza bruta.** Escribe la solución correcta más tonta que puedas. Prueba cada par, cada subconjunto, cada camino. No saltes esto. Si la fuerza bruta es demasiado lenta incluso para teclearla, escribe la *recurrencia* en papel.

Por qué importa:
- Fija qué significa "correcto" — ahora tienes una implementación de referencia para comparar.
- Expone la **estructura**. El cuello de botella de la solución bruta es donde vive la optimización.
- Desactiva el problema. Pasaste de "no sé cómo resolver esto" a "tengo una solución O(N³) que funciona y quiero hacerla más rápida" — son estados psicológicos distintos.

**Paso 2 — Hazte la única pregunta.** *¿Qué trabajo está haciendo la fuerza bruta que se está desperdiciando?*

Esta pregunta es el motor de prácticamente cada mejora algorítmica jamás inventada:

| Trabajo desperdiciado | Optimización que produce |
|---|---|
| Recomputar el mismo subproblema | Memoización → DP |
| Re-escanear un rango que acabamos de escanear | Sumas prefijo, ventana deslizante |
| Buscar linealmente en datos ordenados | Búsqueda binaria |
| Buscar un valor que podríamos haber indexado | Hash map |
| `min` repetido sobre una ventana móvil | Deque monótono |
| Re-recorrer un árbol que acabamos de recorrer | Euler tour, reuso de DFS |
| Probar opciones obviamente dominadas | Greedy + argumento de intercambio |
| Examinar aristas que no pueden mejorar la respuesta | Relajación de Dijkstra |

**Paso 3 — Óptimo (o suficientemente bueno).** Aplica la optimización. Verifica contra la solución bruta en entradas pequeñas. *Luego* preocúpate por las constantes, SIMD y comportamiento de caché — y usualmente no lo necesitas.

Saltar el paso 1 es el error más común de programadores intermedios. Van por la solución astuta, pierden un caso, y ahora están depurando una solución astuta que no entienden del todo. Fuerza bruta primero. Siempre.

---

## Cuándo abandonar — síntomas de que vas por el camino equivocado

Te vas a atascar. Atascarse está bien. Quedarse atascado por ego no. Señales de que tu plan actual está muerto:

- **30+ minutos sin código funcional y sin que el problema se reduzca.** No atascado en un bug — atascado en el enfoque. Empieza de nuevo con una página en blanco.
- **Tus casos límite siguen multiplicándose.** Cada arreglo introduce dos casos nuevos. La estructura de datos es incorrecta, o el invariante lo es.
- **Tu análisis de complejidad no cierra.** Ni siquiera puedes acotarlo en papel. El plan es incoherente; en realidad no sabes lo que hace.
- **Estás parcheando síntomas.** Añadiste `if (i == 0)`, luego `if (n == 1)`, luego `if (arr[i] < 0)`. Cada parche es señal de que tu lógica central no maneja un caso que debería haber manejado por construcción.
- **Estás cansado y el mismo bug sigue volviendo.** Aléjate diez minutos. No es pereza, es depuración.

**Cómo retroceder sin ego.** Escribe — literalmente escribe — lo que tu enfoque actual asume. ¿Cuál suposición es la más débil? Suéltala. A menudo el algoritmo correcto es hermano del que probaste, separado por una sola decisión de diseño (BFS vs. DFS, ordenar por inicio vs. fin, top-down vs. bottom-up).

Abandonar pronto es una habilidad. El costo de cambiar de enfoque en el minuto 15 es pequeño. El costo en el minuto 90 es catastrófico.

---

## Trampas cognitivas comunes

Estos son los modos de fallo recurrentes. Ponles nombre para poder detectarlos en ti mismo.

- **Optimización prematura.** Ir por el segment tree antes de comprobar si una suma prefijo bastaría. Ajustes de constante antes de corrección. La disciplina: *correcto, luego claro, luego rápido*.
- **Anclarse en la primera idea.** Tu primer plan se siente como *el* plan porque tú lo pensaste. Oblígate a generar al menos tres enfoques antes de elegir uno. El acto de comparar es lo que produce la perspicacia.
- **Negarse a escribir fuerza bruta.** "Es indigno de mí." "Obviamente es demasiado lento." Escríbelo igual. Es una implementación de referencia, un oráculo de pruebas y una ayuda para pensar. Cuesta cuatro minutos.
- **Miedo a la recursión.** La recursión es una notación, no un hechizo mágico. Si puedes escribir la recurrencia, puedes escribir la función. Si la recursión es demasiado profunda, conviértela en una pila — eso es una transformación mecánica, no un salto creativo.
- **Saltarse papel y lápiz.** Cada problema cabe en una tarjeta. Dibujar el array, esbozar el árbol, recorrer las primeras tres iteraciones a mano — esto encuentra bugs más rápido que cualquier depurador. El teclado es para teclear, no para pensar.
- **Leer la solución demasiado pronto.** Veinte minutos de lucha productiva enseñan más que dos horas de lectura. Si debes mirar, mira la *idea* (una oración) y luego cierra la pestaña.
- **Generalizar a partir de un ejemplo.** Tu código funciona en `[1,2,3]`. Prueba `[]`, `[5]`, `[5,5]`, `[5,4,3,2,1]`, `[-1,-2]`, y la entrada más grande. Los casos límite no son opcionales.
- **Leer mal la complejidad.** "Es O(N log N) porque ordené." Pero el bucle interno es O(N), entonces es O(N² log N). Recalcula cuando dudes.

---

## Los 7 arquetipos de problemas

La mayoría de problemas de entrevistas y competitivos son uno de estos disfrazados. Cada uno tiene un "olor" — la característica superficial que sugiere la forma subyacente.

| Arquetipo | Olor | Dónde en este repo |
|---|---|---|
| **Búsqueda y ordenamiento** | "Array ordenado", "encuentra el K-ésimo", "el más pequeño tal que…" | Semanas 8–9 |
| **Dos punteros** | "Par con propiedad X en array ordenado", "reordenar in-place" | Semana 30 |
| **Ventana deslizante** | "Subarray contiguo más largo/corto con propiedad X" | Semanas 6, 13, 30 |
| **BFS / DFS** | "Alcanzable", "conectado", "más corto en grafo sin peso", "explorar todo" | Semana 17 |
| **Programación dinámica** | "Cuenta el número de formas", "min/max sobre elecciones", "subestructura óptima con superposición" | Semanas 18, 23 |
| **Greedy** | "Programar", "menos cantidad de X", "puedes probar que la elección local es segura" | Semana 19 |
| **Divide y vencerás** | "Recursión sobre mitades", "fusionar resultados", "O(N log N) es plausible" | Semana 9 (merge/quick sort), Semana 27 (closest pair) |

Estos se superponen. La ventana deslizante es una especialización de dos punteros. La DP a menudo emerge de divide y vencerás con memoización. Greedy es DP cuando puedes probar que solo una elección importa. Las fronteras son borrosas — las etiquetas son andamiaje, no categorías de verdad.

Cuando llega un problema nuevo, haz un triaje rápido: ¿cuál de los siete olores tiene? Si dos, la respuesta probablemente los combina.

---

## Lista de lectura final

- **Polya, *How to Solve It* (1945).** Corto. Viejo. Aún el mejor libro sobre este tema. Léelo una vez al año.
- **Skiena, *The Algorithm Design Manual*, 3ª ed.** Capítulos 1–3 para la filosofía de resolución; las "war stories" son oro. El catálogo de la segunda mitad es referencia para programadores en activo.
- **CLRS (Cormen, Leiserson, Rivest, Stein), *Introduction to Algorithms*, 4ª ed.**
  - Capítulo 1 — El papel de los algoritmos.
  - Capítulo 2 — Getting started (insertion sort como ejemplo Polya trabajado).
  - Capítulo 4 — Divide y vencerás (recurrencias, teorema maestro).
  - Capítulo 15 — Programación dinámica (la derivación del rod-cutting es el walkthrough canónico de fuerza bruta → mejor → óptimo).
  - Capítulo 16 — Algoritmos greedy (y cómo probar correctness).
- **Bentley, *Programming Pearls*.** Columna 2 ("Aha! Algorithms") y Columna 8 ("Algorithm Design Techniques") son las más útiles para esta mentalidad.
- **Kleinberg & Tardos, *Algorithm Design*.** El walkthrough de gale-shapley del capítulo 1 es una clase magistral en convertir un problema vago en uno preciso.

Léelos junto con el currículo, no después. El punto no es terminarlos — es tenerlos abiertos cuando estés atascado.

---

> Los algoritmos en este repo son herramientas. La *resolución de problemas* es el taller. Pasa más tiempo en el taller que en la caja de herramientas.
