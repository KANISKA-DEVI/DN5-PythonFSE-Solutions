from flask import Flask, jsonify
from config     import Config
from extensions import db, migrate
from courses.routes  import courses_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(courses_bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'status': 'error', 'message': 'Not found'}), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)