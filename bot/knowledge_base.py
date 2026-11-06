"""Base de conocimiento del chatbot.

Cada entrada agrupa un tema con:
- ``tags``: palabras clave que activan la búsqueda.
- ``patterns``: formas típicas de preguntar (se usan para el índice).
- ``answer``: respuesta en Markdown (admite LaTeX y bloques de código).
- ``related``: temas que se ofrecen como preguntas de seguimiento.

Para añadir contenido nuevo basta con agregar otra instancia de ``Entry``.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    id: str
    title: str
    category: str
    tags: tuple[str, ...]
    patterns: tuple[str, ...]
    answer: str
    related: tuple[str, ...] = ()


CATEGORIES = ("Estática", "Programación", "Estática ↔ Python")


ENTRIES: tuple[Entry, ...] = (
    # ------------------------------------------------------------------
    # ESTÁTICA
    # ------------------------------------------------------------------
    Entry(
        id="peso-masa",
        title="Masa, peso y gravedad",
        category="Estática",
        tags=(
            "masa", "peso", "gravedad", "newton", "kilogramo", "w igual mg",
            "diferencia", "fuerza gravitatoria",
        ),
        patterns=(
            "¿Cuál es la diferencia entre masa y peso?",
            "Qué es el peso en física",
            "Cómo calcular el peso con la gravedad",
        ),
        answer=r"""La **masa** es la cantidad de materia (se mide en kg) y no cambia con la ubicación. El **peso** es la fuerza con que la gravedad atrae esa masa:

$$W = m\,g$$

- $m$ en $\text{kg}$
- $g$ en $\text{m/s}^2$ ($9{,}81$ en la Tierra, $1{,}62$ en la Luna)
- $W$ en $\text{N}$

**Ejemplo:** una masa de $70\ \text{kg}$ pesa
$$W = 70 \times 9{,}81 = 686{,}7\ \text{N}$$

**Errores comunes**
- Decir "peso" cuando se habla de masa (kg no es lo mismo que N).
- Poner la masa directamente en el DCL: allí va el **peso** $W$, no $m$.
- Usar $g=9{,}8$ o $10$ y mezclarlo con $9{,}81$ en el mismo problema.

**En código**

```python
def peso(masa_kg, g=9.81):
    '''Devuelve el peso en newtons.'''
    return masa_kg * g

print(f"Peso: {peso(70):.2f} N")
```

> La masa es un escalar; el peso es una fuerza y, por tanto, un vector dirigido hacia abajo (hacia el centro de la Tierra en problemas habituales).""",
        related=("unidades", "dcl", "friccion"),
    ),
    Entry(
        id="que-es-estatica",
        title="¿Qué es la estática?",
        category="Estática",
        tags=(
            "estatica", "mecanica", "definicion", "que estudia", "equilibrio",
            "ramas", "estudio de fuerzas", "introduccion",
        ),
        patterns=(
            "¿Qué es la estática?",
            "Qué estudia la estática",
            "Para qué sirve la estática en ingeniería",
        ),
        answer=r"""La **estática** es la rama de la mecánica que estudia cuerpos en **equilibrio**: sin aceleración, es decir, en reposo o moviéndose con velocidad constante. Su modelo ignora el tiempo y analiza cómo se compensan las fuerzas y los momentos.

**Idea central**
$$\sum \vec F = 0, \qquad \sum \vec M = 0$$

**Qué estudia**
- Fuerzas, vectores y momentos.
- Equilibrio de partículas y de cuerpos rígidos.
- Reacciones en apoyos y vínculos.
- Armaduras, cables y poleas.
- Centroides, centro de gravedad y fricción.
- Fuerzas internas en vigas (cortante y flector).

**Qué NO estudia**
- Movimiento y aceleraciones → eso es **dinámica**.
- Deformaciones y esfuerzos internos → **mecánica de materiales**.
- Resistencia o diseño de secciones → cálculo estructural.

**Por qué importa al programar**
Los problemas de estática se reducen muchas veces a sistemas de ecuaciones lineales, ideales para resolverlos con Python y NumPy.

> La estática es la base del análisis estructural: antes de calcular deformaciones hay que entender las fuerzas.""",
        related=("dcl", "equilibrio-rigido", "metodo-estatica"),
    ),
    Entry(
        id="dcl",
        title="Diagrama de cuerpo libre (DCL)",
        category="Estática",
        tags=(
            "diagrama de cuerpo libre", "dcl", "aislar cuerpo", "fuerzas externas",
            "dibujar fuerzas", "cuerpo libre",
        ),
        patterns=(
            "¿Cómo hago un diagrama de cuerpo libre?",
            "Qué es el DCL y para qué sirve",
            "Cómo aislar un cuerpo en estática",
        ),
        answer=r"""**El DCL** (diagrama de cuerpo libre) es el dibujo del cuerpo aislado con **todas las fuerzas externas** que actúan sobre él. Es el punto de partida de casi todo problema de estática.

**Cómo construirlo**
1. Elige el cuerpo, nudo o sección que vas a estudiar y dibújalo separado del resto.
2. Sustituye cada apoyo por la reacción que produce (ver *Tipos de apoyos*).
3. Coloca el peso $W = mg$ en el centro de gravedad.
4. Dibuja las fuerzas aplicadas y las tensiones de cables **saliendo** del cuerpo.
5. Define los ejes $x$–$y$ y el sentido positivo de los momentos (normalmente antihorario).

**Errores frecuentes**
- Incluir fuerzas internas o las que el cuerpo ejerce sobre otros.
- Olvidar una reacción o contarla dos veces.
- Dibujar la tensión de un cable empujando el cuerpo.

> Solo van fuerzas **externas que actúan sobre** el cuerpo elegido.""",
        related=("vectores", "apoyos", "equilibrio-particula"),
    ),
    Entry(
        id="vectores",
        title="Vectores, componentes y resultante",
        category="Estática",
        tags=(
            "vector", "componentes", "resultante", "descomponer fuerza", "seno",
            "coseno", "suma de fuerzas", "angulo",
        ),
        patterns=(
            "¿Cómo descompongo una fuerza en componentes?",
            "Cómo calculo la resultante de varias fuerzas",
            "Cómo usar seno y coseno en estática",
        ),
        answer=r"""Una fuerza es un vector: tiene **módulo**, **dirección** y **sentido**. Para sumar fuerzas conviene descomponerlas.

$$F_x = F\cos\theta,\qquad F_y = F\sin\theta$$

La resultante de varias fuerzas concurrentes:

$$R_x=\sum F_x,\qquad R_y=\sum F_y,\qquad R=\sqrt{R_x^2+R_y^2},\qquad \theta=\operatorname{atan2}(R_y,R_x)$$

**Ejemplo:** $F = 100\ \text{N}$ a $30^\circ$
- $F_x = 100\cos 30^\circ = 86{,}6\ \text{N}$
- $F_y = 100\sin 30^\circ = 50\ \text{N}$

**Cuidado con los cuadrantes:** usa `atan2` y no solo $\arctan(R_y/R_x)$, porque $\arctan$ repite valores cada $180^\circ$.

```python
import math

def componentes(modulo, angulo_grados):
    a = math.radians(angulo_grados)
    return modulo * math.cos(a), modulo * math.sin(a)

def resultante(fuerzas):
    rx = sum(componentes(f, a)[0] for f, a in fuerzas)
    ry = sum(componentes(f, a)[1] for f, a in fuerzas)
    r = math.hypot(rx, ry)
    theta = math.degrees(math.atan2(ry, rx)) % 360
    return r, theta

print(resultante([(100, 30), (80, 120)]))
```

