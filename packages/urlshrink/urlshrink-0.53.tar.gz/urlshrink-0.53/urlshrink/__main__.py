from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from loguru import logger as log

from urlshrink.ShortenerServer import ShortenerServer


def main():
    ap = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    ap.add_argument("-d", "--database", help="database to use", default="shrnk")
    ap.add_argument("-q", "--qr", help="Enable qr code generation", action="store_true")
    ap.add_argument("--salt", help="Hashids salt", default="666")
    ap.add_argument("--host", help="what do you think", default="127.0.0.1")
    ap.add_argument("--port", help="certainly not the port on which we will bind", default=4005)
    ap.add_argument("--domain", help="customize branding and enable more functionality", type=str)
    ap.add_argument("--debug", help="enable debugging messages", action="store_true")
    a = ap.parse_args()

    if a.domain is not None:
        if not a.domain.startswith('http://') and not a.domain.startswith('https://'):
            log.warning("Protocol not specified. Assuming https.")
            a.domain = "https://" + a.domain
        if not a.domain.endswith('/'):
            a.domain += "/"

    if a.qr and not a.domain:
        log.error("Can not use QR Code functionality without the servers TLD")
        exit(0)

    log.debug("Initializing the ShortenerServer")
    server = ShortenerServer(a.database, a.salt, a.host, a.port, a.debug, a.domain, a.qr)

    try:
        log.debug("Starting ShortenerServer")
        server.start()
        server.join()
    except KeyboardInterrupt:
        log.debug("Stopping processes")
        server.terminate()


if __name__ == '__main__':
    main()
