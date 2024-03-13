from PySide6.QtCore import QMetaObject, QRect, QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFrame, QPushButton, QRadioButton, QStatusBar, QMainWindow,
    QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QProgressBar
)

from const import ICONS


class Ui_MainWindow(object):

    settings_window = None

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(433, 390)
        MainWindow.setMinimumSize(QSize(433, 390))
        MainWindow.setMaximumSize(QSize(433, 390))
        MainWindow.setWindowTitle('PDF Combiner')

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setEnabled(True)
        self.frame.setGeometry(QRect(9, 50, 411, 201))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setMouseTracking(True)
        self.frame.setAcceptDrops(True)

        self.layout = QVBoxLayout(self.frame)
        self.file_label = QLabel('Перетащите сюда архив', self.frame)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setWordWrap(True)
        self.layout.addWidget(self.file_label)
        self.frame.setLayout(self.layout)

        self.pushButton_choose = QPushButton(self.centralwidget)
        self.pushButton_choose.setText('Выбрать архив')
        self.pushButton_choose.setGeometry(QRect(10, 330, 411, 31))

        self.pushButton_start = QPushButton(self.centralwidget)
        self.pushButton_start.setText('Старт')
        self.pushButton_start.setGeometry(QRect(10, 260, 411, 31))

        self.pushButton_choose_res = QPushButton(self.centralwidget)
        self.pushButton_choose_res.setText('Выбрать куда сохранять результат')
        self.pushButton_choose_res.setGeometry(QRect(10, 295, 411, 31))

        self.pushButton_settings = QPushButton(self.centralwidget)
        self.pushButton_settings.setEnabled(True)
        self.pushButton_settings.setGeometry(QRect(400, 14, 20, 21))
        self.pushButton_settings.setBaseSize(QSize(13, 12))
        self.pushButton_settings.setMouseTracking(True)
        self.pushButton_settings.setTabletTracking(False)
        self.pushButton_settings.setToolTipDuration(0)
        icon = QIcon()
        icon.addFile(str(ICONS / 'settings.svg'))
        self.pushButton_settings.setIcon(icon)
        self.pushButton_settings.setIconSize(QSize(13, 12))
        self.pushButton_settings.setAutoDefault(False)
        self.pushButton_settings.setFlat(False)
        self.pushButton_settings.setToolTip('Дополнительные настройки')

        self.settings_pdf = QLabel(
            f'Размер страницы: <u>{MainWindow.page_size}</u> <br>'
            f'Количестов елементов на странице: <u>{MainWindow.quantity}</u>',
            self.centralwidget)
        self.settings_pdf.move(10, 7)

        self.radioButton_1 = QRadioButton(self.centralwidget)
        self.radioButton_1.setObjectName(u"radioButton")
        self.radioButton_1.setGeometry(QRect(320, 9, 28, 32))
        self.radioButton_1.setAutoExclusive(True)

        self.radioButton_2 = QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(352, 9, 28, 32))
        self.radioButton_2.setAutoExclusive(True)

        self.radioButton_3 = QRadioButton(self.centralwidget)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setGeometry(QRect(288, 9, 28, 32))
        self.radioButton_3.setAutoExclusive(True)

        self.progressbar = QProgressBar(MainWindow)
        self.progressbar.setGeometry(QRect(100, 155, 226, 45))
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)
        self.progressbar.hide()

        self.settings_window = SettingsWindow(MainWindow)
        self.settings_window.hide()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QMetaObject.connectSlotsByName(MainWindow)


class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setGeometry(parent.x() + 433, parent.y() + 31, 250, 390)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u'centralwidget')

        self.choose_page_size = QComboBox(self)
        self.choose_page_size.setGeometry(QRect(12, 36, 120, 35))
        self.choose_page_size.addItem('A4')
        self.choose_page_size.addItem('A0')
        self.choose_page_size.addItem('A1')
        self.choose_page_size.addItem('A2')
        self.choose_page_size.addItem('A3')
        self.choose_page_size.addItem('A5')
        self.choose_page_size.addItem('A6')
        self.choose_page_size.addItem('A7')
        self.choose_page_size.addItem('A8')
        self.choose_page_size.setCurrentText(parent.page_size)
        self.choose_page_size.setStyleSheet(
            """QComboBox::item:selected {
                color: white;
            }"""
        )

        label_page_size = QLabel('Размеры страниц', self)
        label_page_size.setGeometry(QRect(13, 8, 120, 35))
        label_page_size.setStyleSheet('color: white; \n'
                                      'font-weight: bold; \n'
                                      'font-size: 10pt;')

        self.choose_quantity = QSpinBox(self)
        self.choose_quantity.setMinimum(1)
        self.choose_quantity.setGeometry(QRect(12, 112, 120, 35))
        self.choose_quantity.setValue(parent.quantity)

        label_quantity = QLabel('Количество элементов на странице', self)
        label_quantity.setGeometry(QRect(13, 82, 240, 35))
        label_quantity.setStyleSheet('color: white; \n'
                                     'font-weight: bold; \n'
                                     'font-size: 10pt;')

        self.save_button = QPushButton(self)
        self.save_button.setGeometry(QRect(60, 345, 125, 35))
        self.save_button.setText('Сохранить')