> Los ángulos en Python se manejan en radianes: usa `math.radians` y `math.degrees` al convertir.""",
        related=("momento", "dcl", "numpy"),
    ),
    Entry(
        id="momento",
        title="Momento de una fuerza (torque)",
        category="Estática",
        tags=(
            "momento", "torque", "giro", "brazo de palanca", "perpendicular",
            "par de fuerzas", "varignon", "newton metro",
        ),
        patterns=(
            "¿Cómo calculo el momento de una fuerza?",
            "Qué es el torque o momento",
            "Cómo usar el teorema de Varignon",
        ),
        answer=r"""El **momento** (o torque) mide la tendencia de una fuerza a hacer girar un cuerpo alrededor de un punto:

$$M_O = F\,d_\perp$$

donde $d_\perp$ es la distancia **perpendicular** desde el punto $O$ a la línea de acción de la fuerza. Unidades: $\text{N}\cdot\text{m}$.

**Con signos:** $M_O = +Fd$ si gira en sentido antihorario y $-Fd$ si gira en sentido horario. Elige una convención y mantenla en todo el problema.

**Forma vectorial:** $\vec M_O = \vec r \times \vec F$.

**Teorema de Varignon:** el momento de una fuerza es igual a la suma de los momentos de sus componentes. Es muy útil con fuerzas inclinadas:
$$M_O = F_x\,d_y \pm F_y\,d_x$$

**Ejemplo:** una fuerza de $50\ \text{N}$ perpendicular a una llave de $0{,}3\ \text{m}$ produce
$$M = 50 \times 0{,}3 = 15\ \text{N}\cdot\text{m}$$

**Errores típicos**
- Usar la distancia al punto de aplicación en vez de la distancia perpendicular a la línea de acción.
- Mezclar signos dentro del mismo problema.
- Olvidar que una fuerza cuya línea de acción pasa por $O$ tiene momento nulo.""",
        related=("equilibrio-rigido", "vectores", "equilibrio-particula"),
    ),
    Entry(
        id="equilibrio-particula",
        title="Equilibrio de una partícula",
        category="Estática",
        tags=(
            "equilibrio", "particula", "nudo", "sumatoria de fuerzas", "tension",
            "cable", "sum fx", "sum fy", "incognitas",
        ),
        patterns=(
            "¿Cómo resuelvo el equilibrio de una partícula?",
            "Cómo calcular tensiones en un nudo",
            "Sumatoria de fuerzas igual a cero",
        ),
        answer=r"""Para una **partícula** (cuerpo cuyas dimensiones no importan, o un nudo) el equilibrio exige que la suma de fuerzas sea nula:

$$\sum F_x = 0, \qquad \sum F_y = 0$$

**Procedimiento**
1. Dibuja el DCL del nudo o partícula.
2. Descompone cada fuerza en $x$ e $y$.
3. Plantea las dos ecuaciones.
4. Resuelve el sistema (normalmente 2 incógnitas: tensiones o reacciones).
5. Verifica que los signos tengan sentido físico.

**Ejemplo:** un peso $W=500\ \text{N}$ sostenido por dos cables que forman $40^\circ$ y $60^\circ$ con la horizontal:

$$T_1\cos 40^\circ = T_2\cos 60^\circ$$
$$T_1\sin 40^\circ + T_2\sin 60^\circ = 500$$

> Si hay **3 incógnitas** en un nudo, el problema no se resuelve solo con $\sum F=0$: analiza otro nudo o el cuerpo completo.

Puedes resolver el sistema con `numpy.linalg.solve` (ver el tema *Sistemas de ecuaciones con NumPy*).""",
        related=("equilibrio-rigido", "dcl", "armaduras"),
    ),
    Entry(
        id="equilibrio-rigido",
        title="Equilibrio de un cuerpo rígido",
        category="Estática",
        tags=(
            "equilibrio", "cuerpo rigido", "sumatoria de momentos", "reacciones",
            "tres ecuaciones", "2d", "3d",
        ),
        patterns=(
            "¿Cuáles son las ecuaciones de equilibrio de un cuerpo rígido?",
            "Cómo plantear sumatoria de momentos",
            "Cómo resolver reacciones de una estructura",
        ),
        answer=r"""Para un **cuerpo rígido** en equilibrio se cumplen tres ecuaciones escalares en 2D:

$$\sum F_x = 0,\qquad \sum F_y = 0,\qquad \sum M_O = 0$$

**Consejos**
- Elige el punto $O$ para momentos donde **concurran** la mayor cantidad de fuerzas desconocidas: sus momentos se anulan.
- Puedes usar ecuaciones alternativas ($\sum M_A=0$, $\sum M_B=0$, $\sum F_x=0$) si los puntos no están alineados con las fuerzas.
- Resuelve primero la ecuación que tenga una sola incógnita.
- Al final, comprueba con una ecuación que no hayas usado.

En 3D hay 6 ecuaciones: $\sum F_x=\sum F_y=\sum F_z=0$ y $\sum M_x=\sum M_y=\sum M_z=0$.

**Señal de que algo va mal:** un resultado negativo **no** es un error; indica que el sentido supuesto es el contrario.

**Ejemplo:** viga simplemente apoyada con carga $F$ a distancia $a$:
$$\sum M_A=0 \Rightarrow R_B\,L - F\,a = 0 \Rightarrow R_B=\frac{Fa}{L}$$
$$R_A = F - R_B = F\frac{L-a}{L}$$""",
        related=("apoyos", "momento", "viga-reacciones"),
    ),
    Entry(
        id="apoyos",
        title="Tipos de apoyos y reacciones",
        category="Estática",
        tags=(
            "apoyo", "reaccion", "rodillo", "pasador", "empotramiento",
            "articulacion", "soporte", "cable", "guia", "vinculo",
        ),
        patterns=(
            "¿Qué reacciones produce cada tipo de apoyo?",
            "Diferencia entre rodillo y pasador",
            "Cómo saber cuántas incógnitas tiene un apoyo",
        ),
        answer=r"""Las **reacciones** dependen del tipo de apoyo. En 2D:

| Apoyo | Reacciones | Incógnitas |
|---|---|---|
| Rodillo / patín | 1 fuerza perpendicular a la superficie | 1 |
| Pasador / articulación | 2 componentes ($R_x$, $R_y$) | 2 |
| Empotramiento | $R_x$, $R_y$ y un momento $M$ | 3 |
| Cable / tirante | 1 tensión en la dirección del cable | 1 |
| Guía o collarín | 1 fuerza perpendicular + 1 momento | 2 |

**Claves**
- Un rodillo **no** impide el desplazamiento paralelo a la superficie.
- Un pasador **no** impide el giro, por eso no aporta momento.
- El empotramiento impide traslación y giro.
- Un cable solo puede tirar, nunca empujar.

Si el número de incógnitas supera las ecuaciones disponibles (3 en 2D), la estructura es **hiperestática** y necesitas herramientas adicionales, como la compatibilidad de deformaciones.

> Dibuja la reacción en la dirección en que el apoyo **impide** el movimiento.""",
        related=("equilibrio-rigido", "dcl", "viga-reacciones"),
    ),
    Entry(
        id="centroide",
        title="Centroides y centro de gravedad",
        category="Estática",
        tags=(
            "centroide", "centro de gravedad", "area compuesta", "primer momento",
            "figura compuesta", "baricentro", "centro geometrico",
        ),
        patterns=(
            "¿Cómo calculo el centroide de una figura compuesta?",
            "Qué es el centro de gravedad",
            "Fórmula del centroide de un área",
        ),
        answer=r"""El **centroide** de un área es su centro geométrico; el **centro de gravedad** coincide con él si el material es homogéneo.

$$\bar x = \frac{\sum A_i \bar x_i}{\sum A_i},\qquad \bar y = \frac{\sum A_i \bar y_i}{\sum A_i}$$

**Para figuras compuestas**
1. Divide la figura en partes simples (rectángulos, triángulos, semicírculos).
2. Toma un sistema de ejes de referencia.
3. Anota $A_i$, $\bar x_i$, $\bar y_i$ de cada parte.
4. Aplica las fórmulas; los **agujeros restan** área (usa $A_i$ negativa).
5. Verifica que el resultado quede dentro de la figura.

