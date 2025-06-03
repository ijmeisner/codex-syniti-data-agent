from flask import Flask, request, render_template_string
from .crew import build_crew


def create_app() -> Flask:
    app = Flask(__name__)

    TEMPLATE = """
    <!doctype html>
    <title>Data Agent</title>
    <h1>Query Analyzer</h1>
    <form method=post>
      <input name=query placeholder="Enter statement">
      <button type=submit>Analyze</button>
    </form>
    {% if error %}<p>{{ error }}</p>{% endif %}
    {% if result %}<pre>{{ result }}</pre>{% endif %}
    """

    @app.route('/', methods=['GET', 'POST'])
    def index():
        error = None
        result = None
        if request.method == 'POST':
            query = request.form.get('query', '').strip()
            if not query:
                error = 'query is required'
            else:
                crew = build_crew(query)
                result = crew.kickoff()

        return render_template_string(TEMPLATE, error=error, result=result)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)
