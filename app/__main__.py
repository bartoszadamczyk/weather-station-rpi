import sentry_sdk
from app.env_config import CONFIG

if __name__ == "__main__":
    # Init Sentry before any app imports
    sentry_sdk.init(server_name=CONFIG.DEVICE_ID)

    from app import init

    init.run()
