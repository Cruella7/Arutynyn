import sys
from PyQt6.QtWidgets import QTableWidgetItem, QAbstractItemView, QLabel, \
    QVBoxLayout, QScrollArea, QWidget
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
import sqlite3
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загрузка пользовательского интерфейса из файла 'interface.ui'
        uic.loadUi('interface.ui', self)
        self.setFixedSize(1000, 600)
        #Соединение сигнала "clicked" кнопки pushButton_2 с методом show_admin_window
        self.pushButton_2.clicked.connect(self.show_admin_window)
        #Соединение сигнала "clicked" кнопки pushButton с методом show_minds_window
        self.pushButton.clicked.connect(self.show_minds_window)

    def show_admin_window(self):
        #Определение метода для отображения окна администратора.
        admin_window.show()

    def show_minds_window(self):
        #Вызов метода show() для отображения окна с информацией о разумах.
        minds_window.show()
        #Вызов метода table_view() для отображения таблицы в окне с информацией о разумах.
        minds_window.table_view()

class AdminWindow(QDialog):
    def __init__(self):
        super().__init__()
        # Загрузка пользовательского интерфейса из файла 'Adminn.ui'
        uic.loadUi('Adminn.ui', self)
        self.setFixedSize(1000, 600)
        # Соединение сигнала "clicked" кнопки vxod с методом auth
        self.vxod.clicked.connect(self.auth)

    # Определение метода для аутентификации администратора.
    def auth(self):
        # Получение введенного логина из виджета login и password
        login = self.login.text()
        password = self.password.text()

        # Проверка на ввод цифр, символов или пустых значений
        if not login or not password or not login.isalpha() or not password.isalnum():
            QMessageBox.critical(self, 'Ошибка', 'Введите корректный логин и пароль')
            return

        # Подключение к базе данных
        connection = sqlite3.connect('data.db')
        # Создание объекта курсора для выполнения SQL-запросов
        cursor = connection.cursor()
        # Выполнение SQL-запроса для выбора всех данных из таблицы 'admins'
        cursor.execute('SELECT * FROM admins')
        admins = cursor.fetchall()

        # Проверка соответствия введенного логина и пароля администратора в базе данных
        for logpas in admins:
            if logpas[0] == login and logpas[1] == password:
                return adminminds_window.show()

        QMessageBox.critical(self, 'Ошибка', 'Неверный логин или пароль')

class AdminMindsWindow(QDialog):
    def __init__(self):
        super().__init__()
        #Загрузка пользовательского интерфейса из файла 'AdminMinds.ui'
        uic.loadUi('AdminMinds.ui', self)
        self.setFixedSize(1000, 600)
        #Соединение сигнала "doubleClicked" таблицы tableView
        self.tableView.doubleClicked.connect(self.on_click)
        #Соединение сигнала "clicked" таблицы tableView
        self.tableView.clicked.connect(self.on_click_del_id)
        #Соединение сигнала "clicked" с кнопками
        self.pushButton_2.clicked.connect(self.on_click_del)
        self.pushButton.clicked.connect(self.on_click_add)
        self.id_del = -1
        #Вызов метода table_view для отображения данных в таблице при инициализации окна
        self.table_view()

    def on_click_add(self):
        empl_window.show()

    def on_click_del(self):
        # Устанавливаем соединение с базой данных 'data.db'
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        ## Выполняем SQL-запрос для удаления записи с указанным id из таблицы 'employees'
        cursor.execute(f'DELETE FROM employees WHERE id = {self.id_del}')
        ## Фиксируем изменения в базе данных
        connection.commit()
        cursor.close()
        connection.close()
        self.table_view()

    #Определение метода для отображения данных в таблице.
    def table_view(self):
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM employees')
        #Получаем все записи из результата запроса.
        employees = cursor.fetchall()
        #Устанавливаем количество строк в таблице равным количеству записей в базе данных.
        self.tableView.setRowCount(len(employees))
        #Устанавливаем количество столбцов в таблице равным 1.
        self.tableView.setColumnCount(1)
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger(0))
        header_item = QTableWidgetItem('Умы России')
        header_item.setFont(QFont('Arial', 24))
        self.tableView.setHorizontalHeaderItem(0, header_item)
        #Устанавливаем вид и размеры таблицы
        self.tableView.horizontalHeader().setDefaultSectionSize(1000)
        self.tableView.setStyleSheet(
            "QHeaderView::section { background-color:rgb(0, 0, 63); color:white} QTableWidget {"
            "background-color:rgb(0, 0, 63); color:white; font-size: 22px}QTableWidget "
            "QTableCornerButton::section {background-color: rgb(0, 0, 63);}")
        #Заполняем таблицу данными из базы данных.
        x = 0
        for name in employees:
            self.tableView.setItem(x, 0, QTableWidgetItem(name[1]))
            x += 1
    # Определение метода для получения id_del сотрудника по выбранному имени
    def on_click_del_id(self):
        # Получаем имя сотрудника из выбранной строки таблицы
        name = self.tableView.item(self.tableView.selectedItems()[0].row(), 0).text()
        # Устанавливаем соединение с базой данных 'data.db'
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # Выполняем SQL-запрос для получения id сотрудника по его имени
        cursor.execute(f'SELECT id FROM employees WHERE name = "{name}"')
        # Получаем результат запроса
        employees = cursor.fetchall()
        # Устанавливаем id_del для последующего удаления
        self.id_del = employees[0][0]

    # Определение метода для обработки события выбора сотрудника в таблице
    def on_click(self):
        # Глобальная переменная для хранения id администратора
        global id_admin
        # Получаем имя сотрудника из выбранной строки таблицы
        name_q = self.tableView.item(self.tableView.selectedItems()[0].row(), 0).text()
        # Устанавливаем соединение с базой данных 'data.db'
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # Выполняем SQL-запрос для получения id сотрудника по его имени
        cursor.execute(f'SELECT id FROM employees WHERE name = "{name_q}"')
        # Получаем результат запроса
        employees = cursor.fetchall()
        # Устанавливаем id администратора для последующего использования
        id_admin = employees[0][0]
        # Выполняем SQL-запрос для получения изображения сотрудника
        cursor.execute(f'SELECT img FROM employees WHERE name = "{name_q}"')
        # Получаем результат запроса и загружаем изображение в окно
        adminstati_window.load_image(cursor.fetchall()[0][0])
        # Отображаем окно с изображением и обновляем отображение таблицы
        adminstati_window.show()
        adminstati_window.table_view()

