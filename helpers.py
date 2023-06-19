def configure_ngrok():
    from pyngrok import conf
    config = conf.get_default()
    config.config_path = "./ngrok.yml"
    config.region = "us"
    conf.set_default(config)


def get_public_url(ngrok_token, port):
    try:
        from pyngrok import ngrok
        configure_ngrok()
        ngrok.set_auth_token(ngrok_token)
        ngrok_tunnel = ngrok.connect(port, bind_tls=True)
        public_url = ngrok_tunnel.public_url
        return public_url
    except Exception:  # noqa
        return None