**Centroides útiles**
- Rectángulo: $(b/2,\ h/2)$ desde una esquina.
- Triángulo: a $1/3$ de la base y $1/3$ de la altura desde el lado recto.
- Círculo: el centro del círculo.
- Semicírculo: $\bar y = \dfrac{4r}{3\pi}$ desde el diámetro.

> El primer momento de área respecto al centroide es cero: $\sum A_i(\bar x_i-\bar x)=0$.""",
        related=("momento", "metodo-estatica"),
    ),
    Entry(
        id="friccion",
        title="Fricción estática",
        category="Estática",
        tags=(
            "friccion", "rozamiento", "estatico", "mu", "normal", "deslizamiento",
            "coeficiente", "movimiento inminente",
        ),
        patterns=(
            "¿Cómo funciona la fricción estática?",
            "Fórmula de la fuerza de rozamiento",
            "Cómo saber si un cuerpo se mueve o no",
        ),
        answer=r"""La **fricción estática** aparece cuando dos superficies intentan deslizar pero aún no se mueven.

$$f_s \le \mu_s N$$

- $N$: fuerza normal (perpendicular a la superficie).
- $\mu_s$: coeficiente de fricción estática (adimensional, depende de los materiales).
- La igualdad $f_s=\mu_s N$ se usa en el **umbral de movimiento inminente**.

**Pasos típicos**
1. DCL del cuerpo.
2. Si el cuerpo está quieto, $f_s$ es una incógnita que sale de $\sum F=0$.
3. Si preguntan "¿se mueve?", calcula la $f_s$ necesaria y compárala con $\mu_s N$.
4. Si la $f_s$ necesaria supera $\mu_s N$, el cuerpo desliza y entra en juego la fricción cinética.

**Ángulo de fricción:** $\tan\phi_s=\mu_s$.

**Error común:** suponer $f_s=\mu_s N$ cuando el cuerpo simplemente está en reposo; esa igualdad solo vale en el límite.""",
        related=("equilibrio-particula", "dcl"),
    ),
    Entry(
        id="armaduras",
        title="Armaduras: nudos y secciones",
        category="Estática",
        tags=(
            "armadura", "cercha", "truss", "nodos", "secciones", "barras",
            "traccion", "compresion", "fuerza cero",
        ),
        patterns=(
            "¿Cómo resuelvo una armadura por el método de nudos?",
            "Método de secciones en armaduras",
            "Qué son las barras de fuerza cero",
        ),
        answer=r"""Una **armadura** (cercha) es una estructura de barras rectas unidas por nudos articulados, cargada en los nudos.

**Hipótesis habituales**
- Las barras solo trabajan a **tracción o compresión** (fuerzas axiales).
- Los nudos son articulaciones sin fricción.
- Las cargas se aplican en los nudos.
- El peso de las barras se desprecia o se reparte.

**Método de nudos**
1. Calcula las reacciones globales.
2. Elige un nudo con **como máximo 2 barras desconocidas**.
3. Haz el DCL del nudo y supón todas las barras a tracción (saliendo del nudo).
4. Aplica $\sum F_x=0$ y $\sum F_y=0$. Un resultado negativo significa compresión.
5. Avanza nudo a nudo.

**Método de secciones** (cuando solo quieres una barra)
1. Corta la armadura por 3 barras como máximo.
2. Toma una parte y aplica $\sum M=0$ respecto al nudo donde concurren dos de las barras cortadas.
3. Despeja la tercera.

**Barras de fuerza cero:** si en un nudo sin carga solo concurren 2 barras no colineales, ambas tienen fuerza cero.

> Al final, todas las barras deben quedar resueltas y el equilibrio global debe cerrar.""",
        related=("equilibrio-particula", "numpy-sistemas", "python-estatica"),
    ),
    Entry(
        id="cortante",
        title="Fuerza cortante y momento flector",
        category="Estática",
        tags=(
            "cortante", "flector", "diagrama", "viga", "seccion", "carga distribuida",
            "momento maximo", "traccion fibra inferior",
        ),
        patterns=(
            "¿Cómo hago los diagramas de cortante y momento?",
            "Relación entre carga cortante y momento flector",
            "Dónde está el momento máximo de una viga",
        ),
        answer=r"""Los **diagramas de fuerza cortante $V$ y momento flector $M$** describen las fuerzas internas de una viga.

**Convención usual**
- $V$ positivo: la parte izquierda empuja hacia arriba a la derecha.
- $M$ positivo: produce tracción en la fibra inferior (curvatura cóncava hacia arriba).

**Relaciones diferenciales**
$$\frac{dV}{dx} = -w(x), \qquad \frac{dM}{dx} = V(x)$$
donde $w$ es la carga distribuida hacia abajo. Por eso:
- Carga puntual → salto en $V$.
- Momento puntual → salto en $M$.
- Tramo sin carga → $V$ constante y $M$ lineal.
- Carga uniforme → $V$ lineal y $M$ parabólico.

**Pasos**
1. Calcula las reacciones.
2. Corta a una distancia $x$ y plantea el equilibrio de uno de los lados.
3. Dibuja por tramos.
4. El máximo de $M$ ocurre donde $V=0$.

> Comprueba que $M$ vuelve a cero en los extremos sin momento aplicado.""",
        related=("viga-reacciones", "matplotlib", "apoyos"),
    ),
    Entry(
        id="cables-poleas",
        title="Cables y poleas",
        category="Estática",
        tags=(
            "cable", "polea", "tension", "cuerda", "polipasto", "peso",
            "nudo", "catenaria",
        ),
        patterns=(
            "¿Cómo calculo la tensión en un cable con poleas?",
            "Cómo resolver cables con cargas puntuales",
            "Qué tensión soporta una polea móvil",
        ),
        answer=r"""**Poleas ideales** (sin masa ni fricción): la tensión es la misma en toda la cuerda. Con una polea móvil, la fuerza se reparte entre los tramos de cuerda.

- Polea fija: cambia la dirección de la fuerza, no su magnitud.
- Polea móvil con 2 tramos: $T \approx W/2$.
- Polipasto con $n$ tramos de cuerda que sostienen la carga: $T \approx W/n$ (ideal).

**Cables con cargas puntuales**
1. DCL de cada nudo del cable.
2. Las tensiones siguen la dirección de cada tramo.
3. Aplica $\sum F_x=0$ y $\sum F_y=0$ en cada nudo.
4. La tensión máxima suele estar en el tramo más inclinado o con mayor carga.

**Cable sometido a su propio peso** (catenaria): la forma no es una parábola sino una catenaria; se estudia aparte.

> En un cable real la tensión no puede ser negativa: un cable no empuja.""",
        related=("equilibrio-particula", "vectores"),
    ),
    Entry(
        id="unidades",
        title="Unidades, signos y convenciones",
        category="Estática",
        tags=(
            "unidades", "signos", "convencion", "sistema internacional", "newton",
            "kilonewton", "metro", "consistencia",
        ),
        patterns=(
            "¿Qué unidades se usan en estática?",
            "Cómo elegir la convención de signos",
            "Por qué me salen resultados raros con las unidades",
        ),
        answer=r"""**Sistema Internacional (SI)**
- Fuerza: newton ($\text{N}$) — $1\ \text{N}=1\ \text{kg}\cdot\text{m/s}^2$
- Masa: kilogramo ($\text{kg}$)
- Longitud: metro ($\text{m}$)
- Momento: $\text{N}\cdot\text{m}$
- Presión o tensión: pascal ($\text{Pa}=\text{N/m}^2$)

