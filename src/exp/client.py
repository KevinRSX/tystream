import abr_name_converter

class Client:
    def __init__(self, abr, transport):
        self.abr = abr_name_converter.to_html(abr)
        self.transport = transport
    
    def generate_client_cmd(self):
        if self.transport == 'quic':
            cmd_client = "google-chrome-stable \
            --no-proxy-server \
            --enable-quic \
            --origin-to-force-quic-on=www.quictest.com:443 \
            --host-resolver-rules='MAP www.quictest.com:443 100.64.0.1:6121' \
            https://www.quictest.com/" + self.abr + '.html'
        elif self.transport == 'tcp':
            cmd_client = "google-chrome-stable \
                --no-proxy-server \
                --disable-application-cache \
                http://100.64.0.1/" + self.abr + '.html'
        return cmd_client