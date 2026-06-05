import streamlit as st
import datetime
import urllib.parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración de la página
st.set_page_config(page_title="Cotizador de Eventos", layout="centered", initial_sidebar_state="collapsed")

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
col1, col2 = st.columns(2)
with col1:
    fecha = st.date_input("**Fecha del Evento**", min_value=datetime.date.today())
    tipo_evento = st.selectbox("**Tipo de Evento**", ["Matrimonio", "Cumpleaños", "Almuerzo/Cena Corporativa", "Fiesta Privada", "Otro"])
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
opciones_postre_list = [
    "Torta Decorada", 
    "Mix de Bocaditos", 
    "Torta + Bocaditos", 
    "Ninguno"
]
opcion_postre = st.selectbox("**Torta y Bocaditos:**", options=opciones_postre_list)

# Lógica mixta (fijo vs por persona)
if opcion_postre == "Torta Decorada":
    total_postre = 1.50 * invitados
elif opcion_postre == "Mix de Bocaditos":
    total_postre = 25.00 * (invitados / 20)
elif opcion_postre == "Torta + Bocaditos":
    total_postre = (25.00 * (invitados / 20)) + (1.50 * invitados)
else:
    total_postre = 0.00

# Opción 4: Personal de Servicios
opcion_meseros = st.radio("**Personal de Servicios:**", ["No meseros", "Meseros ($30 c/u)"])
total_meseros = 0.00
cant_meseros = 0
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
precios_diseno = {
    "Diseño Tarjeta de Invitación ($20)": 20.00,
    "Cobertura Fotográfica (5 horas) ($75)": 75.00,
    "Decoración Paquete Básico ($50)": 50.00,
    "Decoración Paquete Premium ($100)": 100.00,
    "Centros de Mesa ($10)": 10.00 * (invitados / 8)
}

# st.multiselect usando la variable corregida (opciones_dis)
opciones_dis = st.multiselect("Seleccione las opciones de Diseño:", options=list(precios_diseno.keys()))

total_diseno = 0.00
for op in opciones_dis:
    total_diseno += precios_diseno[op]

# *****************************************************************************
# --- 4. Resumen y Total ---
st.divider()
st.subheader("4. Resumen de Cotización")

# Mostrar datos básicos si se ingresaron
if nombre:
    st.write(f"**Cliente:** {nombre} | **Evento:** {tipo_evento} para {invitados} invitados.")

# Suma general
total_general = total_menu + total_bebidas + total_postre + total_meseros + total_entretenimiento + total_diseno

# Mostramos el desglose en columnas para que sea fácil de leer
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.write(f"- Gastronomía: **${total_menu:,.2f}**")
    st.write(f"- Bebidas: **${total_bebidas:,.2f}**")
    st.write(f"- Torta/Bocaditos: **${total_postre:,.2f}**")
with col_res2:
    st.write(f"- Personal (Meseros): **${total_meseros:,.2f}**")
    st.write(f"- Entretenimiento: **${total_entretenimiento:,.2f}**")
    st.write(f"- Diseño: **${total_diseno:,.2f}**")
    
st.markdown(f"### **Total Estimado: ${total_general:,.2f}**")

# *******************************************************************************************************
# --- 5. Reserva Rápida por WhatsApp (Tu código original) ---
st.divider()
st.subheader("5. Reserva por WhatsApp")

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
st.link_button("📲 Enviar Mensaje a WhatsApp", link_wa, type="secondary", use_container_width=True)

# *******************************************************************************************************
# *******************************************************************************************************
# --- 6. Envío de Cotización Detallada por Correo ---
st.subheader("6. Enviar Detalle Completo por Correo")
st.write("Recibe el desglose exacto de los servicios seleccionados directamente en tu correo electrónico.")

