import abr_name_converter

class Client:
    def __init__(self, abr_rule):
        self.abr = abr_name_converter.to_html(abr_rule)
    
    def generate_client_cmd(self):
        cmd_client = "google-chrome-stable \
        --no-proxy-server \
        --enable-quic \
        --origin-to-force-quic-on=www.quictest.com:443 \
        --host-resolver-rules='MAP www.quictest.com:443 100.64.0.1:6121' \
        https://www.quictest.com/" + self.abr + '.html'
        return cmd_client