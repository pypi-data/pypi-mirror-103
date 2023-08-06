from flask import Flask, render_template, request, redirect
from os import getcwd
from os.path import join
from loguru import logger as log
from multiprocessing import Process
from urllib.parse import urlparse
from datetime import datetime, timedelta
from hashids import Hashids
from base64 import b64encode
from io import BytesIO
from threading import Thread
from podb import DB, DBEntry
from time import sleep

try:
    import qrcode
except ImportError:
    qrcode = None


class URL(DBEntry):
    def __init__(self, suffix, url):
        DBEntry.__init__(self)
        self.url = url
        self.suffix = suffix
        self.hits = 0
        self.last_visited = None
        self.qr = None
        self.delete_at = datetime.now() + timedelta(weeks=420)
        self.key = None


class ShortenerServer(Process):
    def __init__(self, db_path: str, salt: str, host: str = "127.0.0.1", port: int = 4004, debug: bool = False,
                 domain: str = "", qr: bool = False):
        Process.__init__(self)
        self.db = DB(db_path)
        self.host = host
        self.port = port
        self.debug = debug
        self.app = Flask(__name__, static_folder=join(getcwd(), "static"), static_url_path="")
        self.domain = domain
        self.qr = qr
        self.hashids = Hashids(salt)

        if self.qr and qrcode is None:
            self.qr = False

        @self.app.route("/")
        def root():
            v = self.get_values()
            if "url" in v.keys() and v["url"] != "":
                if not v["url"].startswith("http://") or not v["url"].startswith("https://"):
                    v["url"] = "https://" + v["url"]
                if self.is_url(v["url"]):
                    data = self.shorten_url(v)
                    return render_template("index.html", **data.__dict__, domain=domain)
                return render_template("index.html", error="URL is invalid.", domain=domain)
            return render_template("index.html", domain=domain)

        @self.app.route("/<path>")
        def redirect_to(path):
            e = self.db.find_one({"suffix": path})
            if e is None:
                return render_template("index.html", error="Incorrect suffix.", domain=domain)
            self.increment_url_hit_count(e)  # TODO(nbdy): self.get_remote_addr()
            return redirect(e.url)

    @staticmethod
    def get_remote_addr() -> str:
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            return request.environ['REMOTE_ADDR']
        else:
            return request.environ['HTTP_X_FORWARDED_FOR']

    @staticmethod
    def get_values() -> dict:
        r = {}
        for item in request.values:
            r[item] = request.values[item]
        return r

    @staticmethod
    def is_url(url) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    @staticmethod
    def has_and_not_none(d, keys) -> bool:
        dk = d.keys()
        for k in keys:
            if k in dk and (d[k] != '' or d[k] is not None):
                return False
        return True

    @staticmethod
    def generate_qrcode(url: str) -> str:
        c = qrcode.make(url)
        b = BytesIO()
        c.save(b, format="PNG")
        return b64encode(b.getvalue()).decode('utf-8')

    def shorten_url(self, data: dict) -> URL:
        e = URL(self.hashids.encode(self.db.size()), data["url"])

        if self.qr:
            e.qr = self.generate_qrcode(self.domain + e.suffix)
        if "key" in data.keys():
            e.key = data["key"]
        if self.has_and_not_none(data, ["time", "unit"]):
            x = 0
            try:
                n = int(data["time"])
                if data["unit"] == "Seconds":
                    x = timedelta(seconds=n)
                elif data["unit"] == "Minutes":
                    x = timedelta(minutes=n)
                elif data["unit"] == "Hours":
                    x = timedelta(hours=n)
                elif data["unit"] == "Days":
                    x = timedelta(days=n)
                elif data["unit"] == "Weeks":
                    x = timedelta(weeks=n)
                e.delete_at = (e.delete_at + x)
            except ValueError:
                pass
        print(e)
        self.db.insert(e)
        return e

    def increment_url_hit_count(self, entry: URL) -> None:
        entry.hits += 1
        entry.last_visited = datetime.now()
        self.db.update(entry)

    def clean_db(self):
        while True:
            for e in self.db.find_before(datetime.now()):
                log.debug("Deleting: {0}", e)
                self.db.delete({"id": e.suffix})
            sleep(1)

    def run(self) -> None:
        dbct = Thread(target=self.clean_db)
        dbct.daemon = True
        dbct.start()
        self.app.run(self.host, self.port, self.debug)
