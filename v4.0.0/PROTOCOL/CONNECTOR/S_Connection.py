# v4.0.0 ✠
# S PROTOCOL COMPONENT




import socket
import ssl




class S_Connection:




    def __init__(self, Host, Port, Config):
    
        self.Host = Host
        self.Port = Port
        self.Config = Config
        
        self.SSL_Context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        
        self.SSL_Context.verify_mode = ssl.CERT_REQUIRED

        self.SSL_Context.minimum_version = ssl.TLSVersion.TLSv1_3
        self.SSL_Context.maximum_version = ssl.TLSVersion.TLSv1_3
        
        try:
            self.SSL_Context.load_verify_locations(self.Config["CA_Cert_Path"])
            self.SSL_Context.load_cert_chain(
                certfile=self.Config["Client_Cert_Path"], 
                keyfile=self.Config["Client_Key_Path"]
            )
            self.SSL_Context.check_hostname = False
            
        except Exception:
            pass




    def Execute(self, Request_Payload):

        Base_Socket = None
        Secure_Socket = None
        Response_Data = None

        try:
        
            Base_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Base_Socket.settimeout(10)

            Secure_Socket = self.SSL_Context.wrap_socket(
                Base_Socket, 
                server_hostname=self.Host
            )
            
            Secure_Socket.connect((self.Host, self.Port))
            
            Secure_Socket.sendall(Request_Payload.encode('utf-8'))
            
            Data_Buffer = b""
            
            while True:
            
                Chunk = Secure_Socket.recv(16384)
                
                if not Chunk:
                    break
                    
                Data_Buffer += Chunk
                
                if b"\n" in Data_Buffer:
                    break
            
            if Data_Buffer:
                Response_Data = Data_Buffer.decode('utf-8').strip()

        except Exception:
            pass
            
        finally:
        
            if Secure_Socket:
                try:
                    Secure_Socket.close()
                except Exception:
                    pass
            elif Base_Socket:
                try:
                    Base_Socket.close()
                except Exception:
                    pass
        
        return Response_Data
