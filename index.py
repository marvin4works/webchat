import random
import string
import uuid
from datetime import datetime

import tornado
from tornado import websocket, web, ioloop

import settings as sts
from log import logger
from settings import N, FMT

cl = []
AUTHORIZED_USER = {}  # ws_key: userid
WS_USER_MAP = {}  # ws_object: ws_key


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        # parsed_origin = urllib.parse.urlparse(origin)
        # return parsed_origin.netloc.endswith(".mydomain.com")
        return True

    def open(self):
        logger.debug('ws opened:' + repr(self))
        # print self.request.headers

    def on_close(self):
        logger.debug('ws closed:' + repr(self))
        if self in cl:
            cl.remove(self)  # TODO rm the USER? no ,do it in logout

    def handle_message(self, msg):
        """
        msg example
                {
                    "id": 'id',
                    "time": "2015/11/20 13:47",
                    "msg": "text msg",
                    "name": "abe",
                    "self": true
                }
        """

        logger.debug('server received msg %s' % msg)
        # print self.request.headers

        user_id = AUTHORIZED_USER[WS_USER_MAP[self]]
        d = datetime.now()
        ds = d.strftime(FMT)

        msg = {
            'msg': msg,
            "time": ds,
            'name': user_id,
        }
        for c in cl:
            c.write_message(msg)

    def on_message(self, msg):
        """
        第一次是握手，交换ws_key
        建立连接后  用handle_message处理后续的正常消息
        """
        logger.debug('on message: %s' % msg)
        logger.debug('AUTHORIZED_USER %s:' % AUTHORIZED_USER)
        if msg in AUTHORIZED_USER:
            self.on_message = self.handle_message

            WS_USER_MAP[self] = msg  # msg is ws_key
            cl.append(self)
        else:
            logger.debug('key error,closing the websocket')
            self.close()


# class AuthenticatedWebsocketHandler(tornado.websocket.WebSocketHandler):
#     '''Only allows a request to open a websocket for a valid current user.
#        This class assumes that the get_current_user() method is defined
#        to check for a valid session id. (see Tornado docs).
#     '''
#     def _execute(self, *args, **kwds):
#         if not self.current_user:
#             logging.warn('Unauthorized attempt by {} to open websocket.'
#                     .format(self.request.remote_ip))

#             self.stream.write(tornado.escape.utf8(
#                 'HTTP/1.1 401 Unauthorized\r\n\r\n'
#                 'Not authenticated.'))

#             self.stream.close()
#             return

#         super(AuthenticatedWebsocketHandler, self)._execute(*args, **kwds)


class BaseHandler(tornado.web.RequestHandler):
    """
    all that involved self.current_user
    """
    def get_current_user(self):
        return self.get_secure_cookie("user")  # override this method

        
class MainHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        logger.debug('Main page user get %s' % name)
        # self.write("Hello, " + name)
        ws_key = self.get_secure_cookie("user").decode()
        user = ws_key[:8]  # maybe modify here

        AUTHORIZED_USER[ws_key] = user  # must do it in this page ,
        # not login page, because login may be skipped
        
        self.render('index.html', ws_key=ws_key, user_id=user)


class LoginHandler(BaseHandler):
    """
    setting "login_url": "/login",
    route (r"/login", LoginHandler),
    """
    def get(self):
        salt = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(N))
        user = ''.join([salt, uuid.uuid1().hex])
        logger.debug('Login new user %s' % user)
        self.set_secure_cookie("user", user, expires_days=None)
        self.redirect("/")  # may be redirect to next is better
       
    def post(self):
        return self.get()


app = web.Application([
    (r'/', MainHandler),
    (r'/ws', SocketHandler),
    (r"/login", LoginHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r"/(.*)$", tornado.web.StaticFileHandler, dict(path=sts.settings['static_path'])),  # raise 404  without this
], **sts.settings)


if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
