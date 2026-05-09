from flask import render_template, jsonify, current_app
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
    # Access the Api instance from current_app.extensions
    try:
        api = current_app.extensions.get('flask-smorest')
        if api and hasattr(api, 'spec'):
            spec_dict = api.spec.to_dict()
        else:
            spec_dict = {}
    except Exception:
        spec_dict = {}
    return jsonify(spec_dict)