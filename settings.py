import os
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "webui"),
    "template_path": os.path.join(os.path.dirname(__file__), "webui"),

    "cookie_secret": "61oETzKXQertwerAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
     "xsrf_cookies": True,
}
N = 20  # len of salt
FMT = '%Y-%m-%d %H:%M:%S'
