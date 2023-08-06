import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QLabel, QTableView, QDialog, \
    QPushButton, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
BS_DR = os.path.join(os.getcwd(), '../')
sys.path.append(os.path.realpath(BS_DR))
from common.variables import DB_NAME, DEFAULT_PORT,\
    SRV_SECTION, PAR_PORT, PAR_ADDR, PAR_DB_PATH, PAR_DB_FILE
from server.db_man import DbManager
#from server.srv_sck import MessSrv
from server.srv_add_user import DlgRegUser
from server.srv_del_user import DlgDelUser

class ServConfWindow(QDialog):
    '''
    Диалоговое окно по настройке конфигурации сервера.
    '''
    def __init__(self, i_cfgs, i_cfgs_full_file):
        super().__init__()

        self.m_cfgs = i_cfgs
        self.m_cfg_file = i_cfgs_full_file
        self.setFixedSize(515, 260)
        self.setWindowTitle('Настройки сервера')

        self.m_lbl_db_path = QLabel('Путь до файла базы данных: ', self)
        self.m_lbl_db_path.move(10, 10)
        self.m_lbl_db_path.setFixedSize(240, 15)

        self.m_led_db_path = QLineEdit(self)
        self.m_led_db_path.setFixedSize(400, 20)
        self.m_led_db_path.move(10, 30)

        self.m_qpu_sel_db_path = QPushButton('Обзор...', self)
        self.m_qpu_sel_db_path.move(425, 28)

        self.m_qpu_sel_db_path.clicked.connect(self.open_file_dialog)

        self.m_qlb_db_file = QLabel('Имя файла базы данных: ', self)
        self.m_qlb_db_file.move(10, 68)
        self.m_qlb_db_file.setFixedSize(180, 15)

        self.m_led_db_file = QLineEdit(self)
        self.m_led_db_file.move(350, 66)
        self.m_led_db_file.setFixedSize(150 , 20)

        self.m_qlb_port = QLabel('Номер порта для соединений:', self)
        self.m_qlb_port.move(10, 108)
        self.m_qlb_port.setFixedSize(180, 15)

        self.m_qle_port = QLineEdit(self)
        self.m_qle_port.move(350, 108)
        self.m_qle_port.setFixedSize(150, 20)

        self.m_qlb_ip = QLabel('С какого IP принимаем соединения:', self)
        self.m_qlb_ip.move(10, 148)
        self.m_qlb_ip.setFixedSize(180, 15)

        self.m_qle_ip_note = QLabel(' если это поле пустое, то\n принимаются соединения с любых адресов.', self)
        self.m_qle_ip_note.move(10, 168)
        self.m_qle_ip_note.setFixedSize(500, 30)
        self.m_qle_ip = QLineEdit(self)
        self.m_qle_ip.move(350, 148)
        self.m_qle_ip.setFixedSize(150, 20)

        self.m_btn_save = QPushButton('Сохранить' , self)
        self.m_btn_save.move(190 , 220)

        self.m_btn_close = QPushButton('Закрыть', self)
        self.m_btn_close.move(275, 220)
        self.m_btn_close.clicked.connect(self.close)
        self.m_qpu_sel_db_path.clicked.connect(self.open_file_dialog)

        self.m_led_db_path.insert(self.m_cfgs[SRV_SECTION][PAR_DB_PATH])
        self.m_led_db_file.insert(self.m_cfgs[SRV_SECTION][PAR_DB_FILE])
        self.m_qle_port.insert(self.m_cfgs[SRV_SECTION][PAR_PORT])
        self.m_qle_ip.insert(self.m_cfgs[SRV_SECTION][PAR_ADDR])

        self.m_btn_save.clicked.connect(self.save_srv_cfg)

        self.show()

    def open_file_dialog(self):
        global g_dlg_of
        g_dlg_of = QFileDialog(self)
        l_path = g_dlg_of.getExistingDirectory()
        l_path = l_path.replace('/', '\\')
        self.m_led_db_path.clear()
        self.m_led_db_path.insert(l_path)

        self.m_led_db_path.insert(self.m_cfgs[SRV_SECTION][PAR_DB_PATH])
        self.m_led_db_file.insert(self.m_cfgs[SRV_SECTION][PAR_DB_FILE])
        self.m_qle_port.insert(self.m_cfgs[SRV_SECTION][PAR_PORT])
        self.m_qle_ip.insert(self.m_cfgs[SRV_SECTION][PAR_ADDR])

    def save_srv_cfg(self):
        global config_window
        l_qmb = QMessageBox()
        self.m_cfgs[SRV_SECTION][PAR_DB_PATH] = self.m_led_db_path.text()
        self.m_cfgs[SRV_SECTION][PAR_DB_FILE] = self.m_led_db_file.text()
        self.m_cfgs[SRV_SECTION][PAR_ADDR] = self.m_qle_ip.text()

        try:
            l_port = int(self.m_qle_port.text())
        except ValueError:
            l_qmb.warning(self, 'Ошибка', 'Порт должен быть числом!')
            return

        if not (1023 < l_port < 65536):
            l_qmb.warning(self, 'Ошибка', 'Порт должен быть от 1024 до 65536!')
            return

        self.m_cfgs[SRV_SECTION][PAR_PORT] = str(l_port)

        with open(self.m_cfg_file, 'w') as l_file:
            self.m_cfgs.write(l_file)
        l_qmb.information(self, 'OK', 'Настройки успешно сохранены!')
        self.close()

