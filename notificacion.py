import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def enviar_correo(destinatario, asunto, cuerpo, remitente="carteraproyectois@gmail.com", contraseña="ieir jzue jaif alfl"):
    # Configura los detalles del servidor SMTP de Gmail
    smtp_server = "smtp.gmail.com"
    puerto = 587

    # Crea el mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    # Añade el cuerpo del mensaje
    mensaje.attach(MIMEText(cuerpo, "plain"))

    try:
        # Crea una conexión segura al servidor SMTP
        with smtplib.SMTP(smtp_server, puerto) as servidor:
            servidor.starttls()

            # Inicia sesión en la cuenta
            servidor.login(remitente, contraseña)

            # Envía el correo
            texto = mensaje.as_string()
            servidor.sendmail(remitente, destinatario, texto)

        #Se indica que se mando la notificación
        st.write("Se envío la notificación al jefe")
        print("Correo enviado con éxito")
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False

def obtener_username():
    # Verificamos si el usuario ha iniciado sesión
    if 'username' in st.session_state:
        return st.session_state['username']
    else:
        return "No hay usuario logueado"


def enviar(nuevo_nombre):
    username = obtener_username()
    destinatario = "Prietojorge905@gmail.com"
    asunto = "Notificación de informe"
    cuerpo = (nuevo_nombre + " Fue realizado por: " + username)

    enviar_correo(destinatario, asunto, cuerpo)