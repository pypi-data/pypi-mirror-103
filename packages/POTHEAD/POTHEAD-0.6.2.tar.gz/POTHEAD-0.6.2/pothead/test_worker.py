from threading import Thread
from unittest import TestCase
from wsgiref import simple_server
from socket import socket, AF_INET, SOCK_STREAM, timeout as TimeoutError

from pothead.gating import wait_for_idle_cpus

from .worker import Server, LoadBalancer

demo_app = simple_server.demo_app
demo_app.wait_for_slot = wait_for_idle_cpus(0.1)


class WorkerConnection:
    def __init__(self, sock: socket):
        self.sock = sock

    def send_request(self):
        self.sock.sendall(b"GET / HTTP/1.1\r\n\r\n")


class DummyBroker:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(("localhost", 0))
        self.sock.listen(1)

    def addr(self):
        return self.sock.getsockname()

    def accept(self, timeout) -> WorkerConnection:
        self.sock.settimeout(timeout)
        try:
            sock, _ = self.sock.accept()
            return WorkerConnection(sock)
        except TimeoutError:
            return None


def mock_balancer(addresses):
    class MockBalancer(LoadBalancer):
        def refresh(self):
            self._balancer.provision(addresses)

    return MockBalancer


class WorkerTest(TestCase):
    def test_load_balancing(self):
        broker_a, broker_b = (DummyBroker() for _ in range(2))

        worker = Server(
            ("", 0),
            demo_app,
            load_balancer=mock_balancer(map(DummyBroker.addr, (broker_a, broker_b))),
        )
        Thread(target=worker.poll_loop, daemon=True).start()

        connection_a = broker_a.accept(0.1)
        connection_b = broker_b.accept(0.1)

        assert broker_a.accept(0.1) is None
        assert broker_b.accept(0.1) is None

        connection_b.send_request()
        assert broker_b.accept(0.1) is not None

        connection_a.send_request()
        assert broker_a.accept(0.1) is not None
