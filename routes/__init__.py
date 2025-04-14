
def register_blueprints(app):
    from routes.usuario import usuario_bp
    from routes.administrador import administrador_bp
    from routes.pedidos import pedido_bp

    app.register_blueprint(usuario_bp, url_prefix='/usuario')
    app.register_blueprint(administrador_bp, url_prefix='/administrador')
    app.register_blueprint(pedido_bp, url_prefix='/pedido')
