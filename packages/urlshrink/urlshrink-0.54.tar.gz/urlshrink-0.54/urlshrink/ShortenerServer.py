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
from dataset import connect, Database, Table
from time import sleep

try:
    import qrcode
except ImportError:
    qrcode = None


TIMESTAMP_FORMAT = "%Y.%m.%d %H:%M:%S"


class ShortenerServer(Process):
    _db: Database = None
    _url: Table = None

    def __init__(self, db_path: str, salt: str, host: str = "127.0.0.1", port: int = 4004, debug: bool = False,
                 domain: str = "", qr: bool = False, anonymous: bool = False, max_tries_per_suffix: int = 4):
        Process.__init__(self)
        self._db = connect("sqlite:///{}".format(db_path))
        self._url = self._db["url"]
        self._ips = self._db["ips"]

        self.host = host
        self.port = port
        self.debug = debug
        self.app = Flask(__name__, static_folder=join(getcwd(), "static"), static_url_path="")
        self.domain = domain
        self.qr = qr
        self.anonymous = anonymous
        self.max_tries_per_suffix = max_tries_per_suffix
        self.hashids = Hashids(salt)

        if self.qr and qrcode is None:
            self.qr = False

        # --------------- ROUTES ---------------
        @self.app.route("/")
        def root():
            return self.show_shorten_page()

        @self.app.route("/shorten")
        def shorten():
            return self.show_shorten_page()

        @self.app.route("/search")
        def search():
            self.increment_hits()
            v = self.get_values()
            if not self.has_and_not_none(v, ["suffix"]):
                return render_template("search.html", domain=domain)
            e = self._url.find_one(suffix=v["suffix"])
            if e is None:
                return render_template("search.html", **self._jp({"error": "The suffix '{}' does not exist."
                                                                 .format(v["suffix"])}))
            if e["key"] != "" and self.tries_left(e["suffix"]) == 0:
                return render_template("search.html", **self._jp({"error": "Your out of luck. No tries left."}))
            if e["key"] != "" and not self.has_and_not_none(v, ["key"]):
                return render_template("search.html", **self._jp({"error": "This suffix requires a key."}))
            if e["key"] != v["key"]:
                tl = self.increment_hits()
                return render_template("search.html", **self._jp({"error": "Key is not correct. "
                                                                           "You have {} more tries.".format(tl)}))
            e.update({
                "domain": domain
            })

            return render_template("statistics.html", **e)

        @self.app.route("/<path>")
        def redirect_to(path):
            self.increment_hits()
            e = self._url.find_one(**{"suffix": path})
            if e is None:
                return render_template("shorten.html", **self._jp({"error": "Incorrect suffix."}))
            if e["key"] == "":
                return redirect(e["url"])
            v = self.get_values()
            e.update({"domain": domain})
            if self.has_and_not_none(v, ["key"]):
                log.debug(v)
                if e["key"] == v["key"]:
                    return redirect(e["url"])
                if not self.anonymous:
                    self.increment_tries()
                return render_template("key.html", **self._jp(e))
            return render_template("key.html", **self._jp(e))

        @self.app.route("/del")
        def delete():
            self.increment_hits()
            v = self.get_values()
            log.debug(v)
            return render_template("")  # todo

    # --------------- STATIC METHODS ---------------

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
        if len(d.keys()) == 0:
            return False
        for k in keys:
            if k in dk and d[k] is None:
                log.debug(d, k)
                return False
        return True

    @staticmethod
    def generate_qrcode(url: str) -> str:
        c = qrcode.make(url)
        b = BytesIO()
        c.save(b, format="PNG")
        return b64encode(b.getvalue()).decode('utf-8')

    # --------------- CLASS METHODS ---------------

    def show_shorten_page(self):
        self.increment_hits()
        v = self.get_values()
        if "url" in v.keys() and v["url"] != "":
            if not v["url"].startswith("http://") or not v["url"].startswith("https://"):
                v["url"] = "https://" + v["url"]
            if self.is_url(v["url"]):
                return render_template("shorten.html", **self._jp(self.shorten_url(v)))
            return render_template("shorten.html", **self._jp({"error": "URL is invalid."}))
        return render_template("shorten.html", **self._jp({}))

    def shorten_url(self, data: dict) -> dict:
        e = {
            "created_by": self.get_remote_addr(),
            "url": data["url"],
            "suffix": self.hashids.encode(len(self._url)),
            "hits": 0,
            "last_visited": None,
            "qr": None,
            "delete_at": (datetime.now() + timedelta(weeks=420)).strftime(TIMESTAMP_FORMAT),
            "key": None
        }

        if self.qr:
            e["qr"] = self.generate_qrcode(self.domain + e["suffix"])
        if "key" in data.keys():
            e["key"] = data["key"]
        if self.has_and_not_none(data, ["time", "unit"]):
            log.debug(data)
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
                e["delete_at"] = (datetime.now() + x).strftime(TIMESTAMP_FORMAT)
            except ValueError:
                pass
        self._url.insert(e)
        return e

    def create_ip_entry(self, ip: str, values: dict):
        v = {
            "ip": ip,
            "tries": 0,
            "hits": 0
        }
        v.update(values)
        self._ips.insert(v)

    def increment_hits(self) -> int:
        if self.anonymous:
            return -1
        ip = self.get_remote_addr()
        e = self._ips.find_one(ip=ip)
        if e is None:
            self.create_ip_entry(ip, {"hits": 1})
        else:
            e["hits"] += 1
            self._ips.update(e, ["ip"])
        return e["hits"]

    def increment_tries(self) -> int:
        if self.anonymous:
            return -1
        ip = self.get_remote_addr()
        e = self._ips.find_one(ip=ip)
        if e is None:
            self.create_ip_entry(ip, {"tries": 1})
        else:
            e["tries"] += 1
            self._ips.update(e, ["ip"])
        return e["tries"]

    def tries_left(self, suffix):
        if self.anonymous:
            return 1
        ip = self.get_remote_addr()
        e = self._ips.find_one(ip=ip, suffix=suffix)
        if e is None:
            return self.max_tries_per_suffix
        return e["tries"]

    def create_jinja_params(self, d: dict) -> dict:
        d.update({
            "domain": self.domain,
            "anonymous": self.anonymous
        })
        return d

    def _jp(self, d: dict) -> dict:
        return self.create_jinja_params(d)

    def clean_db(self):
        while True:
            for item in self._url.find(delete_at={'<': datetime.now().strftime(TIMESTAMP_FORMAT)}):
                log.debug("Deleting {}", item)
                self._url.delete(suffix=item["suffix"])
            sleep(1)

    def start_cleaner(self):
        dbct = Thread(target=self.clean_db)
        dbct.daemon = True
        dbct.start()

    def run(self) -> None:
        self.start_cleaner()
        self.app.run(self.host, self.port, self.debug)