class UserStatsWindow(QDialog):
    '''
    Диалоговое окно по статистике сервера.
    '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Статистика клиентов')
        self.setFixedSize(600, 700)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.btn_close = QPushButton('Закрыть', self)
        self.btn_close.move(250, 650)
        self.btn_close.clicked.connect(self.close)

        self.tbl_users_stats = QTableView(self)
        self.tbl_users_stats.move(10, 10)
        self.tbl_users_stats.setFixedSize(580, 620)


class MainSrvWin(QMainWindow):
    '''
    Главное окно сервера.
    '''
    def __init__(self, i_db, i_cfgs, i_cfgs_full_file, i_srv_sck):
        super().__init__()

        self.m_db = i_db
        self.m_cfgs = i_cfgs
        self.m_cfg_file = i_cfgs_full_file
        self.m_srv_sck = i_srv_sck

        la_exit = QAction('Выход', self)
        la_exit.setShortcut('Ctrl+Q')
        la_exit.triggered.connect(qApp.quit)

        la_refr = QAction('Обновить список', self)
        la_refr.triggered.connect(self.refresh_act_users)

        la_show_stats = QAction('Статистика пользователей', self)
        la_show_stats.triggered.connect(self.show_user_statistics)

        la_show_serv_conf = QAction('Настройки сервера', self)
        la_show_serv_conf.triggered.connect(self.show_serv_config)

        self.m_btn_reg_user = QAction('Регистрация пользователя', self)
        self.m_btn_del_user = QAction('Удаление пользователя', self)

        self.statusBar()
        self.statusBar().showMessage('Server is working...')
        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(la_exit)
        self.toolbar.addAction(la_refr)
        self.toolbar.addAction(la_show_stats)
        self.toolbar.addAction(la_show_serv_conf)
        self.toolbar.addAction(self.m_btn_reg_user)
        self.toolbar.addAction(self.m_btn_del_user)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Message Server')

        self.label = QLabel('Список подключённых клиентов:', self)
        self.label.setFixedSize(240, 15)
        self.label.move(10, 25)

        self.m_tbl_act_users = QTableView(self)
        self.m_tbl_act_users.move(10, 45)
        self.m_tbl_act_users.setFixedSize(780, 400)
        self.refresh_act_users()
        self.m_btn_reg_user.triggered.connect(self.reg_user)
        self.m_btn_del_user.triggered.connect(self.del_user)
        self.show()

    def reg_user(self):
        global g_win_reg_user
        g_win_reg_user = DlgRegUser(self.m_db, self.m_srv_sck)
        g_win_reg_user.show()

    def del_user(self):
        global g_win_del_user
        g_win_del_user = DlgDelUser(self.m_db, self.m_srv_sck)
        g_win_del_user.show()

    def show_user_statistics(self):
        global user_stats_win
        user_stats_win = UserStatsWindow()

        l_list_model = QStandardItemModel()
        l_list_model.setHorizontalHeaderLabels(
            ['Имя Клиента', 'Последний раз входил', 'Сообщений отправлено', 'Сообщений получено'])

        l_stats_users = self.m_db.get_users_stats()
        for rec in l_stats_users:
            user_nm, last_log_tm, sent, accepted = rec
            fld_user_nm = QStandardItem(user_nm)
            fld_user_nm.setEditable(False)
            fld_last_log_tm = QStandardItem(str(last_log_tm.replace(microsecond=0)))
            fld_last_log_tm.setEditable(False)
            fld_sent = QStandardItem(str(sent))
            fld_sent.setEditable(False)
            fld_accepted = QStandardItem(str(accepted))
            fld_accepted.setEditable(False)
            l_list_model.appendRow([fld_user_nm, fld_last_log_tm, fld_sent, fld_accepted])

        user_stats_win.tbl_users_stats.setModel(l_list_model)
        user_stats_win.tbl_users_stats.resizeColumnsToContents()
        user_stats_win.tbl_users_stats.resizeRowsToContents()
        user_stats_win.show()


    def refresh_act_users(self):
        l_act_users = self.m_db.get_act_users()
        l_mod_dat = QStandardItemModel()
        l_mod_dat.setHorizontalHeaderLabels(['Имя Клиента', 'IP Адрес', 'Порт', 'Время подключения'])
        for rec in l_act_users:
            l_fld_us = QStandardItem(rec.user_nm)
            l_fld_us.setEditable(False)
            l_fld_ad = QStandardItem(rec.addr)
            l_fld_ad.setEditable(False)
            l_fld_pr = QStandardItem(str(rec.port))
            l_fld_pr.setEditable(False)
            l_fld_tm = QStandardItem(str(rec.log_tm.replace(microsecond=0)))
            l_fld_tm.setEditable(False)
            l_mod_dat.appendRow([l_fld_us, l_fld_ad, l_fld_pr, l_fld_tm])
        self.m_tbl_act_users.setModel(l_mod_dat)
        self.m_tbl_act_users.resizeColumnsToContents()
        self.m_tbl_act_users.resizeRowsToContents()
        print('Refresh was done.')


    def show_serv_config(self):
        global serv_config_win
        serv_config_win = ServConfWindow(self.m_cfgs, self.m_cfg_file)
        serv_config_win.show()


if __name__ == '__main__':
    l_app = QApplication(sys.argv)
    l_mw = MainSrvWin(None, None, None, None)
    l_app.exec_()

