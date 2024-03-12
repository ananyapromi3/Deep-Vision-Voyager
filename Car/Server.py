import curses
import socket
import webbrowser
s = socket.socket()
host = '172.20.10.4'
port = 12760
s.bind((host, port))


def main(window):
    s.listen(5)
    while True:
        print("here")
        c, addr = s.accept()
        print('Got connection from ', addr)
        next_key = None
        while True:
            curses.halfdelay(1)
            if next_key is None:
                key = window.getch()
            else:
                key = next_key
                next_key = None
            if key != -1:
                curses.halfdelay(2)
                print(key)
                data = ''
                if key == 97:
                    data = 'left'
                if key == 100:
                    data = 'right'
                if key == 119:
                    data = 'forward'
                if key == 115:
                    data = 'reverse'
                if key == 259:
                    data = 'sup'
                if key == 260:
                    data = 'camlef'
                if key == 258:
                    data = 'sdown'
                if key == 261:
                    data = 'camrig'
                if key == 99:
                    data = 'movCam'
                c.send(data.encode())
                next_key = key
                first = False
                while next_key == key:
                    next_key = window.getch()
                    if not first:
                        next_key = key
                        first = True
                data = 'stop'
                c.send(data.encode())


curses.wrapper(main)
