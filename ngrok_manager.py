from pyngrok import ngrok, conf


class NgrokManager:
    def __init__(self, token):
        conf.get_default().auth_token = token

    def start_tunnel(self, port, proto="http", domain=None, auth=None):
        options = {"proto": proto, "addr": port}

        if domain:
            options["hostname"] = domain

        if auth:
            options["auth"] = auth

        tunnel = ngrok.connect(**options)
        return tunnel.public_url

    def stop_tunnel(self, port):
        for tunnel in ngrok.get_tunnels():
            if str(port) in tunnel.config["addr"]:
                ngrok.disconnect(tunnel.public_url)
                break

    def get_active_tunnels(self):
        return ngrok.get_tunnels()

    def __del__(self):
        ngrok.kill()