class Employees(QDialog):
    def __init__(self):
        super().__init__()
        # Загрузка интерфейса из файла employees.ui
        uic.loadUi('employees.ui', self)
        self.setFixedSize(400, 250)
        # Привязывается сигнал нажатия кнопки
        self.pushButton.clicked.connect(self.addemp)

    def addemp(self):
        # Получаются значения из полей ввода и сохраняются в переменные
        emp_name = self.lineEdit.text()
        emp_img = self.lineEdit_1.text()
        # Соединение с базой данных
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # Выполняется SQL-запрос для получения всех id из таблицы
        cursor.execute(f'SELECT id FROM employees')
        employees = cursor.fetchall()
        # Вычисляется новый id для нового сотрудника путем увеличения последнего id в таблице на 1
        emp_id = employees[-1][0] + 1
        # Выполняется SQL-запрос для вставки новой записи в таблицу с полученными значениями
        cursor.execute(f'INSERT INTO employees VALUES ({emp_id}, "{emp_name}", "{emp_img}")')
        connection.commit()
        cursor.close()
        connection.close()
        empl_window.close()
        minds_window.table_view()
        adminminds_window.table_view()

class AdminStatiWindow(QDialog):
    def __init__(self):
        super().__init__()
        # Загрузка интерфейса из файла AdminStati.ui
        uic.loadUi('AdminStati.ui', self)
        self.setFixedSize(1000, 600)
        # Инициализация отображения таблицы
        self.table_view()
        # Инициализация переменной для хранения выбранного заголовка
        self.id_del_st = ''
        # Привязка кнопки к методу удаления
        self.pushButton_2.clicked.connect(self.on_click_del)
        # Привязка кнопки к методу добавления
        self.pushButton.clicked.connect(self.on_click_add)
        # Привязка кнопки к методу закрытия окна
        self.pushButton_leave.clicked.connect(self.on_click_leave)

    # Метод для загрузки изображения и отображения его на виджете
    def load_image(self, file_name):
        # Создание объекта QPixmap из файла
        pixmap = QPixmap(file_name)
        pixmap = pixmap.scaled(300, 300)
        # Создание QLabel для отображения изображения
        self.label1 = QLabel(self)
        # Установка QPixmap в QLabel
        self.label1.setPixmap(pixmap)
        # Установка размеров QLabel
        self.label1.resize(300, 300)
        # Установка позиции QLabel в окне
        self.label1.move(600, 150)

    def on_click_leave(self):
        # Метод для закрытия окна
        adminstati_window.close()

    def on_click_add(self):
        # Метод для отображения article_window
        article_window.show()

    def on_click_del(self):
        # Метод для удаления статьи из базы данных
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM articles WHERE title = "{self.id_del_st}"')
        connection.commit()
        cursor.close()
        connection.close()
        # Перезагрузка отображения таблицы после удаления
        self.table_view()

    def show_minds_window(self):
        # Метод для закрытия окна
        adminstati_window.close()

    # Метод для отображения таблицы статей
    def table_view(self):
        # Установка соединения с базой данных
        connection = sqlite3.connect('data.db')
        # Создание курсора для выполнения SQL-запросов
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM articles WHERE id = {id_admin}')
        articles = cursor.fetchall()
        # Установка количества строк и столбцов в таблице
        self.tableView.setRowCount(len(articles))
        self.tableView.setColumnCount(1)
        self.tableView.setHorizontalHeaderItem(0, QTableWidgetItem('Статьи'))
        self.tableView.horizontalHeader().setDefaultSectionSize(500)
        # Запрет редактирования ячеек
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger(0))
        self.tableView.setStyleSheet(
            "QHeaderView::section { background-color:rgb(0, 0, 63); color:white} QTableWidget {"
            "background-color:rgb(0, 0, 63); color:white; font-size: 22px}QTableWidget "
            "QTableCornerButton::section {background-color: rgb(0, 0, 63);}")
        x = 0
        for title in articles:
            # Заполнение ячеек таблицы данными из базы данных
            self.tableView.setItem(x, 0, QTableWidgetItem(title[1]))
            x += 1
        # Привязка событий к таблице
        self.tableView.clicked.connect(self.on_click)
        self.tableView.doubleClicked.connect(self.on_double_click)

    def on_click(self):
        # Метод при клике на ячейку таблицы для получения выбранного заголовка
        self.id_del_st = self.tableView.item(self.tableView.selectedItems()[0].row(), 0).text()

    # Метод при двойном клике на ячейку таблицы для отображения stati_content_window
    def on_double_click(self):
        # Использование глобальной переменной для передачи заголовка статьи
        global title
        # Получение выбранного заголовка
        title = self.tableView.item(self.tableView.selectedItems()[0].row(), 0).text()
        # Отображение окна
        stati_content_window.show()
        # Вызов метода для отображения содержимого окна
        stati_content_window.show_label()

