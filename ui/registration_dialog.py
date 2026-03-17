from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from controllers.user_controller import UserController


class RegistrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.full_name = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)

        form = QFormLayout()
        form.addRow("ФИО:", self.full_name)
        form.addRow("Email:", self.email)
        form.addRow("Телефон:", self.phone)
        form.addRow("Пароль:", self.password)
        form.addRow("Подтвердите:", self.confirm_password)

        register_btn = QPushButton("Зарегистрироваться")
        register_btn.clicked.connect(self.register)

        layout.addLayout(form)
        layout.addWidget(register_btn)
        self.setLayout(layout)

    def register(self):
        name = self.full_name.text().strip()
        email = self.email.text().strip()
        phone = self.phone.text().strip()
        password = self.password.text()
        confirm = self.confirm_password.text()

        if password != confirm:
            QMessageBox.critical(self, "Ошибка", "Пароли не совпадают")
            return

        success, msg = UserController.register_user(name, email, phone, password)
        if success:
            QMessageBox.information(self, "Успех", msg)
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", msg)