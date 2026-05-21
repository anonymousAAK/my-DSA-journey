> Esta es una traducción del original en inglés. Si algo no queda claro, consulta la [versión en inglés](../../docs/diagnostic.md).

# Diagnóstico — ¿Dónde deberías empezar?

15 preguntas a lo largo del currículo. Responde honestamente. Al final, mapeamos tus respuestas a una semana de inicio recomendada.

**No consultes nada mientras haces este test. El objetivo es calibrar, no puntuar.** Presupuesto de tiempo: ~25 minutos en total. Si pasas más de dos minutos en una sola pregunta, escribe tu mejor suposición y sigue.

Lleva una hoja de respuestas simple: `Q1: C`, `Q2: ...`, etc. Revela la clave de respuestas (colapsada al final) solo después de haber respondido las 15.

---

## Sección 1: Fundamentos y complejidad (Q1–Q3)

### Q1. ¿Cuál es la complejidad temporal de este código Python?

```python
def f(n):
    result = []
    for i in range(n):
        for j in range(i, n):
            result.append(i * j)
    return result
```

- A) O(N)
- B) O(N log N)
- C) O(N²)
- D) O(N³)

### Q2. Tienes un algoritmo que tarda 1 segundo con entrada N = 1,000. Suponiendo que el algoritmo es O(N log N), aproximadamente ¿cuánto tardará con N = 1,000,000?

- A) Cerca de 1,000 segundos (~17 minutos)
- B) Cerca de 2,000 segundos (~33 minutos)
- C) Cerca de 1,000,000 segundos (~12 días)
- D) Cerca de 10 segundos

### Q3. Respuesta corta. Un problema tiene restricciones `1 ≤ N ≤ 20`. Sin saber nada más del problema, ¿qué clase de algoritmo *se abre* con este N pequeño que sería inviable con N = 10⁵? Responde en una palabra o frase corta.

---

## Sección 2: Arrays y cadenas (Q4–Q5)

### Q4. Tienes un array ordenado de enteros distintos y un target. Necesitas encontrar dos índices cuyos valores sumen el target. ¿Cuál es el enfoque más limpio?

- A) Hash map: para cada `x`, busca `target - x`. O(N) tiempo, O(N) espacio.
- B) Dos punteros desde ambos extremos, moviéndose hacia adentro según la suma actual. O(N) tiempo, O(1) espacio.
- C) Búsqueda binaria del complemento de cada elemento. O(N log N) tiempo, O(1) espacio.
- D) Bucle anidado comprobando cada par. O(N²) tiempo, O(1) espacio.

> Múltiples opciones son *correctas* en el sentido de "pasaría". Elige la que aproveche **más** la estructura de la entrada.

### Q5. Estás procesando un stream de caracteres y quieres saber, en cada punto, la longitud de la subcadena más larga que termina en el carácter actual sin caracteres repetidos. ¿Qué técnica aplica?

- A) Ordenar la subcadena y deduplicar.
- B) Ventana deslizante con un hash set: expandir derecha, contraer izquierda mientras haya un duplicado en la ventana.
- C) Programación dinámica, `dp[i] = dp[i-1] + 1` siempre.
- D) Array de sufijos.

---

## Sección 3: Hash maps y estructuras (Q6–Q8)

### Q6. En una tabla hash de tamaño correcto en caso promedio, ¿cuál es la complejidad temporal de `insert`, `lookup` y `delete`?

- A) O(log N) las tres.
- B) O(1) amortizado promedio las tres.
- C) O(N) insert, O(1) lookup, O(N) delete.
- D) O(1) insert, O(N) lookup, O(N) delete.

### Q7. Necesitas una estructura que soporte `get(key)` y `put(key, value)` en O(1) promedio, Y evicte la clave menos recientemente usada cuando se excede la capacidad. ¿Qué dos estructuras compones?

- A) Dos pilas.
- B) Hash map + BST balanceado.
- C) Hash map + lista doblemente enlazada.
- D) Min-heap + hash set.

### Q8. Respuesta corta. En una oración: ¿cuándo elegirías un **trie** sobre un **hash map** para almacenar un conjunto de cadenas?

---

## Sección 4: Árboles, recursión y grafos (Q9–Q11)

### Q9. Dada la raíz de un árbol binario, escribes `depth(root) = 1 + max(depth(left), depth(right))` con caso base `depth(None) = 0`. Es una implementación correcta e idiomática. ¿Cuál es su complejidad de tiempo y espacio (espacio = stack de recursión), donde `N` es el número de nodos y `H` la altura?

- A) Tiempo O(N log N), espacio O(N).
- B) Tiempo O(N), espacio O(H).
- C) Tiempo O(H), espacio O(1).
- D) Tiempo O(N²), espacio O(N).

### Q10. Necesitas el camino más corto (en número de aristas) del nodo `s` al nodo `t` en un grafo **no dirigido sin pesos**. ¿Qué recorrido usas y por qué?

