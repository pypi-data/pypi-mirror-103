# npynx
twisted based http server with multiple domain support

## usage
from test/TestServer.py
```python
from jinja2 import Template
from npynx import Server, Domain, response


class DomainTest(Domain):
    root_template = Template("ON {{ ROOT }}")

    def root(self, *args):
        return response(body=self.root_template.render(content="/"))

    def another(self, *args):
        return response(body=self.root_template.render(content="/another"))

    def __init__(self):
        Domain.__init__(self, "127.0.0.1:4200", {
            "": self.root,
            "/": self.root,
            "/another": self.another,
        })


if __name__ == '__main__':
    server = Server("tcp:4200")
    domain_test = DomainTest()
    server.add_domain(domain_test)

    try:
        server.start()
        server.join()
    except KeyboardInterrupt:
        server.terminate()
```