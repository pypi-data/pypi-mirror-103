# secure-socket
a secured python socket using diffie hellman
how to use:
import secure_socket
s=secure_socket()
#server side
s.bind(addr)
s.listen()
s=s.accept()[0]
#client side
s.connect(addr)
#shared
s.setup_encryption()# if you want to make a new shared key using DH
s.set_key(int key)# if you want to set a pre-created key
c.encrypted_send(data)#to encrypt and send data
c.encrypted_recv(buffer size)#to recive and decrypt data
c.encrypted_recvall()#to recive and decrypt all available data
s.close()
