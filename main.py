import pprint
import asyncio
import tornado.ioloop
import tornado.web
import tornado.httpclient

OPENAI_API_URL = "https://chat.openai.com/backend-api/conversation"

class ProxyHandler(tornado.web.RequestHandler):
    async def post(self):
        headers = self.request.headers
        body = self.request.body
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = await http_client.fetch(OPENAI_API_URL, method="POST", body=body, headers=headers)
        pprint.pprint(response)
        self.set_status(response.code)
        for header, value in response.headers.get_all():
            if header not in ('Content-Length', 'Transfer-Encoding', 'Content-Encoding', 'Connection'):
                self.set_header(header, value)
        self.write(response.body)

def make_app():
    return tornado.web.Application([
        (r"/", ProxyHandler),
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())