from flask import Flask, jsonify, request
from .crew import build_crew


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route('/analyze', methods=['POST'])
    def analyze():
        data = request.get_json(force=True)
        query = data.get('query')
        if not query:
            return jsonify({'error': 'query is required'}), 400

        crew = build_crew(query)
        result = crew.kickoff()
        return jsonify({'result': result})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)