- A) DFS, porque explora primero en profundidad.
- B) BFS, porque visita los nodos en orden no decreciente de distancia-en-aristas desde la fuente.
- C) Dijkstra, porque es el algoritmo general de caminos más cortos.
- D) Ordenamiento topológico, porque da un orden.

### Q11. Respuesta corta. Te piden detectar un ciclo en un grafo **dirigido**. Decides usar DFS. ¿Qué estado auxiliar — más allá de un conjunto "visitados" — necesitas, y por qué? Una oración.

---

## Sección 5: DP y avanzado (Q12–Q15)

### Q12. ¿Cuál de estos problemas se resuelve *más limpiamente* con programación dinámica (en lugar de greedy, fuerza bruta o una sola pasada)?

- A) Dadas denominaciones de monedas y una cantidad, devuelve el **mínimo** número de monedas para hacer la cantidad. Las denominaciones son arbitrarias (p.ej. `[1, 3, 4]`, cantidad `6` → `2`, no `3`).
- B) Dada una lista de intervalos, encuentra el máximo de no superpuestos mutuamente.
- C) Dado un array, devuelve su suma.
- D) Dadas dos cadenas, comprueba si son anagramas.

### Q13. Ves "encuentra el número de formas distintas de ..." con una recurrencia de forma `f(n) = f(n-1) + f(n-2)` o similar, y restricciones hasta `N ≤ 10⁵`. La señal es:

- A) Greedy: toma el paso localmente mejor en cada `n`.
- B) DP: memoiza la recurrencia (o tabúlala). Cuida los subproblemas superpuestos.
- C) Backtracking: enumera todas las configuraciones.
- D) Hash map de valores `n` ya vistos.

### Q14. ¿En qué es bueno un **segment tree** que un array de sumas prefijo *no* lo es?

- A) Responder "suma de `a[l..r]`" en O(1) tras O(N) preprocesamiento, cuando el array es **estático**.
- B) Responder "suma de `a[l..r]`" con actualizaciones puntuales `a[i] = x` intercaladas con consultas, ambas en O(log N).
- C) Ordenar el array en O(N log N).
- D) Encontrar la mediana de un stream.

### Q15. Respuesta corta. En una oración, explica qué te permite modelar **network flow** (max-flow / min-cut) que BFS/DFS planos no. No te preocupes por nombres de algoritmos — solo el *tipo* de problema.

---

## Detente aquí. Puntúate solo después de responder las 15.

<details>
<summary><b>Click para revelar la clave de respuestas + placement</b></summary>

### Clave de respuestas

- **Q1: C** — el bucle externo corre N veces; el interno de `i` a `n`, total ops = N + (N-1) + ... + 1 = N(N+1)/2 ≈ N²/2. O(N²).
- **Q2: B** — N log N escala según `(N₂/N₁) · (log N₂ / log N₁) = 1000 · (20/10) ≈ 2000`. Así que ~2,000 segundos. La opción C sería O(N³); la A sería O(N²).
- **Q3** — **Bitmask DP** (o "enumeración de subconjuntos / fuerza bruta 2^N / búsqueda exponencial"). N ≤ 20 significa 2^N ≤ ~10⁶, lo que cabe en un segundo. Cubierto en la Semana 23.
- **Q4: B** — los dos punteros explotan la estructura **ordenada** para O(N) tiempo y O(1) espacio. A funciona pero desperdicia O(N) espacio; C desperdicia un factor log; D ignora el orden. El punto: elige la técnica que use *más* la estructura de la entrada.
- **Q5: B** — ventana deslizante clásica con hash set / mapa de last-seen-index. C es incorrecto porque `dp[i]` **no** siempre es `dp[i-1] + 1` — depende de si `s[i]` ya aparece en la ventana actual.
- **Q6: B** — O(1) amortizado promedio para las tres. El peor caso es O(N) si cada clave hashea al mismo bucket, pero la pregunta es caso promedio.
- **Q7: C** — hash map para lookup O(1), lista doblemente enlazada para reordenar O(1) en cada acceso. Es la estructura estándar de **LRU cache**, cubierta en las Semanas 11, 16 y 29.
- **Q8** — Cuando necesitas **consultas por prefijo** (p.ej. autocompletar, "¿alguna cadena almacenada empieza por `pre`?"), o cuando muchas cadenas almacenadas comparten prefijos largos (ahorro de memoria). Los hash maps tratan las claves como opacas; los tries explotan la estructura de prefijos compartidos.
- **Q9: B** — cada nodo se visita una vez → tiempo O(N). La profundidad de recursión iguala la altura del árbol → espacio O(H). Para un árbol balanceado, H = O(log N); para uno degenerado (similar a lista), H = N.
- **Q10: B** — BFS. La expansión nivel-a-nivel garantiza que cuando llegas por primera vez a un nodo, has usado el mínimo de aristas. Dijkstra también funciona pero es excesivo (y con un factor log innecesario) para grafos sin pesos.
- **Q11** — Necesitas un conjunto de **"actualmente en el stack de recursión" (a.k.a. "gris" o "in-progress")** además del conjunto de "completamente visitados" (negro). Una back edge a un nodo gris es un ciclo. Con un solo conjunto de visitados no puedes distinguir una cross/forward edge en un DAG de una verdadera back edge.
- **Q12: A** — coin change con denominaciones arbitrarias es el problema canónico de DP (greedy falla con `[1, 3, 4]` para cantidad `6` — greedy elige `4 + 1 + 1`; DP encuentra `3 + 3`). B es greedy (interval scheduling). C y D son una sola pasada.
- **Q13: B** — DP. La recurrencia de forma Fibonacci con subproblemas superpuestos es la señal de DP de libro. Con N ≤ 10⁵, la recursión naive es exponencial; memoiza o tabula.
- **Q14: B** — los segment trees manejan **actualizaciones puntuales + consultas de rango** en O(log N) cada una. Los arrays de sumas prefijo responden range-sum en O(1) pero requieren O(N) por actualización; solo son competitivos cuando el array es estático.
- **Q15** — Network flow modela **routing con restricciones de capacidad** a través de una red — puedes enviar hasta `c(u,v)` unidades por cada arista, y quieres el throughput total máximo de source a sink. Equivalentemente (dualidad min-cut), resuelve problemas como "¿cuál es el conjunto más pequeño de aristas para desconectar `s` de `t`?" BFS/DFS planos solo dicen alcanzabilidad o camino más corto; no razonan sobre *capacidad* o *flujo agregado*. Muchos problemas aparentemente no relacionados (bipartite matching, segmentación de imágenes, selección de proyectos) se reducen a max-flow.

