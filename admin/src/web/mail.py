from flask_mail import Mail, Message

mail = Mail()

def init_app(app):
    """
        Inicializa la configuracion de mail
    """
    mail.init_app(app)


def send_email(to, subject, template):
    """
        Envia un correo electronico
        
        args: \n
            subject -> asunto del correo \n
            to -> destinatario del correo \n
            template -> mensaje del correo \n
    """
    
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=mail.default_sender
    )
    mail.send(msg)