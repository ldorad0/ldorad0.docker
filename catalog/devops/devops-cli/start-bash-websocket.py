#!/usr/bin/env python

import argparse
import asyncio
from aiohttp import web
import aiohttp
import os
import pty
import fcntl

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    loop = asyncio.get_running_loop()
    master, slave = pty.openpty()
    name = os.ttyname(slave)
    pid = os.fork()
    if pid == 0:
        os.setsid()
        os.dup2(slave,0)
        os.dup2(slave,1)
        os.dup2(slave,2)
        os._exit(os.execv('/bin/bash',('$', )))

    stdin = os.fdopen(master, 'wb+', buffering=0)
    fl = fcntl.fcntl(master, fcntl.F_GETFL)
    fcntl.fcntl(master, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def pipe_data_received(ws):
        data = stdin.read()
        print('Incoming data: %s' % data)
        try:
            asyncio.ensure_future(ws.send_str(data.decode()))
        except:
            pass

    loop.add_reader(master, pipe_data_received, ws)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            stdin.write(msg.data.encode())
        elif msg.type == aiohttp.WSMsgType.BINARY:
            stdin.write(msg.data)
        elif msg.type == aiohttp.WSMsgType.CLOSE:
            await ws.close()
            print('Connection closed with WSMsgType.CLOSE (PID:%s)' % pid)
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            print('Connection closed with WSMsgType.CLOSED (PID:%s)' % pid)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('Connection closed with WSMsgType.ERROR (PID:%s)' % pid)

    print('Connection refreshed (PID:%s)' % pid)
    return ws

def parse_args(**kwargs):

  parser = argparse.ArgumentParser(description='Binds a websocket to a local bash process')
  parser.add_argument('--port', '-p', help="HTTP Port to listen on", default=5000)
  parser.add_argument('--route', '-r', help="Specifier for websocket HTTP Endpoint", default='ws')
  return parser.parse_args()

def start():
  args = parse_args()
  app = web.Application()
  app.add_routes([web.get('/ws', websocket_handler)])
  web.run_app(app, port=int(args.port))

if __name__ == '__main__':
  start()