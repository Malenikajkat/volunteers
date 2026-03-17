import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget, QFormLayout, QHBoxLayout,
    QMessageBox, QDateEdit, QSpinBox, QComboBox, QTableWidget, QTableWidgetItem,
    QFileDialog
)
from PyQt6.QtCore import QDate
from controllers.user_controller import UserController
from controllers.volunteer_controller import VolunteerController
from controllers.task_controller import TaskController
from utils.export import export_volunteer_report_to_excel, export_tasks_report_to_pdf


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления волонтерами")
        self.resize(800, 600)

        self.current_user = None
        self.login_screen()

    def login_screen(self):
        self.setCentralWidget(QWidget())
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<h2>Вход в систему</h2>"))

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Войти")
        login_btn.clicked.connect(self.handle_login)

        register_btn = QPushButton("Регистрация")
        register_btn.clicked.connect(self.open_registration)

        layout.addLayout(self.create_form([("Email:", self.email_input), ("Пароль:", self.password_input)]))
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)

        self.centralWidget().setLayout(layout)

    def open_registration(self):
        from ui.registration_dialog import RegistrationDialog
        dialog = RegistrationDialog(self)
        dialog.exec()

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        success, user_or_msg = UserController.login(email, password)
        if success:
            self.current_user = user_or_msg
            self.main_screen()
        else:
            QMessageBox.critical(self, "Ошибка", user_or_msg)

    def main_screen(self):
        self.setCentralWidget(QTabWidget())
        tabs = self.centralWidget()

        tabs.addTab(self.volunteers_tab(), "Волонтеры")
        tabs.addTab(self.tasks_tab(), "Задачи")
        tabs.addTab(self.reports_tab(), "Отчеты")

    def create_form(self, fields):
        form = QFormLayout()
        for label, widget in fields:
            form.addRow(label, widget)
        return form

    def volunteers_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.volunteer_list = QListWidget()
        self.volunteer_name = QLineEdit()
        self.volunteer_age = QSpinBox()
        self.volunteer_age.setRange(10, 100)
        self.volunteer_phone = QLineEdit()
        self.volunteer_specialization = QLineEdit()

        add_btn = QPushButton("Добавить волонтера")
        add_btn.clicked.connect(self.add_volunteer)
        refresh_btn = QPushButton("Обновить список")
        refresh_btn.clicked.connect(self.load_volunteers)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по имени или специализации")
        search_btn = QPushButton("Поиск")
        search_btn.clicked.connect(self.search_volunteers)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)

        layout.addLayout(self.create_form([
            ("Имя:", self.volunteer_name),
            ("Возраст:", self.volunteer_age),
            ("Телефон:", self.volunteer_phone),
            ("Специализация:", self.volunteer_specialization)
        ]))
        layout.addWidget(add_btn)
        layout.addLayout(search_layout)
        layout.addWidget(QLabel("Список волонтеров:"))
        layout.addWidget(self.volunteer_list)

        edit_del_layout = QHBoxLayout()
        edit_btn = QPushButton("Редактировать")
        edit_btn.clicked.connect(self.edit_volunteer)
        del_btn = QPushButton("Удалить")
        del_btn.clicked.connect(self.delete_volunteer)
        edit_del_layout.addWidget(edit_btn)
        edit_del_layout.addWidget(del_btn)
        layout.addLayout(edit_del_layout)

        widget.setLayout(layout)
        self.load_volunteers()
        return widget

    def load_volunteers(self):
        self.volunteer_list.clear()
        volunteers = VolunteerController.get_all_volunteers()
        for v in volunteers:
            self.volunteer_list.addItem(f"{v.name} ({v.specialization})")

    def search_volunteers(self):
        query = self.search_input.text().strip()
        if not query:
            self.load_volunteers()
            return
        self.volunteer_list.clear()
        results = VolunteerController.search_volunteers(query)
        for v in results:
            self.volunteer_list.addItem(f"{v.name} ({v.specialization})")

    def add_volunteer(self):
        name = self.volunteer_name.text().strip()
        age = self.volunteer_age.value()
        phone = self.volunteer_phone.text().strip()
        spec = self.volunteer_specialization.text().strip()

        success, msg = VolunteerController.add_volunteer(name, age, phone, spec)
        if success:
            self.load_volunteers()
            self.clear_volunteer_form()
            QMessageBox.information(self, "Успех", msg)
        else:
            QMessageBox.critical(self, "Ошибка", msg)

    def edit_volunteer(self):
        QMessageBox.information(self, "Info", "Редактирование временно недоступно")

    def delete_volunteer(self):
        QMessageBox.information(self, "Info", "Удаление временно недоступно")

    def clear_volunteer_form(self):
        self.volunteer_name.clear()
        self.volunteer_age.setValue(18)
        self.volunteer_phone.clear()
        self.volunteer_specialization.clear()

    def tasks_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.task_title = QLineEdit()
        self.task_desc = QLineEdit()
        self.task_deadline = QDateEdit()
        self.task_deadline.setDate(QDate.currentDate())
        self.task_required = QSpinBox()
        self.task_required.setRange(1, 50)

        add_task_btn = QPushButton("Добавить задачу")
        add_task_btn.clicked.connect(self.add_task)

        layout.addLayout(self.create_form([
            ("Название:", self.task_title),
            ("Описание:", self.task_desc),
            ("Срок:", self.task_deadline),
            ("Кол-во волонтеров:", self.task_required)
        ]))
        layout.addWidget(add_task_btn)

        self.task_list = QListWidget()
        layout.addWidget(QLabel("Задачи:"))
        layout.addWidget(self.task_list)

        self.assign_combo_vol = QComboBox()
        self.assign_combo_task = QComboBox()
        assign_btn = QPushButton("Назначить волонтера")
        assign_btn.clicked.connect(self.assign_volunteer)

        layout.addWidget(QLabel("Назначить:"))
        layout.addWidget(self.assign_combo_vol)
        layout.addWidget(self.assign_combo_task)
        layout.addWidget(assign_btn)

        self.load_tasks_and_volunteers()
        widget.setLayout(layout)
        return widget

    def load_tasks_and_volunteers(self):
        self.task_list.clear()
        tasks = TaskController.get_all_tasks()
        for t in tasks:
            self.task_list.addItem(f"{t.title} до {t.deadline.strftime('%d.%m.%Y')}")

        self.assign_combo_task.clear()
        for t in tasks:
            self.assign_combo_task.addItem(t.title, t.id)

        self.assign_combo_vol.clear()
        volunteers = VolunteerController.get_all_volunteers()
        for v in volunteers:
            self.assign_combo_vol.addItem(v.name, v.id)

    def add_task(self):
        title = self.task_title.text().strip()
        desc = self.task_desc.text().strip()
        deadline = self.task_deadline.date().toPyDate()
        required = self.task_required.value()

        success, msg = TaskController.add_task(title, desc, deadline, required)
        if success:
            self.load_tasks_and_volunteers()
            QMessageBox.information(self, "Успех", msg)
        else:
            QMessageBox.critical(self, "Ошибка", msg)

    def assign_volunteer(self):
        vol_id = self.assign_combo_vol.currentData()
        task_id = self.assign_combo_task.currentData()

        success, msg = TaskController.assign_volunteer_to_task(vol_id, task_id)
        if success:
            QMessageBox.information(self, "Успех", msg)
        else:
            QMessageBox.critical(self, "Ошибка", msg)

    def reports_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        gen_excel = QPushButton("Экспорт: активность волонтеров")
        gen_excel.clicked.connect(lambda: export_volunteer_report_to_excel())

        gen_pdf = QPushButton("Экспорт: сводка по задачам")
        gen_pdf.clicked.connect(lambda: export_tasks_report_to_pdf())

        layout.addWidget(gen_excel)
        layout.addWidget(gen_pdf)
        layout.addStretch()

        widget.setLayout(layout)
        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())