class Article(QDialog):
    def __init__(self):
        super().__init__()
        # Загружаем пользовательский интерфейс из файла 'article.ui'
        uic.loadUi('article.ui', self)
        self.setFixedSize(400, 400)
        # Связываем событие нажатия кнопки с методом addemp
        self.pushButton.clicked.connect(self.addemp)

    def addemp(self):
        # Получаем данные из виджетов
        title = self.lineEdit.text()
        content = self.textEdit.toPlainText()
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO articles VALUES ({id_admin}, "{title}", "{content}")')
        # Фиксируем изменения и закрываем соединение
        connection.commit()
        cursor.close()
        connection.close()
        article_window.close()
        # Обновляем таблицы в окнах adminstati_window и stati_window
        adminstati_window.table_view()
        stati_window.table_view()

class MindsWindow(QDialog):
    def __init__(self):
        super().__init__()
        # Загрузка интерфейса из файла Minds.ui
        uic.loadUi('Minds.ui', self)
        self.setFixedSize(1000, 650)
        # Инициализация отображения таблицы
        self.table_view()

    # Метод для отображения таблицы сотрудников
    def table_view(self):
        # Установка соединения с базой данных
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        # Установка количества строк и столбцов в таблице
        self.tableView.setRowCount(len(employees))
        self.tableView.setColumnCount(1)
        # Запрет редактирования ячеек
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger(0))
        self.tableView.setHorizontalHeaderItem(0, QTableWidgetItem('Умы России'))
        self.tableView.horizontalHeader().setDefaultSectionSize(1000)
        self.tableView.setStyleSheet(
            "QHeaderView::section { background-color:rgb(0, 0, 63); color:white} QTableWidget {"
            "background-color:rgb(0, 0, 63); color:white; font-size: 22px}QTableWidget "
            "QTableCornerButton::section {background-color: rgb(0, 0, 63);}")
        x = 0
        # Заполнение ячеек таблицы данными из базы данных
        for name in employees:
            self.tableView.setItem(x, 0, QTableWidgetItem(name[1]))
            x += 1
        # Привязка события клика по таблице к методу on_click
        self.tableView.clicked.connect(self.on_click)

    # Метод при клике на ячейку таблицы
    def on_click(self):
        # Использование глобальной переменной для передачи идентификатора сотрудника
        global id
        # Получение выбранного имени
        name = self.tableView.item(self.tableView.selectedItems()[0].row(), 0).text()
        # Установка соединения с базой данных
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT id FROM employees WHERE name = "{name}"')
        employees = cursor.fetchall()
        # Получение идентификатора сотрудника
        id = employees[0][0]
        # Выполнение SQL-запроса для получения изображения сотрудника и его отображение
        cursor.execute(f'SELECT img FROM employees WHERE name = "{name}"')
        stati_window.load_image(cursor.fetchall()[0][0])
        stati_window.show()
        # Обновление отображения таблицы в stati_window
        stati_window.table_view()

