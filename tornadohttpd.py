
# tornadohttpd.py
# a simple web server based on TornadoWeb
# https://github.com/tornadoweb/tornado
#
# For testing purposes, not intended for production use ;-)
# 
# if you want to use this commercially, refer to TornadoWeb licenses
#
# Jeff Muday, Wake Forest University
#
docstring = """
Usage:
    
    python tornadohttpd.py --port <int:port> --dir <relative or absolute base directory of files>
    
    example:
    
    python tornadohttpd.py --port 8080 --dir ./www
    
    Notes:
     1) if port argument is ommitted default port is 8080
     2) server does not check if existing server is running on that port
     3) On most systems, if you are an unprivileged user,
           you will have to use a high port greater than 1024
     4) By default, the files served come out of the base program directory e.g. './'
           
    Thank you TornadoWeb Team!
    https://github.com/tornadoweb/tornado
"""
import datetime
import mimetypes
import os
import os.path
import sys
import time
import tornado.httpserver
import tornado.ioloop
import tornado.log
import tornado.options
import tornado.web

BASE_PATH = './'
INDEX_FILES = ['index.html', 'index.htm']

class FileHandler(tornado.web.RequestHandler):
    def get(self, requestpath):
        """get/render the path"""
        
        # normalize the path
        path = os.path.normpath(os.path.join(BASE_PATH, requestpath))
        
        # case 1, path is a directory ==> look for index file
        if os.path.isdir(path):
            # see if a preferred index file is in the directory
            # and we can redirect to the alternate path
            alt_path = ''
            for f in INDEX_FILES:
                temp_path = os.path.normpath(os.path.join(path, f))
                if os.path.isfile(temp_path):
                    alt_path = os.path.join('/', requestpath, f)
                    
            if alt_path:
                # redirect to the alternate path (directory index file)
                self.redirect(alt_path)
            else:
                # no alt_path ==> render a directory listing
                self.write('<h2>Directory Listing of {}</h2>\n'.format(requestpath))
                self.write('<table>\n')
                for f in os.listdir(path):
                    fpath = os.path.normpath(os.path.join(path, f))
                    rpath = os.path.normpath(os.path.join(requestpath, f))
                    fstat = os.lstat(fpath)
                    ftime = tornado.web.escape.xhtml_escape(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fstat.st_mtime)))
                    row = '<tr><td><a href="/{}">{}</a></td><td>{}</td></tr>\n'.format(rpath, f, ftime)
                    self.write(row)
                self.write('</table><br /><hr>')
                self.write('<b>Powered by TornadoHTTP, TornadoWeb</b> @ {}'.format(datetime.datetime.now()))
                self.finish()
                
        
        # case 2, path is a file ==> render file
        if os.path.isfile(path):
            mime_type = mimetypes.guess_type(path)
            self.set_header("Content-Type", mime_type[0] or 'text/plain')
    
            # note you will have to add some code to buffer big media files.
            # Ben Darnell has some directions on this, look those over.
            outfile = open(path, "rb")
            for line in outfile:
                self.write(line)
            self.finish()
        
        # case 3, path DOES NOT exist ==> 404 error
        if not(os.path.exists(path)):
            raise tornado.web.HTTPError(404)
        else:
            # something else bad happened ==> 400 error
            raise tornado.web.HTTPError(400)

def simple_http_server(port=8080):
    """run a simple http server, default port=8080"""
    tornado.log.enable_pretty_logging()
    application = tornado.web.Application([
        (r"/(.*)", FileHandler),
    ])
    print("Tornado HTTP server starting on port {}".format(port))
    print("(control-c to quit, may also require browser connection refresh)")
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

def usage():
    """show usage"""
    print(docstring)
    sys.exit(0)
    
def main():
    """main server starting point, check command line for --port argument"""
    global BASE_PATH
    
    if '--help' in sys.argv or '-h' in sys.argv:
        usage()
        
    if '--dir' in sys.argv:
        try:
            BASE_PATH = sys.argv[sys.argv.index('--dir') + 1]
            if not os.path.exists(BASE_PATH):
                print("ERROR: directory path does not exist!")
                usage()
        except:
            print("ERROR: must supply a valid directory path")
            usage()
        
    port = 8080
    if '--port' in sys.argv:
        try:
            port = int(sys.argv[sys.argv.index('--port')+1])
        except:
            print("ERROR: port must be an integer value")
            usage()
            
            
    simple_http_server(port)    
    
    
if __name__ == "__main__":
    main()
