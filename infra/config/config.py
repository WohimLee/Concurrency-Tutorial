# core/project.py
from pydantic import BaseModel
from .common import CommonSettings
from .app1_settings import App1Settings
from .app2_settings import App2Settings

class GlobalSettings(BaseModel):
    common: CommonSettings = CommonSettings()
    app1: App1Settings = App1Settings()
    app2: App2Settings = App2Settings()


settings = GlobalSettings()

if __name__ == "__main__":

    print(settings.common.DATABASE_URL)
    print(settings.app1.JWT_SECRET)
    print(settings.app2.API_KEY)
    