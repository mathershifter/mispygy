# coding: utf-8
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from flask import Flask, request, render_template
from flask.ext.mistune import Mistune, markdown

app = Flask(__name__)
app.debug = True

class CodeRenderer(mistune.Renderer):
    """Return highlighted code blocks"""
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code.strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)

renderer = CodeRenderer()
Mistune(app, renderer=renderer)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['markdown']:
            content = request.form['markdown']
    return render_template('index.html', **locals())

app.run(debug=True)