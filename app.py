#setup tornado framework
import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.log
import tornado.auth
from dotenv import load_dotenv
load_dotenv('.env')

#set up api request function
import urllib.parse
import requests
import json

#templating engine
from jinja2 import \
    Environment, PackageLoader, select_autoescape

PORT = int(os.environ.get('PORT', '8888'))

ENV = Environment(
    loader=PackageLoader('myapp', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class TemplateHandler(BaseHandler):
    def render_template(self, tpl, context):
        template = ENV.get_template(tpl)
        self.write(template.render(**context))

class MainHandler(TemplateHandler):
    def get(self):
        self.set_header('Cache-Control','no-store, no-cache, must-revalidate, max-age=0')
        p = 'hello'
        self.render_template("index.html",{"p": p})
        
class QueryHandler(TemplateHandler):
    def post(self):
        #outputitems of outputitems much be in strings
        outputitems = "source,sample_id"
        params = {
            'author': 'peter',
            'searchtype' : 'rowdata',
            'outputtype' :'json', #html, csv, staticmap, jsonp, xml
            'showcolumnnames' : 'yes',
            'outputitems' : outputitems
        }
        # POSSIBLE OUTPUTITEMS
        # sample_id
        # source
        # url
        # title
        # journal
        # author
        # longitude
        # latitude
        # method
        # material
        # type
        # composition
        # rock_name
        try:
            response = requests.get('http://ecp.iedadata.org/restsearchservice', params=params)
            print(response)
            print(response.url)
            # print ('Response:')
            parsed = json.loads(response.text)
            print(parsed)
            print (json.dumps(parsed, sort_keys=True, indent=2))

        except Exception as e:
            print('Error:')
            print(e)

class make_app(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/", MainHandler),
        (
            r"/static/(.*)",
            tornado.web.StaticFileHandler,
            {'path': 'static'}
        ),
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)


if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    app.listen(PORT, print('Server started on localhost:' + str(PORT)))
    tornado.ioloop.IOLoop.current().start()
