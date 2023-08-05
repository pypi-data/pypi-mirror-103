# -*- coding: utf-8 -*-


class py-mailsender:
    def __init__(self, author , psswd , dear , subject , content ):

      
        import smtplib

        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        # Correo de acceso al servidor
        MY_ADDRESS = author  # author's email adress 

        PASSWORD = psswd   #The password
        
        # Configure email's server
        s = smtplib.SMTP(host='smtp.' +author[author.find("@") + 1 : ] , port=587) # server & port
        s.starttls() 
        s.login(MY_ADDRESS, PASSWORD) 

        # Create the message
        msg = MIMEMultipart()

        message = content #  The content of the email

        msg['From']=MY_ADDRESS
        msg['To']= dear # el destinatario
        msg['Subject']= subject #The subject of the email

        # Append the text into the message
        msg.attach(MIMEText(message, 'plain'))

        # Enviar el mensaje
        s.send_message(msg)
        del msg

        # Close SMTP session
        s.quit()