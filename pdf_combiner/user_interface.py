import traceback
import os
from pathlib import Path

import patoolib
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Slot
from qt_material import apply_stylesheet, QtStyleTools

from const import (
    EXTRACT_DATA_DIR, USER_SETTINGS, BASE_DIR, DEFAULT_SETTINGS)
from utility import delete_all_data
from creating_pdf import create_combine_pdf
from design_ui_python import Ui_MainWindow


class PdfCombiner(QMainWindow, QtStyleTools):
    def __init__(self):
        super().__init__()

        if USER_SETTINGS.exists():
            with open(USER_SETTINGS, 'r', encoding='utf-8') as f:
                for settings in f:
                    key, val = settings.split('|')
                    if key not in DEFAULT_SETTINGS:
                        continue
                    DEFAULT_SETTINGS[key.strip()] = val.strip()

        self.path_to_archive: str | None = None
        self.count_not_pdfs: int = 0
        self.path_to_save_folder: Path = Path(DEFAULT_SETTINGS['path'])
        self.quantity: int = int(DEFAULT_SETTINGS['quantity'])
        self.page_size: str = DEFAULT_SETTINGS['page_size']
        self.theme: str = DEFAULT_SETTINGS['theme']

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.apply_stylesheet(self, self.theme)
        self.message_box = QMessageBox(self)

        self.ui.pushButton_choose.clicked.connect(self._get_new_path)

        self.ui.pushButton_choose_res.clicked.connect(
            self._get_new_path_for_res)

        self.ui.pushButton_settings.clicked.connect(
            self._open_advanced_settings)

        self.ui.radioButton_1.clicked.connect(
            lambda: self._set_stylesheet('dark_cyan.xml'))
        self.ui.radioButton_2.clicked.connect(
            lambda: self._set_stylesheet('dark_amber.xml'))
        self.ui.radioButton_3.clicked.connect(
            lambda: self._set_stylesheet('dark_red.xml'))

        self.ui.settings_window.save_button.clicked.connect(
            self._save_settings)

        self.ui.pushButton_start.clicked.connect(
            lambda: self._winrar_combine(self.path_to_archive))

    @Slot()
    def _set_stylesheet(self, style) -> None:
        apply_stylesheet(self, style)
        self.theme = style

    @Slot()
    def _save_settings(self) -> None:
        self.quantity = self.ui.settings_window.choose_quantity.value()
        self.page_size = self.ui.settings_window.choose_page_size.currentText()

        self.ui.settings_pdf.setText(
            f'Размер страницы: <u>{self.page_size}</u> <br>'
            f'Количестов елементов на странице: <u>{self.quantity}</u>')
        self.message_box.information(self, 'Уведомление',
                                     'Настройки успешно сохранены!')

    @Slot()
    def _open_advanced_settings(self) -> None:
        if self.ui.settings_window.isVisible():
            self.ui.settings_window.hide()
        else:
            self.ui.settings_window.show()

    @Slot()
    def _get_new_path_for_res(self) -> None:
        directory_path = QFileDialog.getExistingDirectory(
            caption='Выберите папку',
            options=QFileDialog.ShowDirsOnly)

        if not directory_path:
            pass
        else:
            self.path_to_save_folder = Path(directory_path)

    @Slot()
    def _get_new_path(self) -> None:
        directory_path = QFileDialog.getOpenFileName(
            filter='Архивы (*.zip *.rar)')[0]

        if not directory_path:
            pass
        elif not directory_path.endswith(('.rar', '.zip')):
            self.message_box.warning(
                self, 'Error',
                'Выберите файл с расширением ".rar" или ".zip"',
            )
        else:
            self.path_to_archive = directory_path
            self.ui.file_label.setText(directory_path)

    @Slot()
    def _winrar_combine(self, rar_path_file: str) -> None:

        str_e = None

        try:
            if rar_path_file is None:
                return

            elif self.quantity <= 0:
                self.message_box.warning(
                    self, 'Warning',
                    'Количество елементов на одной страницы \n'
                    'не должно быть равно или меньше нкля!')
                return

            self.ui.progressbar.show()
            self.ui.progressbar.setValue(15)

            if (EXTRACT_DATA_DIR.exists() and
               len(os.listdir(EXTRACT_DATA_DIR)) != 0):
                delete_all_data(EXTRACT_DATA_DIR)

            patoolib.extract_archive(
                archive=Path(rar_path_file, encoding='utf-8').absolute(),
                outdir=EXTRACT_DATA_DIR)

            pdfs: list[Path] = []

            for file in Path(EXTRACT_DATA_DIR).iterdir():
                if file.suffix == ".pdf":
                    pdfs.append(file)
                else:
                    self.count_not_pdfs += 1

            if self.count_not_pdfs:
                self.message_box.warning(
                    self, 'Warning',
                    'Были встречены файлы не являющимися PDF.\n'
                    f'В количестве: {self.count_not_pdfs}\n'
                    'Они будут пропущены!')
            self.count_not_pdfs = 0

            create_combine_pdf(
                self, pdfs, page_size=self.page_size,
                quantity=self.quantity,
                pdf_file_path_origin=Path(self.path_to_save_folder))

            self.message_box.information(
                    self, 'Successful', 'Фаил был успешно скомбинирован!')

        except patoolib.util.PatoolError as e:
            str_e = e.__str__()
            if 'was not found' in str_e:
                self.message_box.critical(
                    self, 'Ошибка',
                    'Архив не найден, возможно он был:\n'
                    'Перенесён, удален или переименован!')
            elif 'returned non-zero exit status 10' in str_e:
                self.message_box.critical(
                    self, 'Ошибка',
                    'Архив не должен быть пустым')

        except RuntimeError as e:
            str_e = e.__str__()
            if 'Too many open files' in str_e:
                self.message_box.critical(
                    self, 'Ошибка',
                    'Слишком много PDF в одном архиве \n Разделите архив!')

        except Exception as e:
            str_e = e.__str__()
            if str_e == ('The process cannot access the file because'
                         ' it is being used by another process.'):
                self.message_box.critical(
                    self, 'Ошибка', 'Фаил используется другим процессом!')
            elif str_e == 'document closed or encrypted':
                self.message_box.critical(
                    self, 'Ошибка', 'Файл закрыт, либо зашифрован!')
            elif str_e == 'document closed':
                self.message_box.critical(
                    self, 'Ошибка', 'Файл закрыт!')
            else:
                self.message_box.critical(self, 'Ошибка',
                                          'Что-то пошло не так!')

        finally:
            self.ui.progressbar.setValue(100)
            self.ui.progressbar.close()

            with open(BASE_DIR / 'Logs.txt', 'w', encoding='utf-8') as logs:
                logs.write(f'{traceback.format_exc()} \n {str_e}')

    @Slot()
    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    @Slot()
    def dropEvent(self, event) -> None:
        if event:
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            if not file_path.endswith(('.rar', '.zip')):
                self.message_box.warning(
                    self, 'Error',
                    'Выберите файл с расширением ".rar" или ".zip"',
                )
            else:
                self.path_to_archive = file_path
                self.ui.file_label.setText(file_path)
        else:
            event.ignore()

    @Slot()
    def closeEvent(self, event) -> None:
        answer = self.message_box.question(
            self, 'Exit', 'Вы хотите закрыть приложение?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if answer == QMessageBox.Yes:
            with open(USER_SETTINGS, 'w', encoding='utf-8') as f:
                f.write(f'page_size|{self.page_size}\n'
                        f'quantity|{self.quantity}\n'
                        f'path|{self.path_to_save_folder}\n'
                        f'theme|{self.theme}')
            event.accept()
        else:
            event.ignore()