**Convenciones que debes fijar antes de empezar**
- Ejes $x$ positivo a la derecha, $y$ positivo hacia arriba.
- Momentos positivos en sentido **antihorario**.
- Tracción positiva en barras (o compresión, pero sé consistente).

**Errores de unidades**
- Mezclar milímetros y metros: $1\ \text{mm}=0{,}001\ \text{m}$.
- Usar $g=9{,}81\ \text{m/s}^2$ con masas en kg para obtener peso en N.
- Comparar $\text{kN}\cdot\text{m}$ con $\text{N}\cdot\text{m}$ sin convertir.

> Truco: arrastra las unidades en las ecuaciones. Si el resultado no es $\text{N}$ o $\text{N}\cdot\text{m}$, hay un error.

**Equivalencias rápidas**
$$1\ \text{kN}=1000\ \text{N},\qquad 1\ \text{kgf}\approx 9{,}81\ \text{N},\qquad 1\ \text{cm}=0{,}01\ \text{m}$$""",
        related=("metodo-estatica", "unidades-codigo", "viga-reacciones"),
    ),
    Entry(
        id="metodo-estatica",
        title="Método general para resolver estática",
        category="Estática",
        tags=(
            "metodo", "pasos", "resolver problema", "estrategia", "procedimiento",
            "como empezar", "verificar",
        ),
        patterns=(
            "¿Cómo resuelvo un problema de estática paso a paso?",
            "Por dónde empiezo un ejercicio de estática",
            "Cómo verificar un resultado de estática",
        ),
        answer=r"""**Método general para resolver un problema de estática**

1. **Lee y dibuja:** identifica el cuerpo, las cargas y lo que te piden.
2. **DCL:** aísla el cuerpo y dibuja todas las fuerzas externas.
3. **Incógnitas:** cuenta reacciones y tensiones; compáralas con las ecuaciones disponibles (3 por cuerpo rígido en 2D).
4. **Elige ecuaciones inteligentemente:** toma momentos respecto a un punto donde concurran incógnitas.
5. **Resuelve:** despeja una incógnita por ecuación cuando sea posible.
6. **Verifica:** usa una ecuación no empleada y revisa signos, órdenes de magnitud y unidades.

**Si te trabas**
- ¿Falta una fuerza en el DCL?
- ¿Hay una fuerza interna que no debería estar?
- ¿El cuerpo es hiperestático?
- ¿Estás usando radianes cuando deberían ser grados (o al revés)?

> Escribe siempre las ecuaciones antes de sustituir números: es más fácil encontrar el error.""",
        related=("dcl", "equilibrio-rigido", "unidades"),
    ),
    Entry(
        id="viga-reacciones",
        title="Reacciones en una viga simplemente apoyada",
        category="Estática",
        tags=(
            "viga", "reacciones", "simplemente apoyada", "carga puntual", "luz",
            "carga distribuida", "apoyo izquierdo", "apoyo derecho",
        ),
        patterns=(
            "¿Cómo calculo las reacciones de una viga simplemente apoyada?",
            "Fórmula de reacciones con carga puntual",
            "Reacciones de una viga con carga distribuida",
        ),
        answer=r"""Para una **viga simplemente apoyada** con una carga puntual $F$ a distancia $a$ del apoyo izquierdo y luz $L$:

$$R_A = F\frac{L-a}{L}, \qquad R_B = F\frac{a}{L}$$

Cumplen $R_A+R_B=F$. La reacción del apoyo más cercano a la carga es mayor.

**Con carga distribuida uniforme** $w$ en toda la luz:
$$R_A = R_B = \frac{wL}{2}$$

**Pasos**
1. DCL con $R_A$, $R_B$ y las cargas.
2. $\sum M_A=0$ para despejar $R_B$.
3. $\sum F_y=0$ para obtener $R_A$.
4. Verifica con $\sum M_B=0$.

**Ejemplo:** $L=4\ \text{m}$, $F=1000\ \text{N}$ a $a=1\ \text{m}$:
$$R_B=1000\cdot\frac{1}{4}=250\ \text{N},\qquad R_A=1000-250=750\ \text{N}$$

Usa la **calculadora de viga** de la barra lateral para comprobar tus resultados.

> Con voladizos o cargas inclinadas el procedimiento es el mismo; solo cambian los brazos de palanca.""",
        related=("cortante", "apoyos", "numpy-sistemas"),
    ),
    # ------------------------------------------------------------------
    # PROGRAMACIÓN
    # ------------------------------------------------------------------
    Entry(
        id="que-es-programar",
        title="¿Qué es programar?",
        category="Programación",
        tags=(
            "programar", "programacion", "algoritmo", "lenguaje", "codigo",
            "computadora", "definicion", "que es", "software", "python",
        ),
        patterns=(
            "¿Qué es programar?",
            "Qué es la programación",
            "Qué es un algoritmo y un lenguaje de programación",
            "Cómo se usa Python",
        ),
        answer=r"""**Programar** es escribir instrucciones que una computadora ejecuta para resolver un problema. El código es la traducción de un **algoritmo** a un lenguaje que la máquina puede interpretar.

**Conceptos básicos**
- **Algoritmo:** secuencia finita y ordenada de pasos para resolver algo.
- **Lenguaje:** notación formal para expresar el algoritmo (Python, C, Java…).
- **Variable:** espacio con nombre donde se guarda un valor.
- **Estructuras de control:** condicionales y bucles que deciden el flujo.
- **Función:** bloque reutilizable que hace una tarea.
- **Error:** equivocación en la sintaxis, en la lógica o en los datos.

**Por qué Python es buena elección para empezar**
- Sintaxis legible, cercana al inglés.
- Es interpretado: ejecutas y ves resultados sin compilar.
- Tiene librerías para matemáticas, datos y gráficas (NumPy, Matplotlib).
- Se usa mucho en ingeniería y educación.

```python
def promedio(valores):
    '''Calcula la media de una lista de números.'''
    return sum(valores) / len(valores)

print(promedio([4.0, 3.5, 5.0]))   # 4.166...
```

> Programar no es memorizar sintaxis: es descomponer un problema en pasos pequeños y comprobables.

Si no sabes por dónde empezar, mira el tema **Cómo empezar a programar en Python**.""",
        related=("como-empezar", "variables", "errores"),
    ),
    Entry(
        id="como-empezar",
        title="Cómo empezar a programar en Python",
        category="Programación",
        tags=(
            "empezar", "aprender", "programar", "principiante", "desde cero",
            "ruta de aprendizaje", "primeros pasos", "estudiar",
        ),
        patterns=(
            "¿Cómo empiezo a programar en Python?",
            "Quiero aprender a programar desde cero",
            "Qué debo estudiar primero para programar",
        ),
        answer=r"""**Ruta sugerida para empezar con Python**

1. **Instala Python** y un editor (VS Code, PyCharm o incluso el IDLE que viene incluido).
2. **Variables y tipos de datos:** números, texto y booleanos.
3. **Condicionales y bucles:** `if`, `for` y `while`.
4. **Funciones:** aprender a dividir el problema en pasos pequeños.
5. **Colecciones:** listas y diccionarios.
6. **Errores y depuración:** leer el traceback y usar `print`.
7. **Librerías:** NumPy para cálculo y Matplotlib para gráficas.
8. **Un proyecto pequeño:** por ejemplo, una calculadora de reacciones o de resultantes.

**Consejos**
- Escribe código todos los días, aunque sean 20 minutos.
- No memorices: entiende qué hace cada línea.
- Copia ejemplos, modifícalos y rompelos a propósito para ver qué pasa.
- Divide los problemas grandes en funciones pequeñas.
- Cuando algo falle, lee el mensaje de error antes de pedir ayuda.

**Orden recomendado dentro de este chatbot**
*Variables → Condicionales → `for` → `while` → Funciones → Listas → Diccionarios → Errores → NumPy.*

