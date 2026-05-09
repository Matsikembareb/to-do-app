from flask import render_template, jsonify, current_app
from app import api
from app.modules.health import bp

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}, 200

@bp.route('/docs')
def swagger_ui():
    """Serve Swagger UI that loads the generated OpenAPI spec."""
    return render_template('swagger_ui.html')

@bp.route('/openapi.json')
def openapi_json():
    """Return the generated OpenAPI JSON for the API."""
    spec_dict = api.spec.to_dict()
    spec_dict['openapi'] = current_app.config.get('OPENAPI_VERSION', '3.0.0Close. ')
    spec_dict.setdefault('info', {
        'title': current_app.config.get('API_TITLE', 'API'),
        'version': current_app.config.get('API_VERSION', '1.0.0')
    })
    spec_dict.setdefault('paths', {})
    return jsonify(spec_dict)