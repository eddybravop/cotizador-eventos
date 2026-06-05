@author: Eddy Gabriel Bravo


import streamlit as st
import datetime
import urllib.parse


# Configuración de la página (opcional, para que se vea más ancha)
st.set_page_config(page_title="Cotizador de Eventos", layout="centered",initial_sidebar_state="collapsed")

# Aquí insertas el logotipo de tu marca
st.image("logo1.png", width=300)

st.title("Cotizador de Eventos")
st.write("Hola. Te saludamos de Loly Eventos. Complete sus datos y seleccione los servicios requeridos para calcular el presupuesto estimado de su evento.")
st.divider()
# *****************************************************************************
# --- 1. Variables de entrada (Inputs del usuario) ---
st.subheader("1. Datos del Cliente")

nombre = st.text_input("**Nombre Completo o Empresa**")
contacto = st.text_input("**Número de Contacto**")
correo = st.text_input("**Correo Electrónico**")

# --- 2. Variables de entrada (Inputs del usuario) ---
st.subheader("2. Datos del Evento")
col1, col2 = st.columns(2) # Usamos columnas para organizar mejor el espacio
with col1:
    fecha = st.date_input("**Fecha del Evento**", min_value=datetime.date.today())
    tipo_evento = st.selectbox("**Tipo de Evento**", ["Matrimonio", "Cumpleaños", 
                                                      "Almuerzo/Cena Corporativa","Fiesta Privada","Otro"])
with col2:
    hora = st.time_input("**Hora del Evento**", value=datetime.time(12, 0))
    invitados = st.number_input("**Número de Invitados**", min_value=10, value=10, step=1)

st.divider()
# *****************************************************************************
# --- 3. Gastronomía y Hospitalidad ---
st.subheader("3. Gastronomía y Hospitalidad")

# Opción 1: Menú Principal
precios_menu = {
    "Menú Típico (Hornado + Bebida + Postre)": 12.03,
    "Menú Simple (Plato Fuerte + Bebida + Postre)": 15.28,
    "Menú Completo (Entrada + Plato Fuerte + Bebida + Postre)": 19.18,
    "Sin comida": 0.00
}
opcion_menu = st.selectbox("**Menú Principal:**", options=list(precios_menu.keys()))
total_menu = invitados * precios_menu[opcion_menu]

# Opción 2: Bebidas
precios_bebidas = {
    "Gaseosas ilimitadas": 3.50,
    "Barra libre básica (Cervezas)": 12.00,
    "Barra libre premium (Cerveza + Licor)": 35.00,
    "Estación de bebidas calientes (cortesía)": 0.00,
    "Ninguna": 0.00
}
opcion_bebida = st.selectbox("**Paquete de Bebidas (Bloque de 5 horas)**:", options=list(precios_bebidas.keys()))
total_bebidas = invitados * precios_bebidas[opcion_bebida]

# Opción 3: Torta y Bocaditos
opciones_postre = [
    "Torta Decorada", 
    "Mix de Bocaditos", 
    "Torta + Bocaditos", 
    "Ninguno"
]
opcion_postre = st.selectbox("**Torta y Bocaditos:**", options=opciones_postre)

# Lógica mixta (fijo vs por persona)
if opcion_postre == "Torta Decorada":
    total_postre = 1.50 * invitados
elif opcion_postre == "Mix de Bocaditos":
    total_postre = 25.00 * (invitados/20)
elif opcion_postre == "Torta + Bocaditos":
    total_postre = (25.00 * (invitados/20)) + (1.50 * invitados)
else:
    total_postre = 0.00

