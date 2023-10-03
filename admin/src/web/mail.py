from flask import render_template_string
from flask_mail import Mail, Message

mail = Mail()

def init_app(app):
    """
        Inicializa la configuracion de mail
    """
    mail.init_app(app)

def send_mail(subject, recipients, body, sender='CIDEPINT cidepintgrupo10@gmail.com'):
    """
        Envia un correo electronico
        
            : subject: asunto del correo
            : recipients: destinatario del correo
            : body: mensaje del correo
            : sender: remitente del correo (opcional)
    """
    
    msg = Message(subject=subject, sender=sender, recipients=[recipients])
    msg.html = render_template_string(body)
    mail.send(msg);
    