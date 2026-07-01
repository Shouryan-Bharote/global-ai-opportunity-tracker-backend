import re
from datetime import datetime
from urllib.parse import urlparse


class Normalizer:
    """A utility class for normalizing raw data into consistent formats."""

    def __new__(cls) -> None:
        """Prevents instantiation of the Normalizer class."""
        raise TypeError("Normalizer cannot be instantiated.")

    @staticmethod
    def normalize_string(value: object) -> str | None:
        """Normalizes a value into a trimmed, collapsed string."""
        if value is None:
            return None

        string = re.sub(r"\s+", " ", str(value)).strip()
        return string if string else None

    @staticmethod
    def normalize_list(value: object) -> list[str]:
        """Normalizes various inputs into a clean list of strings."""
        if value is None:
            return []
        
        items: list[object]
        if isinstance(value, (list, tuple, set)):
            items = list(value)
        else:
            items = [value]
            
        normalized = []
        for item in items:
            val = Normalizer.normalize_string(item)
            if val:
                normalized.append(val)
                
        return list(dict.fromkeys(normalized))

    @staticmethod
    def normalize_boolean(value: object) -> bool | None:
        """Normalizes a value into a boolean."""
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        
        truthy = {"true", "yes", "y", "1", "on", "enabled"}
        falsy = {"false", "no", "n", "0", "off", "disabled"}

        normalized = str(value).strip().lower()
        
        if normalized in truthy:
            return True
        if normalized in falsy:
            return False
            
        return None

    @staticmethod
    def normalize_integer(value: object) -> int | None:
        """Normalizes a value into an integer."""
        if value is None or isinstance(value, bool):
            return None
        
        if isinstance(value, int):
            return value

        s = str(value).strip()
        if re.match(r"^-?\d+$", s):
            try:
                return int(s)
            except ValueError:
                return None
        return None

    @staticmethod
    def normalize_float(value: object) -> float | None:
        """Normalizes a value into a float."""
        if value is None or isinstance(value, bool):
            return None
        
        if isinstance(value, (int, float)):
            return float(value)

        try:
            return float(str(value).strip())
        except (ValueError, TypeError):
            return None

    @staticmethod
    def normalize_url(value: object) -> str | None:
        """Normalizes a value into a URL."""
        url = Normalizer.normalize_string(value)
        if not url:
            return None
        
        parsed = urlparse(url)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return url
        return None

    @staticmethod
    def normalize_datetime(value: object) -> datetime | None:
        """Normalizes a value into a datetime."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value

        s = str(value).strip().replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(s)
        except (ValueError, TypeError):
            return None


__all__ = ["Normalizer"]
