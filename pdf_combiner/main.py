import traceback
import sys

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon

from const import (
    EXTRACT_DATA_DIR, APP_ICON, BASE_DIR)
from utility import (
    delete_all_data, check_dirs_ifnot_create)
from user_interface import PdfCombiner


def main():

    window = None

    try:
        check_dirs_ifnot_create([EXTRACT_DATA_DIR])

        app = QApplication(sys.argv)
        app_icon = QIcon(APP_ICON)
        app.setWindowIcon(app_icon)

        window = PdfCombiner()
        window.show()

        app.exec()

    except Exception:
        QMessageBox.critical(window, 'Ошибка', 'Что-то пошло не так!')
        with open(BASE_DIR / 'Logs.txt', 'w') as logs:
            logs.write(traceback.format_exc())

    finally:
        delete_all_data(EXTRACT_DATA_DIR)


if __name__ == '__main__':
    main()
