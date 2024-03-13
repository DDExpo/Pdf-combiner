from pathlib import Path
from datetime import datetime

from pypdf import PaperSize

from additional_utilities import get_desktop_path


PAPER_SIZES = {
    'A0': PaperSize.A0, 'A1': PaperSize.A1, 'A2': PaperSize.A2,
    'A3': PaperSize.A3, 'A4': PaperSize.A4, 'A5': PaperSize.A5,
    'A6': PaperSize.A6, 'A7': PaperSize.A7, 'A8': PaperSize.A8,
}

DEFAULT_SETTINGS: dict[str: str | int] = {
    'quantity': 16,
    'page_size': 'A4',
    'path': Path(get_desktop_path()),
    'theme': 'dark_red.xml',
}

BASE_DIR: Path = Path(__file__).parent.parent
ICONS: Path = BASE_DIR / 'icons/'
DATE_NAME = str(datetime.now().strftime('%d-%m-%Y'))
USER_SETTINGS: Path = BASE_DIR / 'user_settings.txt'

EXTRACT_DATA_DIR: Path = BASE_DIR / 'data/'

APP_ICON: str = str(ICONS / 'app_icon.jpg')