class StatiWindow(QDialog):
    def __init__(self, ):
        super().__init__()
        # Загрузка интерфейса из файла Stati.ui
        uic.loadUi('Stati.ui', self)
        self.setFixedSize(1000, 600)
        self.pushButton.clicked.connect(self.show_minds_window)

    def show_minds_window(self):
        stati_window.close()

    def load_image(self, file_name):
        #Загружает изображение из файла file_name
        pixmap = QPixmap(file_name)
        pixmap = pixmap.scaled(300, 300)
        #Отображение изображения на виджете
        self.label1 = QLabel(self)
        self.label1.setPixmap(pixmap)
        self.label1.resize(300, 300)
        #Размер и положение виджета
        self.label1.move(600, 150)

    def table_view(self):
        # Установка соединения с базой данных SQLite
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # Выполнение SQL-запроса для получения статей
        cursor.execute(f'SELECT * FROM articles WHERE id = {id}')
        articles = cursor.fetchall()
        # Установка количества строк и столбцов в таблице
        self.tableView.setRowCount(len(articles))
        self.tableView.setColumnCount(1)
        self.tableView.setHorizontalHeaderItem(0, QTableWidgetItem('Статьи'))
        self.tableView.horizontalHeader().setDefaultSectionSize(500)
        # Запрет редактирования ячеек
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger(0))
        self.tableView.setStyleSheet(
            "QHeaderView::section { background-color:rgb(0, 0, 63); color:white} QTableWidget {"
            "background-color:rgb(0, 0, 63); color:white; font-size: 22px}QTableWidget "
            "QTableCornerButton::section {background-color: rgb(0, 0, 63);}")
        x = 0
        # Заполнение таблицы
        for title in articles:
            self.tableView.setItem(x, 0, QTableWidgetItem(title[1]))
            x += 1
        self.tableView.clicked.connect(self.on_click)

    def on_click(self):
        global title
        # Получение текста выбранной ячейки таблицы
        title = self.tableView.item(self.tableView.selectedItems()[0].row(), 0).text()
        stati_content_window.show()
        # Вызов метода для отображения контента в окне
        stati_content_window.show_label()

class ScrollLabel(QScrollArea):

    #Конструктор для инициализации виджета прокручиваемой области
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # возможность изменения размера виджета
        self.setWidgetResizable(True)

        # Устанавливается content в качестве виджета прокручиваемой области
        content = QWidget(self)
        self.setWidget(content)

        # Создается вертикальное расположение виджетов
        lay = QVBoxLayout(content)

        self.label = QLabel(content)
        self.label.setStyleSheet('color: white; font-size: 22px; background-color: rgb(0, 0, 63);border:none;')
        content.setStyleSheet('color: white; background-color: rgb(0, 0, 63);border:none;')

        # Устанавливается выравнивание текста
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Включается перенос слов в метке
        self.label.setWordWrap(True)

        # Метка добавляется в вертикальное расположение
        lay.addWidget(self.label)

    # Установка текста в label
    def setText(self, text):
        self.label.setText(text)


class StatiContentWindow(QDialog):
    def __init__(self):
        super().__init__()
        # Загрузка интерфейса из файла Stati_content.ui
        uic.loadUi('Stati_content.ui', self)
        self.setFixedSize(1000, 600)
        # Привязывается сигнал нажатия кнопки
        self.pushButton.clicked.connect(self.show_minds_window)
        self.label1 = ScrollLabel(self)


    def show_label(self):
        #Соединение с базой данных
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT content FROM articles WHERE title = "{title}"')
        texti = cursor.fetchall()
        # Полученный текст статьи устанавливается в виджет с помощью метода
        self.label1.setText(texti[0][0])
        self.label1.setGeometry(50, 50, 900, 500)
    # Закрытие окна
    def show_minds_window(self):
        stati_content_window.close()

# Проверка, запущен ли скрипт напрямую (а не импортирован как модуль)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Инициализируем некоторые переменные, используемые в приложении
    id = -1
    id_admin = -1
    title = ''
    # Создаем экземпляры различных окон нашего приложения
    window = MainWindow()
    admin_window = AdminWindow()
    minds_window = MindsWindow()
    stati_window = StatiWindow()
    article_window = Article()
    stati_content_window = StatiContentWindow()
    adminminds_window = AdminMindsWindow()
    adminstati_window = AdminStatiWindow()
    empl_window = Employees()

    # Показываем главное окно
    # Завершаем выполнение приложения при закрытии главного окна
    window.show()
    sys.exit(app.exec())
