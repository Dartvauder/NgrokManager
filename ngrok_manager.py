from pyngrok import ngrok


class NgrokManager:
    def __init__(self, token):
        ngrok.set_auth_token(token)

        self.tunnels = {}

    def start_tunnel(self, port, proto='http', domain=None):
        if domain:
            tunnel = ngrok.connect(port, proto=proto, hostname=domain)
        else:
            tunnel = ngrok.connect(port, proto=proto)
        tunnel_name = f"{port}"
        self.tunnels[tunnel_name] = tunnel
        return tunnel.public_url

    def stop_tunnel(self, name):
        if name in self.tunnels:
            ngrok.disconnect(self.tunnels[name].public_url)
            del self.tunnels[name]
            return True
        return False
