import os
import sys
import pty
import subprocess
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.process

import pexpect

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        print 'check_origin:', self, origin
        return True
    
    def open(self):
        print 'open:', self
        io_loop = tornado.ioloop.IOLoop.instance()
        self.proc = pexpect.spawn(
            os.getenv('SHELL'),
            cwd=os.getenv('HOME'),
        )
        io_loop.add_handler(self.proc.child_fd, self._read_master, io_loop.READ)
    
    def _read_master(self, *args):
        print '_read_master:', self, args
        b = os.read(self.proc.child_fd, 1024)
        message = b.encode('utf-8')
        
        try:
            self.write_message(message)
        except Exception as e:
            print e
            self.close()
    
    def on_message(self, message):
        print 'on_message:', self, repr(message)
        message = message.replace('\r', '\n')
        message = message.decode('utf-8')
        self.proc.write(message)
    
    def on_close(self):
        print 'on_close:', self
        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.remove_handler(self.proc.child_fd)
        self.proc.close(force=True)

application = tornado.web.Application([
    (r'/', EchoWebSocket),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
