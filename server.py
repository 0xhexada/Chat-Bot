import socket
import time


class Server(object):
    __slots__ = ('HOST', 'PORT', 's', 'conn', 'addr', 'itsatime')
    '''
    https://habr.com/ru/articles/686220/

    Класс с использованием slots примерно на 25-30 % быстрее на операциях доступа к атрибутам
    *Также уменьшает размер файла
    '''

    def __init__ (self, HOST: str, PORT: int, s = None, 
                  conn: bool = None, itsatime = None) -> None:
        self.HOST = HOST
        self.PORT = PORT

    # Контекстный менеджер https://habr.com/ru/articles/739326/
    def __enter__ (self) -> True:
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.HOST = '127.0.0.1'
            self.PORT = 10000
            self.s.bind((self.HOST, self.PORT))
            print('[ Server Started ]')
            self.s.listen(1)
            self.conn, self.addr = self.s.accept()
            self.itsatime = time.strftime('%Y-%m-%d-%H.%M.%S', time.localtime())

        except Exception as e:
            self.unconnected(e)
            return False
        
        else:
            self.connected()
            return self

    def __exit__ (self, exc_type, exc_val, exc_tb) -> True:
        try:
            self.stopped()
            self.conn.close()
            return False

        except Exception as e:
            self.unconnected(e)
            return True

    def connected (self):
        print((f'Соединение прошло успешно: [{self.addr[0]}]=[{str(self.addr[1])}]=[{self.itsatime}] [+]'))
        self.conn.send(f'[{self.addr[0]}]=[{str(self.addr[1])}]=[{self.itsatime}] [+]'.encode())

    def unconnected (self, error):
        print(f'Соединение с клиентом не прошло успешно: [{self.itsatime}] [-]')
        self.conn.send(f'Соединение не прошло успешно [{self.itsatime}] [-]\n\n{error}'.encode())

    def stopped (self):
        print(f'Робота сервера остановлена: [{self.itsatime}] [-]')
        self.conn.send(f'Робота сервера остановлена: [{self.itsatime}] [-]'.encode())
    
    def say_hello (self):
        self.conn.send('Hi'.encode())

    def say_status (self):
        status = '\n\n'

        status += f'host: {self.HOST}\n'
        status += f'port: {self.PORT}\n'

        if self.s.type == socket.SOCK_STREAM: # Если сервер соединен к клиенту через TCP, то ...
            status += 'protocol: TCP\n'

        if self.s.type == socket.SOCK_DGRAM: # Если сервер соединен к клиенту через UDP, то ...
            status += 'protocol: UDP\n'
        
        if self.s.family == socket.AF_INET: # Если адресс сервера IPv4 структуры, то ...
            status += 'address: IPv4'

        if self.s.family == socket.AF_INET6: # Если адресс сервер IPv6 структуры, то ...
            status += 'address: IPv4'

        self.conn.send(status.encode())


if __name__ == '__main__':
    with Server('127.0.0.1', 10000) as srv:
        while True:
            data = srv.conn.recv(1024)
            if not data:
                break

            message = data.decode().lower()
            print(f"Сообщение от клиента: {message}")

            # Можно сделать другие команды, я ничего другого не придумал
            if message == 'hello':
                srv.say_hello()

            elif message == 'status':
                srv.say_status()

            else:
                srv.conn.send(f'Неизвесная команда {message}'.encode())