> No necesitas saber matemáticas avanzadas para empezar; la lógica y la práctica importan más.""",
        related=("variables", "bucles-for", "funciones"),
    ),
    Entry(
        id="variables",
        title="Variables en Python",
        category="Programación",
        tags=(
            "variable", "asignar", "asignacion", "reasignar", "nombre", "type",
            "apuntar", "memoria",
        ),
        patterns=(
            "¿Qué es una variable en Python?",
            "Cómo asignar un valor a una variable",
            "Cómo comprobar el tipo de una variable",
        ),
        answer=r"""Una **variable** es un nombre que apunta a un valor en memoria. En Python no hace falta declarar el tipo: se infiere al asignar.

```python
nombre = "Ana"          # str
edad = 21               # int
promedio = 4.35         # float
activo = True           # bool
```

**Reglas y buenas prácticas**
- Nombres descriptivos en `snake_case`: `fuerza_total`, no `x`.
- Puede empezar con letra o guion bajo, nunca con un número.
- No uses palabras reservadas (`for`, `class`, `list`, `None`).
- Python distingue mayúsculas: `Fuerza` y `fuerza` son variables distintas.
- Asignación múltiple: `x, y = 1, 2`.
- Puedes cambiar el tipo al reasignar: `dato = "hola"` y luego `dato = 3`.

**Comprobar el tipo**

```python
print(type(edad))              # <class 'int'>
print(isinstance(edad, int))   # True
```

**Convertir**

```python
int("42")      # 42
float("3.5")   # 3.5
str(42)        # "42"
```

> Una variable no "contiene" el objeto: apunta a él. Si haces `b = a`, ambas apuntan al mismo objeto (muy importante con listas).

**Ver también:** *Tipos de datos* para `str`, `int`, `float` y `bool`.""",
        related=("tipos-datos", "condicionales", "funciones"),
    ),
    Entry(
        id="tipos-datos",
        title="Tipos de datos: str/string, int, float y bool/booleano",
        category="Programación",
        tags=(
            "tipo de dato", "tipos de datos", "string", "cadena", "str", "int",
            "float", "bool", "booleano", "entero", "decimal", "texto",
            "conversion", "convertir", "numero", "none",
        ),
        patterns=(
            "¿Qué es un string o cadena de texto?",
            "¿Qué tipos de datos hay en Python?",
            "Diferencia entre int y float",
            "¿Qué es un booleano?",
            "¿Cómo convierto texto a número?",
            "Cómo convertir entre tipos en Python",
        ),
        answer=r"""Python tiene tipos de datos integrados. Los más usados:

| Tipo | Nombre | Ejemplo | Para qué |
|---|---|---|---|
| `int` | entero | `42`, `-7` | conteos, índices |
| `float` | decimal | `3.14`, `9.81` | medidas y cálculos |
| `str` | cadena de texto | `"hola"`, `'N'` | texto |
| `bool` | booleano | `True`, `False` | condiciones |
| `NoneType` | nulo | `None` | "sin valor" |

**Strings (texto)**

```python
nombre = "Estática"
print(nombre[0])        # E
print(nombre.upper())   # ESTÁTICA
print(len(nombre))      # 8
print(f"Hola {nombre}")
```

**Números**

```python
entero = 10
decimal = 2.5

print(entero / 3)    # 3.333... (la división siempre devuelve float)
print(entero // 3)   # 3 (división entera)
print(entero % 3)    # 1 (resto)
print(2 ** 10)       # 1024 (potencia)
```

**Booleanos**

```python
activo = True
print(not activo)          # False
print(3 > 2 and 1 < 5)     # True
```

**Conversión entre tipos**

```python
int("42")        # 42
float("9.81")    # 9.81
str(3.14)        # "3.14"
bool(0)          # False
```

> `input()` siempre devuelve `str`. Si necesitas un número, conviértelo con `int()` o `float()` antes de operar.""",
        related=("variables", "fstrings", "validacion"),
    ),
    Entry(
        id="condicionales",
        title="Condicionales: if, elif y else",
        category="Programación",
        tags=(
            "if", "elif", "else", "condicional", "condicion", "comparar",
            "booleano", "indentacion", "and", "or", "not",
        ),
        patterns=(
            "¿Cómo funcionan los if y else en Python?",
            "Cómo comparar valores en Python",
            "Ejemplo de condicionales en Python",
        ),
        answer=r"""Los **condicionales** permiten ejecutar código según una condición booleana.

```python
nota = 3.8

if nota >= 4.5:
    print("Excelente")
elif nota >= 3.0:
    print("Aprobado")
else:
    print("Reprobado")
```

**Reglas**
- La indentación (4 espacios) define el bloque; no se usan llaves.
- `=` asigna; `==` compara.
- Operadores: `==`, `!=`, `<`, `<=`, `>`, `>=`.
- Para combinar: `and`, `or`, `not`.
- Cuidado al comparar floats por igualdad: usa `abs(a - b) < 1e-9`.

**Ejemplo aplicado:** verificar si una partícula está en equilibrio:

```python
tolerancia = 1e-6

if abs(sum_fx) < tolerancia and abs(sum_fy) < tolerancia:
    print("La partícula está en equilibrio")
else:
    print("Hay una fuerza resultante")
```

**Error frecuente:** poner `if x = 5:`. Eso asigna en lugar de comparar y provoca un `SyntaxError`.""",
        related=("variables", "bucles-for", "validacion"),
    ),
    Entry(
        id="bucles-for",
        title="Bucle for y range",
        category="Programación",
        tags=(
            "for", "bucle", "range", "iterar", "repetir", "recorrer", "enumerate",
            "lista", "acumulador",
        ),
        patterns=(
            "¿Cómo funciona el bucle for en Python?",
            "Cómo usar range en Python",
            "Cómo recorrer una lista con for",
        ),
        answer=r"""El **`for`** recorre una secuencia o repite un bloque un número conocido de veces.

```python
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

fuerzas = [100, 250, 75]
for f in fuerzas:
    print(f)

for i, f in enumerate(fuerzas, start=1):
    print(i, f)
```

**`range`**
- `range(n)`: de `0` a `n-1`.
- `range(a, b)`: de `a` a `b-1`.
- `range(a, b, paso)`: con incremento (puede ser negativo).

**Acumulador típico**

```python
suma = 0
for f in fuerzas:
    suma += f

promedio = suma / len(fuerzas)
```

> No modifiques una lista mientras la recorres; recorre una copia (`for f in fuerzas.copy()`) o crea una lista nueva.

**¿Cuándo usarlo?** Cuando sabes cuántas veces repetir o tienes una colección que recorrer.""",
        related=("listas", "bucles-while", "funciones"),
    ),
    Entry(
        id="bucles-while",
        title="Bucle while y validación",
        category="Programación",
        tags=(
            "while", "bucle", "repetir", "condicion", "infinito", "break",
            "continue", "validar", "hasta que",
        ),
        patterns=(
            "¿Cómo funciona el while en Python?",
            "Diferencia entre for y while",
            "Cómo evitar un bucle infinito",
        ),
        answer=r"""El **`while`** repite mientras una condición sea verdadera. Úsalo cuando **no sabes cuántas iteraciones** harán falta.

```python
intentos = 0
while intentos < 3:
    print("Intento", intentos + 1)
    intentos += 1
```

**Validación de entrada**

```python
while True:
    texto = input("Fuerza en N: ")
    try:
        fuerza = float(texto)
        break
    except ValueError:
        print("Ingresa un número válido")
```

**Riesgos**
- Olvidar actualizar la condición → **bucle infinito**.
- Usa `break` para salir o `continue` para saltar a la siguiente iteración.

**¿`for` o `while`?**
- Número de repeticiones conocido → `for`.
- Repetir "hasta que pase algo" → `while`.

