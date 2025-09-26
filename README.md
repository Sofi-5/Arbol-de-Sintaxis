# Arbol-de-Sintaxis

==================================================
Generador de Árboles de Sintaxis en Python
==================================================

Autor: Laura Sofia Londoño Perez  
Fecha: Septiembre 2025  

Este programa analiza cadenas de entrada según una gramática libre de contexto
y genera:
1. El proceso de derivación paso a paso (por consola).
2. Un árbol de sintaxis visual en formato PNG.

Ideal para fines educativos en cursos de compiladores o lenguajes formales.

--------------------------------------------------
📌 REQUISITOS
--------------------------------------------------

- Python 3.6 o superior
- Librerías de Python:
    - anytree
    - graphviz

  Instálalas con:
      pip install anytree graphviz

- Graphviz instalado en tu sistema operativo:
    - Windows: https://graphviz.org/download/#windows
    - macOS (con Homebrew): brew install graphviz
    - Linux (Ubuntu/Debian): sudo apt-get install graphviz

--------------------------------------------------
📂 ESTRUCTURA DEL PROYECTO
--------------------------------------------------

├── arbol_sintaxis.py      ← Programa principal
├── gra.txt                ← Archivo de ejemplo de gramática
├── expresiones.txt        ← Archivo de ejemplo con cadenas de prueba
└── README.txt             ← Este archivo

--------------------------------------------------
📝 FORMATO DEL ARCHIVO DE GRAMÁTICA (gra.txt)
--------------------------------------------------

- Cada línea representa una regla:  <NO_TERMINAL> -> produccion1 | produccion2 ...
- Los símbolos se separan por espacios.
- Se permite el símbolo 'ε' para producciones vacías.
- La PRIMERA regla define el SÍMBOLO INICIAL.
- Líneas vacías o sin '->' se ignoran.

Ejemplo (gramática para expresiones aritméticas):

E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | num

> ⚠️ IMPORTANTE: La gramática debe ser compatible con un parser descendente
> recursivo (es decir, sin recursión izquierda y preferiblemente LL(1)).

--------------------------------------------------
🔤 TOKENIZACIÓN
--------------------------------------------------

El programa incluye un tokenizador básico que reconoce:
- Números enteros (ej. 123)
- Identificadores (ej. id, variable)
- Operadores y símbolos comunes: + - * / ( )

Esto significa que puedes escribir cadenas como:
    "10 + 2 * id"
y serán tokenizadas correctamente como:
    ['10', '+', '2', '*', 'id']

> ❗ No uses espacios dentro de números o identificadores.

--------------------------------------------------
🚀 CÓMO USAR
--------------------------------------------------

1. Edita o crea tu archivo de gramática (ej. `mi_gramatica.txt`).
2. Prepara tus cadenas de prueba (directamente o en un archivo).

Ejecuta desde la terminal:

Opción A: Probar cadenas directamente
    python arbol_sintaxis.py gra.txt "3+4*5" "(10+2)*3"

Opción B: Probar múltiples cadenas desde un archivo
    python arbol_sintaxis.py gra.txt expresiones.txt

Los árboles generados se guardarán como:
    arbol_sintaxis_1.png, arbol_sintaxis_2.png, ...

--------------------------------------------------
⚠️ LIMITACIONES CONOCIDAS
--------------------------------------------------

- No soporta gramáticas con recursión izquierda (ej. E -> E + T).
- No maneja ambigüedad: elige la primera producción que funcione.
- Las producciones con 'ε' deben usarse con cuidado para evitar bucles.
- El símbolo inicial se toma de la PRIMERA regla del archivo de gramática.

--------------------------------------------------
💡 CONSEJOS
--------------------------------------------------

- Si no se genera el PNG, verifica que Graphviz esté instalado en tu sistema.
- Usa gramáticas en Forma Normal de Greibach o transformadas para parsers LL(1).
- Para depuración, observa la derivación impresa en consola: muestra cada intento.

--------------------------------------------------
📄 LICENCIA
--------------------------------------------------

Este proyecto es de uso educativo. Puedes modificarlo y redistribuirlo
siempre que se mantenga el crédito al autor original.

==================================================
¡Gracias por usar el Generador de Árboles de Sintaxis!
==================================================
