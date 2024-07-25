import socket


class Client(object):
    __slots__ = ('HOST', 'PORT', 'c')

    def __init__ (self, HOST: str, PORT: int, c = None):
        self.HOST = HOST
        self.PORT = PORT

    def __enter__ (self):
        try:
            self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.HOST = '127.0.0.1'
            self.PORT = 10000
            self.c.connect((self.HOST, self.PORT))

        except Exception as e:
            return False
        
        else:
            return self

    def __exit__ (self, exc_type, exc_val, exc_tb):
        try:
            self.c.close()
        
        except Exception as e:
            return True
        
        else:
            return False


if __name__ == '__main__':
    with Client('127.0.0.1', 10000) as cln:
        while True:
            data = cln.c.recv(1024)
            if not data:
                break
            
            message = data.decode()
            print(f"Сообщение от сервера: {message}")

            inpt = input("> ")
            cln.c.sendall(inpt.encode())
