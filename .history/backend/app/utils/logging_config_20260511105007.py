"""Logging configuration with email handler for errors."""
import logging
from logging.handlers import SMTPHandler
from flask import Flask


def setup_error_logging(app: Flask) -> None:
    """Configure email logging for application errors.
    
    Sends errors to admin emails via SMTP when configured.
    Requires environment variables:
        - MAIL_SERVER: SMTP server address
        - MAIL_PORT: SMTP port (default: 587)
        - MAIL_USERNAME: SMTP username
        - MAIL_PASSWORD: SMTP password
        - ADMINS: Comma-separated list of admin emails
    """
    if not app.config.get('ADMINS') or not app.config.get('MAIL_SERVER'):
        return

    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr=app.config['MAIL_FROM'],
        toaddrs=app.config['ADMINS'],
        subject=f'Muzukuru API Error [{app.config.get("FLASK_ENV", "unknown")}]',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
        secure=() if app.config['MAIL_USE_TLS'] else None
    )

    mail_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    mail_handler.setFormatter(formatter)

    app.logger.addHandler(mail_handler)
    app.logger.setLevel(logging.INFO)
