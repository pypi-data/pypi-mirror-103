from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class DlgDelUser(QDialog):
    '''
    Диалоговое окно по удалению пользователя.
    '''
    def __init__(self, i_db, i_sc):
        super().__init__()
        self.m_db = i_db
        self.m_sc = i_sc

        self.setFixedSize(350, 120)
        self.setWindowTitle('Удаление пользователя')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.lbl_sel = QLabel('Выберите пользователя для удаления:', self)
        self.lbl_sel.setFixedSize(200, 20)
        self.lbl_sel.move(10, 0)

        self.m_cmb_sel = QComboBox(self)
        self.m_cmb_sel.setFixedSize(200, 20)
        self.m_cmb_sel.move(10, 30)

        self.m_btn_ok = QPushButton('Удалить', self)
        self.m_btn_ok.setFixedSize(100, 30)
        self.m_btn_ok.move(230, 20)
        self.m_btn_ok.clicked.connect(self.del_user)

        self.m_btn_can = QPushButton('Отмена', self)
        self.m_btn_can.setFixedSize(100, 30)
        self.m_btn_can.move(230, 60)
        self.m_btn_can.clicked.connect(self.close)
        self.fill_conn_users()

    def fill_conn_users(self):
        self.m_cmb_sel.addItems([rec[1]
                                for rec in self.m_db.get_users_list()])

    def del_user(self):
        self.m_db.del_user(self.m_cmb_sel.currentText())
        self.close()
