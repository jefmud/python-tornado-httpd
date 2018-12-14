# python-tornado-httpd
A simple HTTP daemon built with TornadoWeb

This is not meant to scale or have any meaningful security, but will function as a very lightweight server
for internal use and development.  Note-- that this server is not particularly well suited for serving anything
but tiny media files.  You will have to add some protocol control on Range and Content-range for the browser.

Ben Darnell recommends looking into HLS or MPEG-DASH.

tornadohttpd.py

based on-- https://github.com/tornadoweb/tornado (by Ben Darnell)

For testing purposes, not intended for production use ;-)

if you want to use this commercially, refer to TornadoWeb license below
(https://github.com/tornadoweb/tornado/blob/master/LICENSE)


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
