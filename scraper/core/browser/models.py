from pydantic import BaseModel, Field

from shared.constants.browser import Browser
from shared.constants.browser import Browser

class Viewport(BaseModel):
    width: int = Field(default=1920, ge=1)
    height: int = Field(default=1080, ge=1)
    
class BrowserLaunchOptions(BaseModel):
    headless: bool = True

    viewport: Viewport = Viewport()

    locale: str = "en-US"

    slow_mo: int = 0
    
    # proxy: str | None = None

    # user_agent: str | None = None

    # timeout: int = Browser.DEFAULT_TIMEOUT

    # downloads_path: Path | None = None

    # permissions: list[str] = []

    # storage_state: Path | None = None
    