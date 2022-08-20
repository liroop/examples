# -*- coding: utf-8 -*-

# setup
# pip install pyzmq

import zmq
import os
import time
import random

def front(ctx):
    sock = ctx.socket(zmq.ROUTER)
    sock.bind("tcp://*:9001")
    return sock

def back(ctx):
    sock = ctx.socket(zmq.DEALER)
    sock.bind("tcp://*:9002")
    return sock

def router(ctx, front, back):
    return zmq.device(zmq.QUEUE, front, back)

def start_proxy():
    ctx = zmq.Context(1)
    f = front(ctx)
    b = back(ctx)
    try:
        print ('start proxy...')
        #zmq.device(zmq.QUEUE, f, b)
        #zmq.device(zmq.FORWARDER, f, b)
        zmq.device(zmq.STREAMER, f, b)
    except KeyboardInterrupt:
        print ('STOPED')
    finally:
        f.close()
        b.close()
        ctx.term()


def start_monitorq():
    from zmq.devices.monitoredqueue import monitored_queue
    ctx = zmq.Context(1)
    s_in = ctx.socket(zmq.ROUTER)
    s_in.bind('tcp://*:9001')
    s_out = ctx.socket(zmq.DEALER)
    s_out.bind('tcp://*:9002')
    s_mon = ctx.socket(zmq.PUB)
    s_mon.bind('tcp://*:9003')
    try:
        print ('start monitored queue...')
        monitored_queue(s_in, s_out, s_mon)
    except KeyboardInterrupt:
        pass
    finally:
        s_in.close()
        s_out.close()
        s_mon.close()
        ctx.term()


def start_monitor():
    ctx = zmq.Context(1)
    sock = ctx.socket(zmq.SUB)
    sock.setsockopt(zmq.SUBSCRIBE, "")
    sock.connect('tcp://localhost:9003')
    while True:
        print ('MON:' , sock.recv_multipart())


def start_client():
    ctx = zmq.Context(1)
    sock = ctx.socket(zmq.REQ)
    sock.connect('tcp://localhost:9001')
    while True:
        sock.send('PING:%d' % os.getpid())
        print (sock.recv())
        time.sleep(random.random())


def start_serv():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.REP)
    sock.bind('tcp://*:5555')
    #sock.connect('tcp://localhost:5555')
    while True:
        print (sock.recv())
        #sock.send('PONG:%d' % os.getpid())
        sock.send(b'PONG:')
        #p sock.recv()


if __name__ == '__main__':
    import sys
    f = {
        'serv'      : start_serv,
        'client'    : start_client,
        'proxy'     : start_proxy,
        'monitorq'  : start_monitorq,
        'monitor'   : start_monitor,
    }.get(sys.argv[1])
    f()