### Matriz de colocación

Cuenta cuántas obtuviste *totalmente* correctas (para preguntas de respuesta corta, dúdate el crédito si tu respuesta captura la misma idea, aunque las palabras difieran).

| Puntuación | Punto de inicio recomendado |
|---|---|
| **0–3** | Empieza en la **Semana 1**. Los fundamentos son necesarios. No los saltes — pagan interés compuesto. |
| **4–7** | Hojea Semanas 1–5 (o salta si Q1–Q3 te resultaron fáciles). Trabajo serio en **Semana 6** (arrays) o **Semana 8** (búsqueda). |
| **8–11** | Empieza en **Semana 11** (listas enlazadas) o **Semana 14** (árboles), según dónde fallaste. Si fallaste Q9–Q11, Semana 14. Si fallaste Q6–Q8, Semana 16. |
| **12–15** | Empieza en **Semana 17** (grafos) o salta a temas avanzados (**Semanas 21+**). Si también clavaste Q14–Q15, ve directo a las Semanas 23–24 (DP avanzada y temas research). |

**Anomalías del diagnóstico — léelas también:**
- **Aprobaste las secciones 4–5 (Q9–Q15) pero suspendiste la sección 1 (Q1–Q3)**: inusual. Sabes escribir algoritmos pero no razonar sobre su coste. Revisa el análisis de complejidad en [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) — específicamente "Identificar restricciones". Luego vuelve a la Semana 8.
- **Aprobaste secciones 1–3 pero fallaste secciones 4–5**: perfil clásico. Tienes fundamentos sólidos pero no has construido vocabulario algorítmico. Salta al **camino de prep de entrevistas de 8 semanas** en el [README raíz](../../README.md#path-2-interview-prep-8-weeks) — Semanas 6, 8, 11, 14, 16, 17, 18, 30.
- **Acertaste Q3, Q8, Q11 o Q15 plenamente (respuesta corta)**: tienes el *vocabulario* de un practicante experimentado. Aunque tu MCQ sea medio, ve por el camino avanzado.

### Qué probó cada sección

| Sección | Probó | Cubierto en |
|---|---|---|
| 1 (Q1–Q3) | Intuición de complejidad, escalado big-O, lectura de restricciones | Semanas 1–5, 8; [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) |
| 2 (Q4–Q5) | Modismos de array y string — dos punteros, ventana deslizante | Semanas 6, 7, 10, 30 |
| 3 (Q6–Q8) | Hash maps, estructuras compuestas, tries | Semanas 11, 16, 21 |
| 4 (Q9–Q11) | Recursión, árboles, razonamiento de recorrido de grafos | Semanas 5, 14, 17 |
| 5 (Q12–Q15) | Reconocimiento de DP, segment trees, network flow | Semanas 18, 21, 23, 26 |

---

> Sea cual sea la semana en la que aterrices, deja tu puntaje del diagnóstico y la recomendación como la primera entrada de tu journal. Dentro de seis meses, cuando hayas olvidado lo que no sabías, será la instantánea más honesta de dónde empezaste.

</details>

---

## ¿Qué sigue?

- ¿Nuevo en la metodología? Prueba primero el [**Quickstart**](QUICKSTART.md) — 4 horas, 8 problemas, el bucle completo.
- ¿Listo para comprometerse? Ve al [**README raíz**](../../README.md) y elige un learning path.
- ¿Quieres la filosofía detrás del currículo? Lee [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md).