> Si el programa se queda colgado, revisa qué variable de la condición debería cambiar dentro del bucle.""",
        related=("bucles-for", "validacion", "errores"),
    ),
    Entry(
        id="funciones",
        title="Funciones en Python",
        category="Programación",
        tags=(
            "funcion", "def", "return", "parametro", "argumento", "reutilizar",
            "docstring", "scope", "llamar",
        ),
        patterns=(
            "¿Cómo se define una función en Python?",
            "Diferencia entre parámetro y argumento",
            "Cómo devolver un valor de una función",
        ),
        answer=r"""Una **función** agrupa código reutilizable con un nombre.

```python
def peso(masa, gravedad=9.81):
    '''Devuelve el peso en newtons.'''
    return masa * gravedad

print(peso(10))          # 98.1
print(peso(10, 1.62))    # 16.2 (Luna)
```

**Partes**
- `def nombre(parametros):`
- `return` devuelve un valor (si no hay, devuelve `None`).
- Los parámetros con valor por defecto van al final.
- Las variables creadas dentro son **locales**.

**Buenas prácticas**
- Una función = una responsabilidad.
- Nombres con verbo: `calcular_resultante`, `convertir_unidades`.
- Documenta con un docstring.
- Evita `print` dentro de funciones de cálculo: devuelve el valor y muestra fuera.

```python
def reaccion_viga(L, a, F):
    if not 0 <= a <= L:
        raise ValueError("a debe estar entre 0 y L")
    return F * (L - a) / L
```

> Si una función no devuelve nada, no podrás usar su resultado en otra operación.""",
        related=("variables", "listas", "clases"),
    ),
    Entry(
        id="listas",
        title="Listas en Python",
        category="Programación",
        tags=(
            "lista", "array", "indice", "append", "recorrer", "slicing",
            "comprehension", "mutar", "copiar",
        ),
        patterns=(
            "¿Cómo se usa una lista?",
            "Cómo agregar elementos a una lista",
            "Diferencia entre lista y arreglo de NumPy",
        ),
        answer=r"""Una **lista** es una colección ordenada y mutable.

```python
fuerzas = [100.0, 250.0, 75.0]
fuerzas.append(50)        # agrega al final
fuerzas[0]                # 100.0
fuerzas[-1]               # 50
fuerzas[1:3]              # [250.0, 75.0]
len(fuerzas)              # 4
sum(fuerzas)              # 475.0
```

**Métodos útiles**
`append`, `extend`, `insert`, `remove`, `pop`, `sort`, `reverse`, `index`, `count`.

**Listas por comprensión**

```python
pesos = [m * 9.81 for m in [10, 20, 30]]
mayores = [f for f in fuerzas if f > 100]
```

**Copiar (¡importante!)**

```python
a = [1, 2, 3]
b = a          # mismo objeto
c = a.copy()   # lista independiente
```

> Para datos numéricos grandes, usa `numpy.array` en lugar de listas.

**Error típico:** `IndexError` por pedir una posición que no existe. Recuerda que el último índice es `len(lista) - 1`.""",
        related=("bucles-for", "diccionarios", "numpy"),
    ),
    Entry(
        id="diccionarios",
        title="Diccionarios en Python",
        category="Programación",
        tags=(
            "diccionario", "clave", "valor", "dict", "items", "get", "json",
            "anidado",
        ),
        patterns=(
            "¿Cómo funciona un diccionario en Python?",
            "Cómo recorrer un diccionario",
            "Diferencia entre lista y diccionario",
        ),
        answer=r"""Un **diccionario** guarda pares clave–valor.

```python
material = {
    "nombre": "Acero",
    "densidad": 7850,   # kg/m^3
    "E": 200e9,         # Pa
}

print(material["densidad"])
print(material.get("poisson", "no definido"))
material["poisson"] = 0.3
```

**Recorrer**

```python
for clave, valor in material.items():
    print(clave, valor)
```

**Métodos útiles:** `keys()`, `values()`, `items()`, `get()`, `pop()`, `update()`.

**Anidados**

```python
secciones = {
    "viga1": {"L": 4.0, "carga": 1200},
    "viga2": {"L": 6.0, "carga": 800},
}

print(secciones["viga1"]["carga"])
```

> Usa `[]` cuando la clave debe existir y `get()` cuando puede faltar. Un `KeyError` casi siempre es una clave mal escrita.""",
        related=("listas", "archivos", "clases"),
    ),
    Entry(
        id="errores",
        title="Errores comunes y traceback",
        category="Programación",
        tags=(
            "error", "excepcion", "traceback", "index error", "key error",
            "type error", "name error", "value error", "syntax error", "try except",
        ),
        patterns=(
            "¿Cómo leer un error de Python?",
            "Qué significa IndexError o KeyError",
            "Cómo usar try y except",
        ),
        answer=r"""**Cómo leer un error en Python**

Lee el **traceback de abajo hacia arriba**:
1. La última línea indica el tipo de error y el mensaje.
2. La línea anterior muestra el archivo y la línea del código.

| Error | Causa típica |
|---|---|
| `SyntaxError` | Falta `:`, paréntesis o comillas |
| `IndentationError` | Indentación inconsistente |
| `NameError` | Variable no definida o mal escrita |
| `TypeError` | Operación entre tipos incompatibles (`"2" + 2`) |
| `ValueError` | El tipo es correcto pero el valor no (`int("hola")`) |
| `IndexError` | Índice fuera de rango |
| `KeyError` | Clave inexistente en un diccionario |
| `ZeroDivisionError` | División entre cero |
| `AttributeError` | El objeto no tiene ese método o atributo |

**Manejo de errores**

```python
try:
    fuerza = float(input("Fuerza: "))
except ValueError:
    print("Eso no es un número")
```

**Depuración rápida**
- Imprime las variables antes de la línea que falla.
- Revisa los tipos con `type()`.
- Comenta bloques para aislar el problema.

> No uses `except:` vacío: oculta el error y hace más difícil encontrarlo.""",
        related=("debug", "validacion", "bucles-while"),
    ),
    Entry(
        id="recursividad",
        title="Recursividad",
        category="Programación",
        tags=(
            "recursividad", "recursiva", "recursion", "factorial", "caso base",
            "pila", "recursion error",
        ),
        patterns=(
            "¿Qué es la recursividad en Python?",
            "Cómo hacer una función recursiva",
            "Qué es el caso base de una recursión",
        ),
        answer=r"""Una función **recursiva** se llama a sí misma y necesita:

1. Un **caso base** que detenga la recursión.
2. Un **caso recursivo** que reduzca el problema.

```python
def factorial(n):
    if n < 0:
        raise ValueError("n debe ser >= 0")
    if n in (0, 1):          # caso base
        return 1
    return n * factorial(n - 1)
```

**Qué pasa internamente** con `factorial(4)`:
$$4 \times 3 \times 2 \times 1 = 24$$

**Cuidado**
- Sin caso base, o con uno inalcanzable → `RecursionError`.
- Cada llamada consume memoria (pila).
- Para cálculos numéricos grandes, prefiere un bucle.

**Cuándo usarla:** estructuras recursivas (árboles, carpetas), divide y vencerás, o cuando la versión iterativa es mucho más compleja.

> Regla práctica: si puedes escribirlo fácil con un `for`, usa el `for`.""",
        related=("funciones", "errores"),
    ),
    Entry(
        id="numpy",
        title="NumPy básico",
        category="Programación",
        tags=(
            "numpy", "array", "arreglo", "vector", "matriz", "linspace",
            "operaciones", "vectorizado", "linalg",
        ),
        patterns=(
            "¿Cómo empiezo con NumPy?",
            "Diferencia entre lista y array de NumPy",
            "Cómo hacer operaciones con vectores en NumPy",
        ),
        answer=r"""**NumPy** aporta arreglos rápidos y operaciones vectorizadas.

