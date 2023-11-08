# Autora: Irene Munoz Barquero

# -*- coding: utf-8 -*-
from twisted.internet import reactor, protocol
from twisted.words.xish import domish
from twisted.python import log
import uuid
import base64

class XMPP(protocol.Protocol):
    session = None
    auth_step = 0 # 0: esperando usuario, 1: esperando contraseña, 2: esperando mensaje
    
    def connectionMade(self):
        self.connect()
        
    def connect(self):
        self.local_host = self.transport.getHost()
        self.remote_host = self.transport.getPeer()
        self.session = uuid.uuid1()
        log.msg('%s %s CONNECT %s %s %s %s %s' % (self.session, self.remote_host.type, self.local_host.host, self.local_host.port, self.factory.name, self.remote_host.host, self.remote_host.port))

        # Se inicia la conexion pidiendo que se introduzca un usuario
        self.tx("Please enter your username:")
        
    def connectionLost(self, reason):
        log.msg('{} DISCONNECTED {}'.format(self.session, self.transport.getPeer()))

    def dataReceived(self, data):
        self.rx(data)
        
        
        if self.auth_step == 0:  # Se espera a que el usuario se haya introducido
            self.username = data.strip()
            self.auth_step += 1
            self.tx("Please enter your password:")
        elif self.auth_step == 1:  # Se espera a la password
            self.password = data.strip()
            self.auth_step += 1
            log.msg("Received username: %s " % (self.username))
            log.msg("Received password: %s " % (self.password))
            
            
            # Esto acepta cualquier tipo de password que se le introduzca
            response = domish.Element(('urn:ietf:params:xml:ns:xmpp-sasl', 'success'))
            self.tx(response.toXml().encode('utf-8'))

            # Aqui se solicita que el cliente introduzca un mensaje
            self.tx("<message xmlns='jabber:client' type='chat'><body>Please send a message.</body></message>")
        elif self.auth_step == 2:  # Esperando a recibir el mensaje del cliente
            self.message = data.strip()
            log.msg("Received message: %s" % self.message)
            self.transport.loseConnection()  # Al introducir el mensaje, se cierra la conexion
     
    def rx(self, data):
        log.msg('%s %s RX %s %s %s %s %s %s' % (self.session, self.remote_host.type, self.local_host.host, self.local_host.port, self.factory.name, self.remote_host.host, self.remote_host.port, data.encode("hex")))
    
    def tx(self, data):
        log.msg('%s %s TX %s %s %s %s %s %s' % (self.session, self.remote_host.type, self.local_host.host, self.local_host.port, self.factory.name, self.remote_host.host, self.remote_host.port, data.encode("hex")))
        self.transport.write(data)

class pluginFactory(protocol.Factory):
    protocol = XMPP  # Set protocol to custom protocol class name
    
    def __init__(self, name=None):
        self.name = name or 'HoneyPy'
