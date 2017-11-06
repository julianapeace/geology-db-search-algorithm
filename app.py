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

PORT = int(os.environ.get('PORT', '8080'))

ENV = Environment(
    loader=PackageLoader('myapp', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
    def render_template(self, tpl, context):
        template = ENV.get_template(tpl)
        self.write(template.render(**context))

class MainHandler(TemplateHandler):
    def get(self):
        self.set_header('Cache-Control','no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("index.html",{})

class QueryHandler(TemplateHandler):
    def post(self):
        url = 'http://ecp.iedadata.org/restsearchservice'

        author = self.get_body_argument("author")
        searchtype = self.get_body_argument("searchtype")
        output_type = self.get_body_argument("output_type")
        output_fields = self.get_body_arguments("output_fields")
        show_column_names = self.get_body_argument("show_column_names")
        outputitems = ",".join(output_fields)

        params = {
            'author': author,
            'searchtype' : searchtype,
            'outputtype' :output_type,
            'showcolumnnames' : show_column_names,
            'outputitems' : outputitems
        }
        try:
            response = requests.get(url, params=params)
            print(response)
            print(response.url)
            if output_type=='json':
                html = "false"
                parsed = json.loads(response.text)
                results = json.dumps(parsed, sort_keys=True, indent=2)
            elif output_type =="html":
                #get the count
                params_count={
                'author': author,
                'searchtype' : "count",
                'outputtype' :output_type,
                'showcolumnnames' : show_column_names,
                'outputitems' : outputitems
                }

                count_response = requests.get(url, params=params_count)
                count = count_response.text

                html = "true"
                results = response.text
            else:
                html = "false"
                count = ""
                results = response.text

            # print ('Response:')
            # print(results)
            self.render_template("response.html",{"html":html, "results":results, "count":count})

        except Exception as e:
            print('Error:')
            print(e)
            #http://ecp.iedadata.org/restsearchservice?author=smith&searchtype=rowdata&outputtype=html&showcolumnnames=yes&outputitems=sample_id,source,longitude,latitude
            self.redirect("/")


def make_app():
  return tornado.web.Application([
        (r"/", MainHandler),
        (r"/query", QueryHandler),
        (
            r"/static/(.*)",
            tornado.web.StaticFileHandler,
            {'path': 'static'}
        ),
        ], autoreload=True)


if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    app.listen(PORT, print('Server started on localhost:' + str(PORT)))
    tornado.ioloop.IOLoop.current().start()