```python
import numpy as np

v = np.array([3.0, 4.0])
print(np.linalg.norm(v))    # 5.0

A = np.array([[1.0, 2.0], [3.0, 4.0]])
b = np.array([5.0, 11.0])
x = np.linalg.solve(A, b)
print(x)
```

**Diferencias con listas**
- Operaciones elemento a elemento: `v * 2`, `v + 1`.
- Funciones: `np.sin`, `np.cos`, `np.sqrt`, `np.sum`, `np.mean`.
- Indexado y slicing similares, pero `v[0]` devuelve un escalar.
- `np.linspace(a, b, n)` genera $n$ puntos entre $a$ y $b$.

**Para estática**

```python
fuerzas = np.array([[100, 30], [80, 120]])  # [modulo, angulo]
ang = np.radians(fuerzas[:, 1])
fx = fuerzas[:, 0] * np.cos(ang)
fy = fuerzas[:, 0] * np.sin(ang)
R = np.hypot(fx.sum(), fy.sum())
theta = np.degrees(np.arctan2(fy.sum(), fx.sum())) % 360
print(R, theta)
```

> NumPy trabaja en radianes: usa `np.radians()` al convertir desde grados.""",
        related=("listas", "numpy-sistemas", "matplotlib"),
    ),
    Entry(
        id="matplotlib",
        title="Gráficas con Matplotlib",
        category="Programación",
        tags=(
            "matplotlib", "grafico", "plot", "figura", "eje", "visualizar",
            "diagrama", "streamlit", "pyplot",
        ),
        patterns=(
            "¿Cómo hago una gráfica en Python?",
            "Cómo mostrar una gráfica en Streamlit",
            "Cómo graficar un diagrama de cortante",
        ),
        answer=r"""**Matplotlib** sirve para visualizar resultados: diagramas de cortante, trayectorias, funciones.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 4, 200)
y = x**2

plt.plot(x, y, label="y = x²")
plt.xlabel("x (m)")
plt.ylabel("y")
plt.title("Parábola")
plt.grid(True)
plt.legend()
plt.show()
```

**En Streamlit** usa `st.pyplot(fig)`:

```python
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("y")
st.pyplot(fig)
```

**Diagrama de cortante típico**

```python
ax.plot(x, V, drawstyle="steps-post")  # saltos en cargas puntuales
ax.axhline(0, color="black", linewidth=0.8)
```

**Buenas prácticas**
- Etiqueta ejes y unidades.
- Usa `fig.tight_layout()`.
- Cierra figuras en scripts largos: `plt.close(fig)`.""",
        related=("numpy", "cortante", "fstrings"),
    ),
    Entry(
        id="validacion",
        title="Validar datos de entrada",
        category="Programación",
        tags=(
            "validar", "input", "usuario", "dato", "numero", "float", "rango",
            "error", "while",
        ),
        patterns=(
            "¿Cómo valido la entrada del usuario en Python?",
            "Cómo pedir un número y evitar errores",
            "Cómo comprobar que un dato esté en un rango",
        ),
        answer=r"""Validar la entrada evita que el programa se caiga con datos del usuario.

```python
def pedir_float(mensaje, minimo=None):
    while True:
        try:
            valor = float(input(mensaje))
        except ValueError:
            print("Debes ingresar un número.")
            continue
        if minimo is not None and valor < minimo:
            print(f"El valor debe ser >= {minimo}.")
            continue
        return valor

luz = pedir_float("Luz de la viga (m): ", minimo=0.1)
```

**Qué validar**
- Tipo correcto (`float`, `int`).
- Rangos físicos: longitudes $>0$, ángulos entre $0$ y $360$, coeficientes $\ge 0$.
- Coherencia entre datos (por ejemplo, $a \le L$).

**En Streamlit** usa `st.number_input` con `min_value`, o valida después y muestra `st.error`.

**Ejemplo de coherencia**

```python
if not 0 <= distancia <= luz:
    raise ValueError("La carga debe estar dentro de la viga")
```

> Nunca confíes en que el usuario escribirá lo que esperas.""",
        related=("bucles-while", "errores", "unidades-codigo"),
    ),
    Entry(
        id="debug",
        title="Depurar código (debug)",
        category="Programación",
        tags=(
            "depurar", "debug", "print", "breakpoint", "assert", "revisar",
            "logging", "error logico",
        ),
        patterns=(
            "¿Cómo puedo depurar mi código?",
            "Cómo encontrar un error lógico en Python",
            "Para qué sirve breakpoint o assert",
        ),
        answer=r"""**Estrategia para depurar**

1. **Reproduce** el error con el caso más pequeño posible.
2. **Lee el traceback** completo: tipo de error, mensaje y línea.
3. **Inspecciona** los valores justo antes del fallo:
   ```python
   print("x =", x, "tipo:", type(x))
   ```
4. **Divide y vencerás:** comenta mitades del código para localizar el bloque.
5. **Comprueba supuestos** con `assert`:
   ```python
   assert L > 0, "La luz debe ser positiva"
   ```
6. **Usa el depurador** si está disponible: `breakpoint()` y ejecuta paso a paso.

**Preguntas que ayudan**
- ¿Qué esperaba que pasara?
- ¿Qué pasó realmente?
- ¿Cuál es el primer valor que no coincide con lo esperado?

**En Python moderno** también puedes usar `logging` en lugar de `print` para no llenar la consola.

> Explica el código en voz alta: muchas veces el error aparece al intentar describirlo.

**Errores lógicos frecuentes:** índices desfasados, usar `=` en vez de `==`, olvidar convertir unidades o dividir por cero.""",
        related=("errores", "funciones", "validacion"),
    ),
    Entry(
        id="clases",
        title="Clases y objetos (POO)",
        category="Programación",
        tags=(
            "clase", "objeto", "poo", "init", "atributo", "metodo", "self",
            "constructor", "programacion orientada a objetos",
        ),
        patterns=(
            "¿Cómo se crea una clase en Python?",
            "Qué es self y __init__",
            "Ejemplo de programación orientada a objetos",
        ),
        answer=r"""Una **clase** define un molde para crear objetos con datos (atributos) y comportamientos (métodos).

```python
from math import cos, sin, radians

class Fuerza:
    def __init__(self, modulo, angulo):
        self.modulo = float(modulo)
        self.angulo = float(angulo)

    @property
    def componentes(self):
        a = radians(self.angulo)
        return self.modulo * cos(a), self.modulo * sin(a)

    def __repr__(self):
        return f"Fuerza({self.modulo} N, {self.angulo}°)"

f = Fuerza(100, 30)
print(f.componentes)
print(f)
```

**Conceptos**
- `__init__`: constructor, inicializa atributos.
- `self`: referencia al objeto actual.
- Métodos: funciones dentro de la clase.
- `__repr__`: representación legible para depurar.

**Cuándo usar clases:** cuando varios datos y operaciones van siempre juntos (fuerzas, materiales, vigas).

> No uses clases para todo: para un cálculo suelto, una función es más simple.""",
        related=("funciones", "diccionarios", "python-estatica"),
    ),
    Entry(
        id="fstrings",
        title="Formato con f-strings",
        category="Programación",
        tags=(
            "f-string", "formato", "imprimir", "texto", "redondear", "decimales",
            "print", "porcentaje", "alinear",
        ),
        patterns=(
            "¿Cómo formatear números en Python?",
            "Cómo redondear al imprimir con f-strings",
            "Cómo unir texto y variables",
        ),
        answer=r"""Los **f-strings** formatean texto de forma clara y rápida.

```python
masa = 12.3456

