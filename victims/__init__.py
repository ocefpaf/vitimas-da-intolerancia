from aiocache import cached, caches
from sanic import Sanic
from sanic_compress import Compress
from sanic_jinja2 import SanicJinja2

from victims.data import Data
from victims.settings import CACHE, STATIC_DIR, TITLE


app = Sanic("vitimas_da_intolerancia")
app.static("/static", str(STATIC_DIR))
jinja = SanicJinja2(app, pkg_name="victims")
caches.set_config(CACHE)
Compress(app)


@cached(key="cases")
async def get_cases():
    data = Data()
    return await data.cases()


@app.route("/")
@jinja.template("home.html")
async def home(request):
    return {"cases": await get_cases(), "title": TITLE, "url_path": "/"}


@app.route("/about.html")
@jinja.template("about.html")
async def about(request):
    return {"title": TITLE, "url_path": "/about.html"}
