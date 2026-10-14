import sys
from pathlib import Path

from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class SqlLabWindow(QMainWindow):
    CONNECTION_NAME = "lab3_connection"

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Лабораторная работа №3 — PyQt5 + SQL")
        self.resize(950, 650)

        self.db = None
        self.models = {}

        self.create_menu()
        self.create_interface()
        self.set_controls_enabled(False)

    def create_menu(self):
        menu = self.menuBar().addMenu("Menu")

        self.action_set_connection = QAction("Set connection", self)
        self.action_close_connection = QAction("Close connection", self)

        self.action_set_connection.triggered.connect(self.set_connection)
        self.action_close_connection.triggered.connect(self.close_connection)

        menu.addAction(self.action_set_connection)
        menu.addAction(self.action_close_connection)

    def create_interface(self):
        central = QWidget()
        root_layout = QVBoxLayout(central)

        controls = QGridLayout()

        self.bt1 = QPushButton('bt1 "SELECT name FROM sqlite_master"')
        self.combo_columns = QComboBox()
        self.combo_columns.setPlaceholderText('QComboBox "Columns"')

        self.bt2 = QPushButton('bt2 "Query2"')
        self.bt3 = QPushButton('bt3 "Query3"')

        controls.addWidget(self.bt1, 0, 0)
        controls.addWidget(QLabel("Выберите колонку sqlite_master:"), 0, 1)
        controls.addWidget(self.combo_columns, 0, 2)
        controls.addWidget(self.bt2, 1, 0)
        controls.addWidget(self.bt3, 1, 2)

        self.tabs = QTabWidget()
        self.tables = []

        for i in range(5):
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)

            table = QTableView()
            table.setAlternatingRowColors(True)
            table.setSelectionBehavior(QTableView.SelectRows)
            table.setEditTriggers(QTableView.NoEditTriggers)
            table.horizontalHeader().setStretchLastSection(True)

            tab_layout.addWidget(table)
            self.tabs.addTab(tab, f"Tab{i + 1}")
            self.tables.append(table)

        root_layout.addLayout(controls)
        root_layout.addWidget(self.tabs)

        self.setCentralWidget(central)

        self.bt1.clicked.connect(self.run_query_1)
        self.bt2.clicked.connect(self.run_query_2)
        self.bt3.clicked.connect(self.run_query_3)
        self.combo_columns.currentTextChanged.connect(self.run_column_query)

        self.statusBar().showMessage("Соединение с БД не установлено")

    def set_controls_enabled(self, enabled):
        self.bt1.setEnabled(enabled)
        self.bt2.setEnabled(enabled)
        self.bt3.setEnabled(enabled)
        self.combo_columns.setEnabled(enabled)

    def set_connection(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите SQLite базу данных",
            str(Path(__file__).resolve().parent),
            "SQLite database (*.db *.sqlite *.sqlite3);;All files (*.*)",
        )

        if not file_name:
            return

        self.close_connection(show_message=False)

        if QSqlDatabase.contains(self.CONNECTION_NAME):
            QSqlDatabase.removeDatabase(self.CONNECTION_NAME)

        self.db = QSqlDatabase.addDatabase("QSQLITE", self.CONNECTION_NAME)
        self.db.setDatabaseName(file_name)

        if not self.db.open():
            error = self.db.lastError().text()
            self.db = None
            QMessageBox.critical(
                self,
                "Ошибка подключения",
                f"Не удалось открыть базу данных:\n{error}",
            )
            return

        self.set_controls_enabled(True)
        self.statusBar().showMessage(f"Подключено: {file_name}")

        self.fill_columns_combo()

        self.execute_query("SELECT * FROM sqlite_master", tab_index=0)
        self.tabs.setCurrentIndex(0)

    def close_connection(self, show_message=True):
        self.combo_columns.blockSignals(True)
        self.combo_columns.clear()
        self.combo_columns.blockSignals(False)

        for table in self.tables:
            table.setModel(None)

        self.models.clear()
        self.set_controls_enabled(False)

        if self.db is not None:
            connection_name = self.db.connectionName()
            self.db.close()
            self.db = None

            if QSqlDatabase.contains(connection_name):
                QSqlDatabase.removeDatabase(connection_name)

        self.statusBar().showMessage("Соединение с БД закрыто")

        if show_message:
            QMessageBox.information(
                self,
                "Close connection",
                "Соединение с базой данных закрыто.\nТаблицы очищены.",
            )

    def fill_columns_combo(self):
        self.combo_columns.blockSignals(True)
        self.combo_columns.clear()

        query = QSqlQuery(self.db)
        if not query.exec_("PRAGMA table_info(sqlite_master)"):
            QMessageBox.warning(
                self,
                "Ошибка",
                "Не удалось получить колонки sqlite_master:\n"
                + query.lastError().text(),
            )
            self.combo_columns.blockSignals(False)
            return

        while query.next():
            column_name = query.value(1)
            if column_name:
                self.combo_columns.addItem(str(column_name))

        self.combo_columns.setCurrentIndex(-1)
        self.combo_columns.blockSignals(False)

    def execute_query(self, sql, tab_index):
        if self.db is None or not self.db.isOpen():
            QMessageBox.warning(
                self,
                "Нет соединения",
                "Сначала выберите Menu → Set connection.",
            )
            return False

        model = QSqlQueryModel(self)
        model.setQuery(sql, self.db)

        if model.lastError().isValid():
            QMessageBox.critical(
                self,
                "Ошибка SQL",
                f"Запрос:\n{sql}\n\nОшибка:\n{model.lastError().text()}",
            )
            model.deleteLater()
            return False

        self.models[tab_index] = model
        self.tables[tab_index].setModel(model)
        self.tables[tab_index].resizeColumnsToContents()
        self.tabs.setCurrentIndex(tab_index)
        return True

    def run_query_1(self):
        self.execute_query(
            "SELECT name FROM sqlite_master",
            tab_index=1,
        )

    def run_column_query(self, column_name):
        if not column_name:
            return

        allowed = {"type", "name", "tbl_name", "rootpage", "sql"}
        if column_name not in allowed:
            QMessageBox.warning(self, "Ошибка", "Недопустимое имя колонки.")
            return

        self.execute_query(
            f'SELECT "{column_name}" FROM sqlite_master',
            tab_index=2,
        )

    def run_query_2(self):
        self.execute_query(
            """
            SELECT type, COUNT(*) AS object_count
            FROM sqlite_master
            GROUP BY type
            ORDER BY type
            """,
            tab_index=3,
        )

    def run_query_3(self):
        self.execute_query(
            """
            SELECT name, type, tbl_name, sql
            FROM sqlite_master
            ORDER BY name
            """,
            tab_index=4,
        )

    def closeEvent(self, event):
        self.close_connection(show_message=False)
        event.accept()


def main():
    app = QApplication(sys.argv)

    window = SqlLabWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
