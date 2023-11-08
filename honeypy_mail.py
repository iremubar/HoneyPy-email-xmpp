# Autora: Irene Munoz Barquero


import sys
import hashlib
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from twisted.python import log

# prevent creation of compiled bytecode files
sys.dont_write_bytecode = True

def process(config, section, parts, time_parts):
        # TCP
        #	parts[0]: date
        #	parts[1]: time_parts
        #	parts[2]: plugin
        #	parts[3]: session
        #	parts[4]: protocol
        #	parts[5]: event
        #	parts[6]: local_host
        #	parts[7]: local_port
        #	parts[8]: service
        #	parts[9]: remote_host
        #	parts[10]: remote_port
        #	parts[11]: data
        # UDP
        #	parts[0]: date
        #	parts[1]: time_parts
        #	parts[2]: plugin string part
        #	parts[3]: plugin string part
        #	parts[4]: session
        #	parts[5]: protocol
        #	parts[6]: event
        #	parts[7]: local_host
        #	parts[8]: local_port
        #	parts[9]: service
        #	parts[10]: remote_host
        #	parts[11]: remote_port
        #	parts[12]: data
  
    # Se divide el mensaje recibido siguiendo la estructura superior.
    # Posteriormente se llama al metodo de send_email para enviar el correo con la informacion del logger
    
    if parts[4] == 'TCP':
        if len(parts) == 11:
            parts.append('')  # no data for CONNECT events
    
        send_email(config, section, parts[0], parts[1], parts[5], parts[8], parts[9], parts[10], parts[11])
    else:
        # UDP splits differently (see comment section above)
        if len(parts) == 12:
            parts.append('')  # no data sent
    
        send_email(config, section, parts[0], parts[1], parts[5], parts[8], parts[9], parts[10], parts[11])        
        
def send_email(config, section, date, time, event, service, remote_host, remote_port, data):
    
    # Se definen los parametros necesarios para el envio del email
    smtp_server = 'smtp.gmail.com'
    smtp_port = '587'
    smtp_username = 'honeypysender@gmail.com'
    smtp_password = 'xgyc hice mtyl xymo'
    from_address = 'honeypysender@gmail.com'
    to_address = 'honeypyreceiver@gmail.com'
    subject = 'HoneyPy Alert' + str(service)

    # Se construye el mensaje del email
    
    content = 'Posible ataque el dia ' + date + ' a las ' + time + ' al servicio ' + service + ' desde ' + remote_host + ':' + remote_port + '. Datos recibidos: ' + data.decode('hex')      
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(smtp_username, smtp_password)
        server.sendmail(from_address, [to_address], msg.as_string())
        server.quit()
        log.msg('Email sent to %s for event %s' % (to_address, event))
    except Exception as e:
        log.msg('Error sending email: %s' % str(e))

