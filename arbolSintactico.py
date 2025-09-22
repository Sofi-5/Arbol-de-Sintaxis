"""
--------------------------------------------------------
PROGRAMA: Generador de Árboles de Sintaxis en Python
AUTOR:    Laura Sofia Londoño Perez
FECHA:    Septiembre 2025
--------------------------------------------------------
DESCRIPCIÓN:
Este programa lee una gramática libre de contexto desde un
archivo `gra.txt`, luego analiza una o varias cadenas de prueba
y genera:

1. El proceso de derivación paso a paso (por consola).
2. Un árbol de sintaxis para cada cadena en formato gráfico (PNG).

REQUISITOS:
- Python 3.x
- Librerías: anytree, graphviz
  Instalar con: pip install anytree graphviz
- Tener instalado Graphviz en el sistema (Windows/Linux/Mac).

USO:
python arbol_sintaxis.py gra.txt "3+4*5" "4*5+3"
python arbol_sintaxis.py gra.txt expresiones.txt   (si expresiones.txt contiene varias líneas)
--------------------------------------------------------
"""

import sys
from collections import defaultdict
from anytree import Node
from graphviz import Digraph
import os

# ---------- LECTOR DE GRAMÁTICA ----------
def leer_gramatica(archivo):
    """
    Lee el archivo de gramática y construye un diccionario
    donde la clave es el símbolo no terminal y el valor es
    una lista de producciones (cada producción es lista de símbolos).
    """
    gramatica = defaultdict(list)
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or "->" not in linea:
                continue
            izquierda, derecha = linea.split("->")
            izquierda = izquierda.strip()
            producciones = [prod.strip().split() for prod in derecha.split("|")]
            gramatica[izquierda].extend(producciones)
    return dict(gramatica)

# ---------- PARSER RECURSIVO ----------
def construir_arbol(gramatica, simbolo, tokens, pos=0, nivel=0):
    """
    Construye recursivamente un árbol de sintaxis para la cadena de tokens.
    Soporta producciones vacías usando el símbolo 'ε'.
    Devuelve:
    - nodo raíz del árbol (o None si falla)
    - nueva posición en la cadena después de consumir tokens
    - lista de pasos (strings) con el proceso de derivación
    """
    pasos = []
    if pos > len(tokens):
        return None, pos, pasos

    for produccion in gramatica.get(simbolo, []):
        nodo = Node(simbolo)
        actual_pos = pos
        exito = True
        pasos.append("  " * nivel + f"Intentando {simbolo} -> {' '.join(produccion)}")

        for s in produccion:
            if s == "ε":  # PRODUCCIÓN VACÍA
                pasos.append("  " * (nivel+1) + "✔ Producción vacía aceptada")
                continue

            if s in gramatica:  # No terminal
                hijo, actual_pos, pasos_hijo = construir_arbol(gramatica, s, tokens, actual_pos, nivel + 1)
                pasos.extend(pasos_hijo)
                if hijo:
                    hijo.parent = nodo
                else:
                    pasos.append("  " * (nivel+1) + f"❌ Falló en {s}")
                    exito = False
                    break
            else:  # Terminal
                if actual_pos < len(tokens) and tokens[actual_pos] == s:
                    Node(s, parent=nodo)
                    pasos.append("  " * (nivel+1) + f"✔ Coincide terminal '{s}' con '{tokens[actual_pos]}'")
                    actual_pos += 1
                else:
                    pasos.append("  " * (nivel+1) +
                                 f"✘ Terminal '{s}' no coincide (esperado '{s}', encontrado '{tokens[actual_pos] if actual_pos < len(tokens) else 'EOF'}')")
                    exito = False
                    break

        if exito:
            return nodo, actual_pos, pasos

    return None, pos, pasos

# ---------- GENERAR ÁRBOL GRÁFICO ----------
def dibujar_arbol(nodo, nombre_archivo):
    """
    Genera un archivo PNG con el árbol de sintaxis usando Graphviz.
    """
    dot = Digraph(comment="Árbol de Sintaxis")
    dot.attr('node', shape='circle')

    def agregar_nodo(nodo, parent=None):
        dot.node(str(id(nodo)), nodo.name)
        if parent:
            dot.edge(str(id(parent)), str(id(nodo)))
        for hijo in nodo.children:
            agregar_nodo(hijo, nodo)

    agregar_nodo(nodo)
    dot.render(nombre_archivo, format="png", cleanup=True)
    print(f"✅ Árbol generado: {nombre_archivo}.png")

# ---------- FUNCIÓN PRINCIPAL ----------
def analizar_cadenas(archivo_gramatica, cadenas):
    """
    Analiza cada cadena de prueba, imprime pasos y genera árbol.
    """
    gramatica = leer_gramatica(archivo_gramatica)
    print("\n=== GRAMÁTICA ===")
    for nt, reglas in gramatica.items():
        print(f"{nt} -> {' | '.join(' '.join(r) for r in reglas)}")

    for idx, cadena_prueba in enumerate(cadenas, 1):
        print("\n" + "="*50)
        print(f"ANÁLISIS #{idx}: {cadena_prueba}")
        print("="*50)

        tokens = list(cadena_prueba.replace(" ", ""))
        print("TOKENS:", tokens)

        arbol, pos_final, pasos = construir_arbol(gramatica, "E", tokens)

        print("\n=== PROCESO DE DERIVACIÓN ===")
        for p in pasos:
            print(p)

        if arbol and pos_final == len(tokens):
            print("\n✅ Cadena válida.")
            nombre_archivo = f"arbol_sintaxis_{idx}"
            dibujar_arbol(arbol, nombre_archivo)
        else:
            print("\n❌ La cadena no pertenece a la gramática.")

# ---------- MAIN ----------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python arbol_sintaxis.py gra.txt \"expr1\" \"expr2\" ...")
        print("O:   python arbol_sintaxis.py gra.txt archivo_cadenas.txt")
        sys.exit(1)

    archivo_gramatica = sys.argv[1]
    if os.path.isfile(sys.argv[2]):
        # Si el segundo argumento es un archivo, leer líneas
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            cadenas = [linea.strip() for linea in f if linea.strip()]
    else:
        # Si no es archivo, usar argumentos como cadenas directas
        cadenas = sys.argv[2:]

    analizar_cadenas(archivo_gramatica, cadenas)
