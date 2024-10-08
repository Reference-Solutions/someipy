import socket
from someipy import SOMEIPDatagramHandler, SOMEIPUDPServer

class SomeIPLibrary:

    def __init__(self):
        self.server_ip = None
        self.server_port = None
        self.events = []

    def someip_connection_validation(self, server_ip, server_port):
        """
        Validates the connection to a SOME/IP server by opening a UDP socket.
        """
        try:
            # Setup a UDP connection to the SOME/IP server
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)  # 5-second timeout for validation
            sock.sendto(b'', (server_ip, server_port))
            sock.close()
            return f"Connection to {server_ip}:{server_port} is valid."
        except Exception as e:
            raise RuntimeError(f"Failed to connect to SOME/IP server: {e}")

    def someip_receive_events_udp(self, server_ip, server_port):
        """
        Receives SOME/IP events from the UDP server and stores them in a list.
        """
        try:
            self.server_ip = server_ip
            self.server_port = server_port

            # Define the handler for the SOME/IP datagrams
            class MySOMEIPHandler(SOMEIPDatagramHandler):
                def handle(self):
                    # Store events in the events list
                    event = self.request
                    SomeIPLibrary().events.append(event)

            # Set up the UDP server to receive SOME/IP events
            server = SOMEIPUDPServer((server_ip, server_port), MySOMEIPHandler)
            server.serve_forever()
        except Exception as e:
            raise RuntimeError(f"Error receiving SOME/IP events: {e}")
        
        return self.events
