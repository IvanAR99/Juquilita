import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Comanda App", page_icon="🌮")
st.title("🍽️ Registro de Órdenes - Juquilita")

# 2. DEFINIR EL MENÚ (Diccionario: Platillo -> Precio)
# ¡Aquí puedes editar tus platillos reales!
menu = {
    "Empanadas": 35,
    "Tostadas": 35,
    "Quesadillas pescado": 10,
    "Quesadillas camarón": 15,
    "Mojarra":80,
    "Filete":25,
    "Refrescos":25,
    "Cerveza": 40
}

# Archivo donde se guardarán los datos
ARCHIVO_VENTAS = 'ventas_historicas.csv'

# 3. INICIALIZAR ESTADO (Para mantener la orden actual en memoria)
if 'orden_actual' not in st.session_state:
    st.session_state.orden_actual = []

# --- SECCIÓN A: AGREGAR PLATILLOS ---
st.header("1. Nueva Orden")

# Usamos columnas para que se vea más ordenado
col1, col2 = st.columns(2)

with col1:
    platillo = st.selectbox("Selecciona platillo", list(menu.keys()))
    # Muestra el precio inmediatamente al seleccionar
    precio_actual = menu[platillo]
    st.info(f"💰 Precio: ${precio_actual}")

with col2:
    cantidad = st.number_input("Cantidad", min_value=1, value=1)

# Botón para agregar
if st.button("Agregar a la Orden"):
    # Calculamos el total de este ítem
    total_item = precio_actual * cantidad
    
    item = {
        "Platillo": platillo,
        "Precio": precio_actual,
        "Cantidad": cantidad,
        "Total": total_item
    }
    st.session_state.orden_actual.append(item)
    st.success(f"Agregado: {cantidad} x {platillo} (${total_item})")

# --- SECCIÓN B: VER ORDEN ACTUAL Y GUARDAR ---
if len(st.session_state.orden_actual) > 0:
    st.divider()
    st.subheader("Resumen de Orden Actual")
    
    # Convertimos la lista a DataFrame para mostrarla bonita
    df_orden = pd.DataFrame(st.session_state.orden_actual)
    st.table(df_orden)
    
    total_pagar = df_orden['Total'].sum()
    st.metric(label="TOTAL A COBRAR", value=f"${total_pagar}")

    # Botón para cerrar la venta
    if st.button("✅ Finalizar y Guardar Orden", type="primary"):
        fecha_hora = datetime.now()
        folio = fecha_hora.strftime("%Y%m%d%H%M%S") # Folio basado en fecha/hora
        
        # Agregamos folio y fecha a cada ítem
        df_orden['Folio'] = folio
        df_orden['Fecha'] = fecha_hora
        
        # Guardar en CSV (Append mode)
        header = not os.path.exists(ARCHIVO_VENTAS) # Solo poner encabezados si el archivo no existe
        df_orden.to_csv(ARCHIVO_VENTAS, mode='a', header=header, index=False)
        
        st.success(f"Orden {folio} guardada exitosamente.")
        
        # Limpiar la orden actual
        st.session_state.orden_actual = []
        st.rerun()

# --- SECCIÓN C: VISTA RÁPIDA DE DATOS (Para ti, el analista) ---
st.divider()
with st.expander("📊 Ver Historial de Ventas (Admin)"):
    if os.path.exists(ARCHIVO_VENTAS):
        df_hist = pd.read_csv(ARCHIVO_VENTAS)
        st.dataframe(df_hist)
        st.write(f"Ventas Totales Históricas: ${df_hist['Total'].sum()}")
    else:
        st.info("Aún no hay ventas registradas.")
