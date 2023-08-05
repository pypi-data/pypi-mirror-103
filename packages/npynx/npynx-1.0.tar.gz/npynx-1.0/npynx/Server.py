from twisted.internet import protocol, reactor, endpoints

from os.path import abspath
from os import listdir
from multiprocessing import Process

try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser


def response(version="1.1", code="200", content_type="text/html", body=""):
    return "HTTP/{0} {1}\n" \
           "Content-Type: {2}\n" \
           "\n" \
           "{3}\n".format(version, code, content_type, body)


class Domain(object):
    def __init__(self, name: str, routes: dict):
        self.name = name
        self.routes = routes

    def add_route(self, path, func):
        self.routes[path] = func

    def on_request(self, headers, path):
        if path in self.routes.keys():
            return self.routes[path](headers, path)
        else:
            return response(code="404", body="404 - Should there be something here?")


class HTTPResponse(protocol.Protocol):
    def __init__(self, domains: dict):
        self.domains = domains

    def dataReceived(self, data):
        p = HttpParser()
        data_len = len(data)
        pdata_len = p.execute(data, data_len)
        resp = ""

        if pdata_len == data_len:
            if p.is_headers_complete():
                headers = p.get_headers()
                path = p.get_path()
                resp = self.domains[headers["Host"]].on_request(headers, path)
            else:
                resp = response(code="406", body="406 - Your request is weird, man.")

        self.transport.write(bytes(resp, "utf-8"))
        self.transport.loseConnection()


class HTTPResponseFactory(protocol.Factory):
    def __init__(self, domains: dict):
        self.domains = domains

    def buildProtocol(self, addr):
        return HTTPResponse(self.domains)

    def add_domain(self, domain: Domain):
        self.domains[domain.name] = domain

    def remove_domain(self, name: str):
        del self.domains[name]


class Server(Process):
    def __init__(self, address, domain_dir: str = None):
        Process.__init__(self)
        self.address = address
        self.http_resp_factory = HTTPResponseFactory({})
        self.domain_dir = domain_dir
        self.do_run = True

    def domain_names(self):
        return self.http_resp_factory.domains.keys()

    def add_domain(self, domain: Domain):
        self.http_resp_factory.add_domain(domain)

    def check_domain_dir(self):
        if not self.domain_dir:
            return

        for domain in listdir(abspath(self.domain_dir)):
            if domain in self.domain_names():
                self.http_resp_factory.remove_domain(domain)
            # todo: load module
            # self.http_resp_factory.add_domain()

    def run(self) -> None:
        endpoints.serverFromString(reactor, self.address).listen(self.http_resp_factory)
        reactor.run()
