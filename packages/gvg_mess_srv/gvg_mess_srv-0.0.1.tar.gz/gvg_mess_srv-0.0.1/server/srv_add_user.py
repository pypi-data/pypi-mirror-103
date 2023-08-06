import os
import sys
from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import binascii
BS_DR = os.path.join(os.getcwd(), '../')
sys.path.append(os.path.realpath(BS_DR))
from common.utils import create_user_hash

class DlgRegUser(QDialog):
    '''
    Диалоговое окно по созданию пользователя.
    '''
    def __init__(self, i_db, i_sc):
        super().__init__()

        self.m_db = i_db
        self.m_sc = i_sc

        self.setWindowTitle('Регистрация')
        self.setFixedSize(175, 183)
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.m_lbl_user_nm = QLabel('Введите имя пользователя:', self)
        self.m_lbl_user_nm.move(10, 10)
        self.m_lbl_user_nm.setFixedSize(150, 15)

        self.m_qle_user_nm = QLineEdit(self)
        self.m_qle_user_nm.setFixedSize(154, 20)
        self.m_qle_user_nm.move(10, 30)

        self.m_lbl_passwd = QLabel('Введите пароль:', self)
        self.m_lbl_passwd.move(10, 55)
        self.m_lbl_passwd.setFixedSize(150, 15)
        self.m_qle_passwd = QLineEdit(self)
        self.m_qle_passwd.setFixedSize(154, 20)
        self.m_qle_passwd.move(10, 75)
        self.m_qle_passwd.setEchoMode(QLineEdit.Password)

        self.m_lbl_passw2 = QLabel('Введите подтверждение:', self)
        self.m_lbl_passw2.move(10, 100)
        self.m_lbl_passw2.setFixedSize(150, 15)
        self.m_qle_passw2 = QLineEdit(self)
        self.m_qle_passw2.setFixedSize(154, 20)
        self.m_qle_passw2.move(10, 120)
        self.m_qle_passw2.setEchoMode(QLineEdit.Password)

        self.m_btn_ok = QPushButton('Сохранить', self)
        self.m_btn_ok.move(10, 150)
        self.m_btn_ok.clicked.connect(self.save_new_user)

        self.m_btn_cancel = QPushButton('Выход', self)
        self.m_btn_cancel.move(90, 150)
        self.m_btn_cancel.clicked.connect(self.close)

        self.m_qmb = QMessageBox()

        self.show()

    def save_new_user(self):
        if not self.m_qle_user_nm.text():
            self.m_qmb.critical(
                self, 'Ошибка', 'Не указано имя пользователя.')
            return
        elif self.m_qle_passwd.text() != self.m_qle_passw2.text():
            self.m_qmb.critical(
                self, 'Ошибка', 'Введённые пароли не совпадают.')
            return
        elif self.m_db.is_user_exists(self.m_qle_user_nm.text()):
            self.m_qmb.critical(
                self, 'Ошибка', 'Пользователь уже существует.')
            return

        lbt_hash = create_user_hash(self.m_qle_user_nm.text(),
                                    self.m_qle_passwd.text())
        self.m_db.add_user(self.m_qle_user_nm.text(), lbt_hash)
        self.m_qmb.information(self, 'Успех', 'Пользователь успешно зарегистрирован.')
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    l_dlg_add_user = DlgRegUser(None, None)
    app.exec_()