# Opción 4: Personal de Servicios
opcion_meseros = st.radio("**Personal de Servicios:**", ["No meseros", "Meseros ($30 c/u)"])
total_meseros = 0.00
if opcion_meseros == "Meseros ($30 c/u)":
    # Calcula sugerencia base: 1 mesero por cada 15 invitados
    meseros_sugeridos = max(1, invitados // 20)
    cant_meseros = st.number_input("Cantidad de meseros requeridos:", min_value=1, value=meseros_sugeridos, step=1)
    total_meseros = cant_meseros * 30.00

# Opción 5: Ambientación y Entretenimiento
st.write("**Ambientación y Entretenimiento (Puede seleccionar varias opciones):**")
precios_entretenimiento = {
    "DJ y Animación Estándar ($250)": 250.00,
    "Música en vivo (solista) ($60)": 60.00,
    "Banda en vivo (Setlist de varios estilos) ($250)": 250.00,
    "Show en vivo (hora loca) ($100)": 100.00,
    "Bartender profesional ($100)": 150.00
}

# st.multiselect para permitir múltiples opciones al mismo tiempo
opciones_ent = st.multiselect("Seleccione las opciones de entretenimiento:", options=list(precios_entretenimiento.keys()))

total_entretenimiento = 0.00
for op in opciones_ent:
    total_entretenimiento += precios_entretenimiento[op]


# Opción 6: Diseño, Visuales y Decoración
st.write("**Diseño, Visuales y Decoración (Puede seleccionar varias opciones):**")
precios_diseño = {
    "Diseño Tarjeta de Invitación ($20)": 20.00,
    "Cobertura Fotográfica (5 horas) ($75)": 75.00,
    "Decoración Paquete Básico ($50)": 50.00,
    "Decoración Paquete Premium ($100)": 100.00,
    "Centros de Mesa ($10)": 10.00 * (invitados/8)
}

# st.multiselect para permitir múltiples opciones al mismo tiempo
opciones_ent = st.multiselect("Seleccione las opciones de Diseño:", options=list(precios_diseño.keys()))

total_diseño = 0.00
for op in opciones_ent:
    total_diseño += precios_diseño[op]
# *****************************************************************************
# --- 4. Resumen y Total ---
st.divider()
st.subheader("4. Resumen de Cotización")

# Mostrar datos básicos si se ingresaron
if nombre:
    st.write(f"**Cliente:** {nombre} | **Evento:** {tipo_evento} para {invitados} invitados.")

# Suma general
total_general = total_menu + total_bebidas + total_postre + total_meseros + total_entretenimiento + total_diseño

# Mostramos el desglose en columnas para que sea fácil de leer
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.write(f"- Gastronomía: **${total_menu:,.2f}**")
    st.write(f"- Bebidas: **${total_bebidas:,.2f}**")
    st.write(f"- Torta/Bocaditos: **${total_postre:,.2f}**")
with col_res2:
    st.write(f"- Personal (Meseros): **${total_meseros:,.2f}**")
    st.write(f"- Entretenimiento: **${total_entretenimiento:,.2f}**")
    st.write(f"- Diseño: **${total_diseño:,.2f}**")
    
st.markdown(f"### **Total Estimado: ${total_general:,.2f}**")

# *******************************************************************************************************
# --- 5. Botones de Envío ---
st.divider()
st.subheader("¿Deseas reservar esta cotización?")

# Armamos el texto que te llegará por mensaje
mensaje_resumen = (
    f"Hola, soy {nombre}. Me interesa la cotización para mi evento ({tipo_evento}) "
    f"el día {fecha}.\n\n"
    f"👥 Invitados: {invitados}\n"
    f"💰 Total Estimado: ${total_general:,.2f}\n\n"
    f"Por favor, contáctame a este número o al correo {correo}."
)

# Codificamos el mensaje para que funcione en un enlace web
mensaje_codificado = urllib.parse.quote(mensaje_resumen)

# Configuramos el número de destino (Código de país + número sin el 0 inicial)
numero_whatsapp = "593999633383"
link_wa = f"https://wa.me/{numero_whatsapp}?text={mensaje_codificado}"

# Creamos el botón en la interfaz
st.link_button("📲 Enviar por WhatsApp", link_wa, type="primary", use_container_width=True)
