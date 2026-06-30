# models.py

from pydantic import BaseModel, Field

class Viewport(BaseModel):
    """
    Represents the browser viewport dimensions.
    """

    width: int = Field(default=1920, ge=1)
    height: int = Field(default=1080, ge=1)

    def to_patchright(self) -> dict[str, int]:
        """
        Convert the viewport into Patchright's expected format.
        """

        return {
            "width": self.width,
            "height": self.height,
        }


class BrowserLaunchOptions(BaseModel):
    """
    Configuration used when launching the browser.
    """

    headless: bool = Field(default=True)

    viewport: Viewport = Field(default_factory=Viewport)

    locale: str = Field(default="en-US")

    slow_mo: int = Field(default=0, ge=0)

    ignore_https_errors: bool = Field(default=False)

    channel: str | None = Field(default=None)

    # proxy: str | None = None
    # user_agent: str | None = None
    # timeout: int = Browser.DEFAULT_TIMEOUT
    # downloads_path: Path | None = None
    # permissions: list[str] = []
    # storage_state: Path | None = None