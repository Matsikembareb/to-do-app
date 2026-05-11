"""Logging configuration with file and email handlers."""
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask


def setup_error_logging(app: Flask) -> None:
    """Configure logging for the application.
    
    Logs all INFO+ to file (app.log) with rotation.
    Sends ERROR+ to admin emails via SMTP when configured.
    
    File logging is always enabled. Email requires:
        - MAIL_SERVER: SMTP server address
        - MAIL_PORT: SMTP port (default: 587)
        - MAIL_USERNAME: SMTP username
        - MAIL_PASSWORD: SMTP password
        - ADMINS: Comma-separated list of admin emails
    """
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # File Handler - Always enabled
    log_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(os.path.dirname(log_dir), '..', '..', 'app.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    # Email Handler - Only if configured
    if app.config.get('ADMINS') and app.config.get('MAIL_SERVER'):
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_FROM'],
            toaddrs=app.config['ADMINS'],
            subject=f'Muzukuru API Error [{app.config.get("FLASK_ENV", "unknown")}]',
            credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
            secure=() if app.config['MAIL_USE_TLS'] else None
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(formatter)
        app.logger.addHandler(mail_handler)

    app.logger.setLevel(logging.INFO)