# Botón para accionar el envío por correo
if st.button("✉️ Enviar Cotización por Correo", type="primary", use_container_width=True):
    # 1. Validación inmediata de campos en la interfaz
    if not nombre or not correo:
        st.warning("⚠️ Por favor, ingresa el Nombre y Correo Electrónico en la Sección 1 antes de solicitar el envío.")
    else:
        # El spinner asegura que el usuario vea actividad visual en pantalla
        with st.spinner("🔄 Conectando con el servidor de correo..."):
            try:
                # Verificar que existan las credenciales cargadas
                if "smtp_server" not in st.secrets:
                    st.error("❌ Configuración incompleta: No se detectaron las credenciales en los Secrets de Streamlit.")
                else:
                    smtp_config = st.secrets["smtp_server"]
                    
                    # Configuración del encabezado del correo
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = f"Nueva Cotización Loly Eventos - {nombre}"
                    msg['From'] = smtp_config["user"]
                    msg['To'] = smtp_config["destination"]
                    
                    # Formatear las selecciones de listas múltiples para el cuerpo de texto
                    ent_texto = ", ".join(opciones_ent) if opciones_ent else "Ninguna opción seleccionada"
                    dis_texto = ", ".join(opciones_dis) if opciones_dis else "Ninguna opción seleccionada"
                    meseros_texto = f"{cant_meseros} mesero(s)" if cant_meseros > 0 else "Sin meseros"
                    
                    # Diseño del correo en HTML estructurado
                    html_content = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; padding: 20px; border-radius: 8px;">
                            <h2 style="color: #2C3E50; border-bottom: 2px solid #ECF0F1; padding-bottom: 10px;">Nueva Cotización: Loly Eventos</h2>
                            
                            <h3>Datos del Cliente</h3>
                            <p><strong>Nombre:</strong> {nombre}<br>
                            <strong>Teléfono:</strong> {contacto if contacto else 'No provisto'}<br>
                            <strong>Correo:</strong> {correo}</p>
                            
                            <h3>Detalles del Evento</h3>
                            <p><strong>Tipo:</strong> {tipo_evento}<br>
                            <strong>Fecha y Hora:</strong> {fecha} a las {hora}<br>
                            <strong>Invitados:</strong> {invitados}</p>
                            
                            <h3>Desglose de Servicios Seleccionados</h3>
                            <ul>
                                <li><strong>Gastronomía:</strong> {opcion_menu} (${total_menu:,.2f})</li>
                                <li><strong>Bebidas:</strong> {opcion_bebida} (${total_bebidas:,.2f})</li>
                                <li><strong>Postre/Bocaditos:</strong> {opcion_postre} (${total_postre:,.2f})</li>
                                <li><strong>Personal:</strong> {meseros_texto} (${total_meseros:,.2f})</li>
                                <li><strong>Entretenimiento:</strong> {ent_texto} (${total_entretenimiento:,.2f})</li>
                                <li><strong>Diseño y Decoración:</strong> {dis_texto} (${total_diseno:,.2f})</li>
                            </ul>
                            
                            <div style="background-color: #EAEDED; padding: 15px; border-radius: 6px; text-align: right; font-size: 18px;">
                                <strong>TOTAL ESTIMADO: <span style="color: #27AE60;">${total_general:,.2f}</span></strong>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    msg.attach(MIMEText(html_content, 'html'))
                    
                    # Conexión usando Puerto 587 (TLS) y un parámetro de timeout de 15 segundos para evitar congelamientos
                    with smtplib.SMTP(smtp_config["server"], 587, timeout=15) as server:
                        server.starttls()  # Inicializa el cifrado seguro obligatorio
                        server.login(smtp_config["user"], smtp_config["password"])
                        server.sendmail(smtp_config["user"], smtp_config["destination"], msg.as_string())
                    
                    st.success("¡El desglose detallado ha sido enviado con éxito por correo!")
                    
            except Exception as e:
                # Captura el error exacto en pantalla si la conexión falla o expira el tiempo
                st.error(f"❌ Error al procesar el envío: {e}")
                st.info("💡 Consejo de conexión: Asegúrate de que tu archivo de configuración tenga asignado el puerto 587 y que la contraseña sea la clave de aplicación de 16 letras.")
