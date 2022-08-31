import re, traceback

from flask import Flask, request, render_template, Blueprint

try:
	from jinja2.utils import markupsafe
	Markup = markupsafe.Markup
	escape = markupsafe.escape
	from jinja2 import pass_eval_context as evalcontextfilter
except ImportError:
	from jinja2 import evalcontextfilter
	from jinja2 import Markup, escape

from . import yahoo, data
from .constants import PROGNAME

app = Flask(PROGNAME, template_folder="stock_tracker/templates")

@app.route("/")
def index():
    tickers = request.args.get("tickers", "").replace(",", " ").split()
    stocks = [yahoo.Stock(t) for t in tickers]
    status = {}
    try:
        for stock in stocks:
            status[stock.ticker] = data.evaluate(stock)
    except Exception:
        error = traceback.format_exc()
        print(error)
    else:
        error = None
    return render_template("index.html", tickers=status, error=error)


blueprint = Blueprint('custom_template_filters', __name__)


@evalcontextfilter
@blueprint.app_template_filter()
def nl2br(context, value: str) -> str:
    result = "<br />".join(re.split(r'(?:\r\n|\r|\n){2,}', escape(value)))

    if context.autoescape:
        result = Markup(result)

    return result

app.register_blueprint(blueprint)