print(f"Masa: {masa:.2f} kg")        # 2 decimales
print(f"Valor: {masa:10.3f}")        # ancho 10
print(f"Porcentaje: {0.456:.1%}")    # 45.6%
print(f"{'izquierda':<10}|")         # alineación
print(f"{42:05d}")                   # 00042
```

**Útil para reportes**

```python
print(f"R = {R:.2f} N a {theta:.1f}°")
print(f"¿Equilibrio? {'sí' if ok else 'no'}")
```

**Alternativas:** `"{}".format(valor)` y `%`, pero los f-strings son más legibles.

> Para depurar desde Python 3.8: `f"{variable=}"` imprime `variable=valor`.

**Cuidado:** no metas comillas dobles dentro de un f-string delimitado por comillas dobles; usa comillas simples en el interior.""",
        related=("variables", "matplotlib", "debug"),
    ),
    Entry(
        id="archivos",
        title="Leer y escribir archivos",
        category="Programación",
        tags=(
            "archivo", "leer", "escribir", "open", "csv", "guardar", "with",
            "pathlib", "encoding",
        ),
        patterns=(
            "¿Cómo leo un archivo en Python?",
            "Cómo guardar resultados en un archivo",
            "Cómo leer un CSV con Python",
        ),
        answer=r"""Para **leer o escribir archivos** usa `with open(...)`; cierra el archivo automáticamente aunque ocurra un error.

```python
with open("resultados.txt", "w", encoding="utf-8") as f:
    f.write("R = 123.45 N\n")
    f.write("theta = 30.0 grados\n")

with open("resultados.txt", "r", encoding="utf-8") as f:
    for linea in f:
        print(linea.strip())
```

**Modos:** `"r"` leer, `"w"` sobrescribir, `"a"` agregar, `"x"` crear (falla si existe).

**CSV**

```python
import csv

with open("datos.csv", newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        print(fila["fuerza"])
```

**Rutas modernas**

```python
from pathlib import Path

ruta = Path("datos") / "resultados.txt"
ruta.write_text("hola", encoding="utf-8")
```

> Usa siempre `encoding="utf-8"` para evitar problemas con tildes y símbolos.""",
        related=("diccionarios", "errores", "fstrings"),
    ),
    # ------------------------------------------------------------------
    # PUENTE ESTÁTICA ↔ PYTHON
    # ------------------------------------------------------------------
    Entry(
        id="numpy-sistemas",
        title="Sistemas de ecuaciones con NumPy",
        category="Estática ↔ Python",
        tags=(
            "sistema", "ecuacion", "ecuaciones", "solve", "numpy", "matriz",
            "equilibrio", "incognitas", "linalg",
        ),
        patterns=(
            "¿Cómo resuelvo un sistema de ecuaciones con NumPy?",
            "Cómo resolver tensiones con numpy.linalg.solve",
            "Cómo plantear el equilibrio como matriz",
        ),
        answer=r"""Muchos problemas de equilibrio terminan en un **sistema lineal** $A\vec x=\vec b$. NumPy lo resuelve directo:

```python
import numpy as np

# 2 ecuaciones: sum Fx = 0 y sum Fy = 0
# Incógnitas: T1 y T2
A = np.array([
    [np.cos(np.radians(40)), -np.cos(np.radians(60))],
    [np.sin(np.radians(40)),  np.sin(np.radians(60))],
])
b = np.array([0.0, 500.0])   # peso de 500 N hacia abajo

x = np.linalg.solve(A, b)
print(f"T1 = {x[0]:.2f} N, T2 = {x[1]:.2f} N")
```

**Verifica siempre**

```python
assert np.allclose(A @ x, b), "La solución no satisface el sistema"
```

**Buenas prácticas**
- Escribe las ecuaciones en forma estándar: coeficientes a la izquierda, constantes a la derecha.
- Mantén las unidades consistentes.
- Comprueba el determinante: si es casi cero, el sistema es indeterminado o inconsistente.
- Para sistemas no cuadrados usa `np.linalg.lstsq`.

**Signos:** el vector de incógnitas debe contener las tensiones con el signo que supusiste. Si sale negativo, la dirección real es la opuesta.""",
        related=("numpy", "equilibrio-particula", "python-estatica"),
    ),
    Entry(
        id="python-estatica",
        title="Calcular estática con Python",
        category="Estática ↔ Python",
        tags=(
            "calcular", "script", "resultante", "momento", "ejemplo", "automatizar",
            "dataclass", "fuerza", "programa",
        ),
        patterns=(
            "¿Cómo calculo fuerzas y momentos con Python?",
            "Ejemplo de script para estática",
            "Cómo automatizar cálculos de estática",
        ),
        answer=r"""Puedes automatizar los cálculos de estática con Python. Ejemplo de una clase sencilla para sumar fuerzas y momentos:

```python
from dataclasses import dataclass
from math import cos, sin, radians


@dataclass
class Fuerza:
    fx: float
    fy: float
    x: float = 0.0   # punto de aplicación
    y: float = 0.0

    @classmethod
    def polar(cls, modulo, angulo, x=0.0, y=0.0):
        a = radians(angulo)
        return cls(modulo * cos(a), modulo * sin(a), x, y)


def resultante(fuerzas):
    rx = sum(f.fx for f in fuerzas)
    ry = sum(f.fy for f in fuerzas)
    return rx, ry


def momento_en_origen(fuerzas):
    # M = x*Fy - y*Fx  (producto vectorial r x F)
    return sum(f.x * f.fy - f.y * f.fx for f in fuerzas)


fs = [Fuerza.polar(100, 30), Fuerza.polar(80, 120, x=2)]
rx, ry = resultante(fs)
print(f"R = {rx:.2f} i + {ry:.2f} j N")
print(f"Mo = {momento_en_origen(fs):.2f} N·m")
```

**Ventajas**
- Repites cálculos con distintos datos sin rehacer cuentas.
- Puedes graficar y comparar casos.
- Sirve para verificar resultados hechos a mano.

> Escribe funciones pequeñas y compruébalas con un caso conocido antes de confiar en el script.""",
        related=("clases", "numpy", "vectores"),
    ),
    Entry(
        id="unidades-codigo",
        title="Unidades y conversiones en código",
        category="Estática ↔ Python",
        tags=(
            "unidades", "conversion", "magnitud", "codigo", "si", "milimetros",
            "kilonewton", "error", "nombres",
        ),
        patterns=(
            "¿Cómo evitar errores de unidades en mi código?",
            "Cómo convertir kN a N en Python",
            "Buenas prácticas de unidades al programar",
        ),
        answer=r"""Mezclar unidades es una de las causas más comunes de resultados absurdos.

**Reglas prácticas**
1. Guarda **todo en SI** dentro del código ($\text{m}$, $\text{N}$, $\text{kg}$, $\text{s}$).
2. Convierte al **entrar** y al **salir** de la función.
3. Nombra las variables con su unidad: `luz_m`, `carga_n`, `angulo_deg`.
4. Documenta las unidades en el docstring.

```python
def reaccion_viga(luz_m, carga_n, distancia_m):
    '''Reacciones de una viga simplemente apoyada. Todo en SI.'''
    if luz_m <= 0:
        raise ValueError("La luz debe ser positiva")
    if not 0 <= distancia_m <= luz_m:
        raise ValueError("La carga debe estar dentro de la viga")
    return carga_n * (luz_m - distancia_m) / luz_m


RA = reaccion_viga(luz_m=4.0, carga_n=1200, distancia_m=1.5)
```

**Conversiones frecuentes**
- $1\ \text{kN} = 1000\ \text{N}$
- $1\ \text{mm} = 0{,}001\ \text{m}$
- $1\ \text{cm} = 0{,}01\ \text{m}$
- $1\ \text{kgf} \approx 9{,}81\ \text{N}$

**En Python** usa `math.radians` / `math.degrees`; NumPy también los incluye.

> Un test sencillo con un caso conocido detecta la mayoría de errores de unidades.""",
        related=("unidades", "funciones", "validacion"),
    ),
)


# Índice auxiliar para no recorrer la tupla completa en cada búsqueda.
ENTRIES_BY_ID: dict[str, Entry] = {entry.id: entry for entry in ENTRIES}
