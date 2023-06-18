from pyngrok import ngrok, conf


def ngrok_config():
    default_config = conf.get_default()
    default_config.config_path = "./ngrok.yml"
    default_config.region = "us"
    return default_config


def get_public_url(ngrok_token, port):
    config = ngrok_config()
    conf.set_default(config)
    ngrok.set_auth_token(ngrok_token)
    ngrok_tunnel = ngrok.connect(port, bind_tls=True)
    public_url = ngrok_tunnel.public_url
    return public_url
