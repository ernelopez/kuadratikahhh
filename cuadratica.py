
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Función cuadrática", layout="centered")

st.title("Explorador de funciones cuadráticas")

st.write("Ingresá los coeficientes de la función:")

# Parámetros
a = st.number_input("Coeficiente a", value=1.0, step=0.5)
b = st.number_input("Coeficiente b", value=2.0, step=0.5)
c = st.number_input("Coeficiente c", value=3.0, step=0.5)

st.divider()

st.subheader("Intervalo de graficación")

col1, col2 = st.columns(2)

with col1:
    ini = st.number_input("Extremo inicial", value=-10.0)

with col2:
    fin = st.number_input("Extremo final", value=10.0)

N = st.slider("Cantidad de puntos", min_value=50, max_value=1000, value=300, step=50)

# Opciones del gráfico
st.subheader("Opciones")

mostrar_raices = st.checkbox("Mostrar raíces", value=True)
mostrar_vertice = st.checkbox("Mostrar vértice", value=True)
mostrar_ejes = st.checkbox("Mostrar ejes coordenados", value=True)

# Funciones
def cuadratica(a, b, c, x):
    return a*x**2 + b*x + c

def raices(a, b, c):
    d = b**2 - 4*a*c

    if d < 0:
        return None
    elif d == 0:
        return [-b/(2*a)]
    else:
        return [
            (-b + np.sqrt(d))/(2*a),
            (-b - np.sqrt(d))/(2*a)
        ]

def vertice(a, b, c):
    xv = -b/(2*a)
    yv = cuadratica(a, b, c, xv)
    return xv, yv

# Validaciones y resultados
if a == 0:
    st.error("El coeficiente a debe ser distinto de cero.")
elif ini >= fin:
    st.error("El extremo inicial debe ser menor que el extremo final.")
else:

    d = b**2 - 4*a*c
    xv, yv = vertice(a, b, c)

    # Expresión
    st.subheader("Función")

    st.latex(
        rf"f(x) = {a}x^2 {'+' if b >= 0 else '-'} {abs(b)}x "
        rf"{'+' if c >= 0 else '-'} {abs(c)}"
    )

    # Resultados
    st.subheader("Características")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Discriminante", f"{d:.4f}")
        st.metric("Vértice", f"({xv:.4f}, {yv:.4f})")

    with col2:
        st.metric("Eje de simetría", f"x = {xv:.4f}")
        st.metric("Concavidad", "Hacia arriba" if a > 0 else "Hacia abajo")

    if d > 0:
        r = raices(a, b, c)
        st.write(f"**Raíces:** {r[0]:.4f} y {r[1]:.4f}")
    elif d == 0:
        r = raices(a, b, c)
        st.write(f"**Raíz doble:** {r[0]:.4f}")
    else:
        st.write("**No tiene raíces reales.**")

    # Gráfico
    st.subheader("Gráfico")

    x = np.linspace(ini, fin, N)
    y = cuadratica(a, b, c, x)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(x, y, label="f(x)", linewidth=2)

    if mostrar_raices and d >= 0:
        r = raices(a, b, c)
        ax.scatter(r, [0]*len(r), color="red", s=60,
                   zorder=3, label="Raíces")

    if mostrar_vertice:
        ax.scatter(xv, yv, color="green", s=70,
                   zorder=3, label="Vértice")

    if mostrar_ejes:
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)

    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

    st.pyplot(fig)
    plt.close(fig)
