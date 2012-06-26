import os
import sys
import re
from cgi import parse_qs

curdir = os.path.dirname(__file__)
sys.path.append(curdir)
from checksum import *

def response(environ, start_response, post_data):
    """Receives the post transaction completion data from the zaakpay site and 
    confirms the integrity of the data received based on checksum calculations.
    """
    
    recvd_checksum = post_data['checksum']
    checksum = Checksum(post_data)
    all_params = checksum.getAllParams()
    checksum_check = checksum.verifyChecksum(recvd_checksum, all_params, secret);

    html_template = open(curdir + '/templates/response.html').read()
    output = html_template %(str(checksum.outputResponse(checksum_check)))
    
    start_response('200 OK', [('Content-Type', 'text/html'),('Content-Length', str(len(output)))])
    return [output]

def posttozaakpay(environ, start_response, post_data):
    """POST's the form data received to the Zaakpay transaction API along with 
    a checksum of the data being transferred for security purposes"""

    checksum = Checksum(post_data)
    all = checksum.getAllParams()
    chcksum = checksum.calculateChecksum(secret, all)

    html_template = open(curdir + '/templates/posttozaakpay.html').read()
    output = html_template %(str(checksum.outputForm(chcksum)))
    start_response('200 OK', [('Content-Type', 'text/html'),('Content-Length', str(len(output)))])
    return [output]

urls = [
    (r'response/', response),
    (r'posttozaakpay/', posttozaakpay)
]

def application(environ, start_response):
    """Main WSGI function to be called on running the script."""

    request_body = environ['wsgi.input'].read()
    path = environ.get('PATH_INFO', '').lstrip('/')
    raw_data = parse_qs(request_body,1)

    post_data = {}
    for key in raw_data:
        post_data[key] = raw_data[key][0]
    
    #Calls the relevant function based on the URL being accessed.
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            return callback(environ, start_response, post_data)
    
    #Error case.
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']