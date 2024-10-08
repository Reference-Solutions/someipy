import socket
from someipy import SOMEIPDatagramHandler, SOMEIPUDPServer

class SomeIPLibrary:

    def __init__(self):
        self.server_ip = None
        self.server_port = None
        self.events = []
        self.response = None

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

    def send_someip_message(self, message):
        """
        Sends a SOME/IP message to the server.
        """
        if not self.server_ip or not self.server_port:
            raise ValueError("Server IP and port must be set before sending message.")
        
        try:
            # Send a message to the SOME/IP server using UDP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(message, (self.server_ip, self.server_port))
                return f"Message sent to {self.server_ip}:{self.server_port}."
        except Exception as e:
            raise RuntimeError(f"Failed to send SOME/IP message: {e}")

    def receive_someip_response(self, buffer_size=1024, timeout=5):
        """
        Receives the SOME/IP response from the server.
        """
        if not self.server_ip or not self.server_port:
            raise ValueError("Server IP and port must be set before receiving response.")
        
        try:
            # Create a UDP socket to receive the response
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(timeout)
                self.response, addr = sock.recvfrom(buffer_size)
                return f"Response received from {addr}: {self.response}"
        except Exception as e:
            raise RuntimeError(f"Failed to receive SOME/IP response: {e}")

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
        
    def _start_someip_udp_server(self, timeout=None):
        """
        Starts the SOME/IP UDP server with an optional timeout.
        """
        class MySOMEIPHandler(SOMEIPDatagramHandler):
            def handle(self):
                event = self.request
                self.server.library.events.append(event)  # Store event in the main library

        # Set up the UDP server to receive SOME/IP events
        server = SOMEIPUDPServer((self.server_ip, self.server_port), MySOMEIPHandler)
        server.library = self  # Attach the library instance to access events
        
        if timeout:
            server.timeout = timeout
        return server

    def clear_events(self):
        """
        Clears the list of stored SOME/IP events.
        """
        self.events = []

    def get_events(self):
        """
        Returns the list of SOME/IP events.
        """
        return self.events

    def get_response(self):
        """
        Returns the SOME/IP response message.
        """
        return self.response
