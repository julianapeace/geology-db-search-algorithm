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
import csv
from datetime import *

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
class testHandler(TemplateHandler):
    def post(self):
        url = 'http://ecp.iedadata.org/restsearchservice'

        author = self.get_body_argument("author") or None
        title = self.get_body_argument("title") or None
        journal = self.get_body_argument("journal") or None
        doi = self.get_body_argument("doi") or None
        searchtype = self.get_body_argument("searchtype") or None
        outputtype = self.get_body_argument("output_type") or None
        output_fields = self.get_body_arguments("output_fields")
        outputitems = ",".join(output_fields)
        showcolumnnames = self.get_body_argument("show_column_names")
        minpubyear = self.get_body_argument("minpubyear") or None
        maxpubyear = self.get_body_argument("maxpubyear") or None
        exactpubyear = self.get_body_argument("exactpubyear") or None
        sampleid = self.get_body_argument("sample_id") or None
        exactage = self.get_body_argument("exactage") or None
        minage = self.get_body_argument("minage") or None
        maxage = self.get_body_argument("maxage") or None
        geologicalage = self.get_body_argument("geologicalage") or None
        material = self.get_body_argument("material") or None

        arguments = {
            "author":author,
            "title": title,
            "journal": journal,
            "doi": doi,
            "searchtype": searchtype,
            "outputtype": outputtype,
            "outputitems": outputitems,
            "showcolumnnames":showcolumnnames,
            "minpubyear":minpubyear,
            "maxpubyear":maxpubyear,
            "exactpubyear":exactpubyear,
            "sampleid":sampleid,
            "exactage":exactage,
            "minage":minage,
            "maxage":maxage,
            "geologicalage":geologicalage,
            "material":material
        }
        params = {}
        for key, value in arguments.items():
            if value != None:
                params[key] = value
        print(params)
        print(author, title, journal, doi, searchtype, outputtype, outputitems, showcolumnnames, minpubyear, maxpubyear, exactpubyear, sampleid, exactage, minage, maxage, geologicalage, material)

        try:
            response = requests.get(url, params=params)
            print(response)
            print(response.url)
            if outputtype=='json':
                output_dict = {'html':'false', 'csv':'false'}
                parsed = json.loads(response.text)
                results = json.dumps(parsed, sort_keys=True, indent=2)
            elif outputtype=='html':
                output_dict = {'html':'true', 'csv':'false'}
                results = response.text
            elif outputtype =='csv':
                myquery = response.text
                splitn = myquery.split('\n')
                value_list = []
                for i in splitn:
                    x = i.split(',')
                    value_list.append(x)
                print(value_list)
                file_name = datetime.strftime(datetime.now(), '%Y%m%d%H%m%s') + '.csv'
                file_path = os.path.join('static/exports/', file_name)

                if not os.path.exists('static/exports/'):
                            os.makedirs('static/exports/')
                with open(file_path, 'w', newline='') as outfile:
                    writer = csv.writer(outfile, delimiter = ',')
                    for x in value_list:
                        writer.writerow(x)
                outfile.close()
                output_dict = {'html':'false', 'csv':'true'}
                results = file_path
            else:
                output_dict = {'html':'false', 'csv':'false'}
                results = response.text

            self.render_template("response.html",{"output_dict":output_dict, "results":results})

        except Exception as e:
            print('Error:')
            print(e)
            self.redirect("/")


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
        (r"/query", testHandler),
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
