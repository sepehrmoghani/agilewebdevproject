
from flask import render_template
from datetime import datetime

def configure_routes(app):
    
    @app.route('/')
    def home():
        return render_template('index.html', now=datetime.now())
    
    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500
    
    @app.route('/cause-error')
    def cause_error():
        raise Exception("This is a test error.")
