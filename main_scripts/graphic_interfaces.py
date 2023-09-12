import interfaces
import sys
import cv2
import config
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, \
    QStackedWidget, QGridLayout


class GraphicInterfaces(interfaces.GraphicInterfaces):
    """
    Класс GraphicInterfaces:
    Главный управляющий класс.
    Регулирует работу всех графических интерфейсов, переключение между ними и другие операции.
    Также является главным окном приложения, содержит переменные для взаимодействия с основным кодом.
    """

    def __init__(self):
        """
        Инициализация объекта класса.
        """

        # Инициализация графики и самого виджета
        super().__init__()
        self.__init_ui()

        # Инициализация переменных
        self.isStart = False

    def __init_ui(self):
        """
        Инициализация интерфейсов, настройка окна приложения.
        В коде создается словарь интерфейсов, для поиска их по имени.
        Также создается объект класса QStackedWidget, для управления видимым интерфейсом.
        """

        # Настройка основных параметров окна
        self.setGeometry(100, 100, 1000, 550)
        self.setWindowTitle("Main Window")
        self.setFixedSize(1000, 550)

        # Создание переменных для каждого интерфейса
        self.__name_interface = NameInterface(self)
        self.__picture_interface = PictureInterface(self, 0)
        self.__like_interface = LikeInterface(self)

        # Создание словаря всех интерфейсов, для удобного взаимодействия
        self.__interfaces = {'name': self.__name_interface,
                             'picture': self.__picture_interface,
                             'like': self.__like_interface}

        # Создание виджета для переключения между окнами
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Добавление в основной виджет всех интерфейсов
        self.stacked_widget.addWidget(self.__interfaces['name'])
        self.stacked_widget.addWidget(self.__interfaces['like'])
        self.stacked_widget.addWidget(self.__interfaces['picture'])

        # Установка видимого интерфейса в основной виджет
        self.stacked_widget.setCurrentWidget(self.__interfaces['name'])

    def change_interface(self, widget: QWidget) -> None:
        """
        Изменение основного видимого интерфейса.
        Метод не возвращает значений.
        :param widget: Объект класса QWidget, интерфейс, на который поменяется нынешний.
        """
        self.stacked_widget.setCurrentWidget(widget)

    def get_interface_by_name(self, name: str):
        """
        Получение интерфейса по его имени.
        :param name: Имя интерфейса, по которому осуществляется поиск.
        :return interface: Объект одного из классов, описывающих интерфейсы, если нет объекта с таким именем, вернется None.
        """
        return self.__interfaces[name] if self.__interfaces[name] else None


class NameInterface(QWidget):
    """
    Класс NameInterface:
    Шаблон окна для ввода имени с виртуальной клавиатуры.
    """

    def __init__(self, graphic_interfaces: GraphicInterfaces):
        """
        Инициализация объекта класса.
        :param graphic_interfaces: Объект класса GraphicInterfaces, для взаимодействия с другими интерфейсами и управления основным окном.
        """

        # Инициализация шрифта
        self.bold_font = QFont()
        self.bold_font.setPointSize(20)
        self.bold_font.setBold(True)

        # Инициализация переменных
        self.graphic_interfaces = graphic_interfaces

        # Инициализация графики и самого виджета
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Инициализация графики, виджетов и их расстановка на экране.
        Создание виртуальной клавиатуры и ее размещение на экране.
        """

        # Инициализация надписи заголовка
        self.label = QLabel('Name', parent=self)
        self.label.setFont(self.bold_font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(350, 0, 300, 50)

        # Создание layout для удобного размещения компонентов
        self.layout = QVBoxLayout()

        # Создание сетки для размещения кнопок клавиатуры
        grid_layout = QGridLayout()

        # Создание кнопок для клавиш
        buttons = [
            'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х',
            'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э',
            'я', 'ч', 'с', 'м', 'и', 'т', 'ь',
            'Backspace',
            'Enter'
        ]

        # Настройка клавиш
        row, col = 0, 0
        for button_text in buttons:
            if button_text == 'Backspace':
                button = QPushButton(button_text)
                button.setFixedHeight(40)
                button.clicked.connect(self.onBackspaceClick)
                grid_layout.addWidget(button, row, col, 1, 2)  # Занимаем две ячейки для кнопки Backspace
                col += 2
            elif button_text == 'Enter':
                button = QPushButton(button_text)
                button.setFixedHeight(40)
                button.clicked.connect(self.onEnterClick)
                grid_layout.addWidget(button, row, col, 1, 2)  # Занимаем две ячейки для кнопки Enter
                col += 2
            else:
                button = QPushButton(button_text)
                button.setFixedHeight(40)
                button.clicked.connect(self.onButtonClick)
                grid_layout.addWidget(button, row, col)
                col += 1

            if col > 10:
                col = 0
                row += 1

        # Поле для отображения текста
        self.text_edit = QLineEdit()
        self.layout.addWidget(self.text_edit)
        self.layout.addLayout(grid_layout)  # Добавляем сетку кнопок после поля ввода

        self.setLayout(self.layout)

    def onButtonClick(self):
        """
        Обработка нажатия на кнопку.
        При нажатии на кнопку в поле ввода добавится буква, на кнопку которой вы нажали.
        """

        button = self.sender()
        text = button.text()
        current_text = self.text_edit.text()
        self.text_edit.setText(current_text + text)

    def onBackspaceClick(self):
        """
        Обработка нажатия на кнопку Backspace.
        При нажатии на кнопку в поле ввода удалится последний символ, если оно не пусто, иначе ничего не произойдет.
        """

        current_text = self.text_edit.text()
        if current_text:
            self.text_edit.setText(current_text[:-1])

    def onEnterClick(self):
        """
        Обработка нажатия на кнопку Enter.
        При нажатии на кнопку в словарь из файла конфигурации names запишется новое значение типа: {порядковый номер: Имя}, где "Имя" это текст из поля ввода.
        Также значение переменной count_names из файла конфигурации увеличивается на 1.
        """

        current_text = self.text_edit.text()
        config.names.update({config.count_names: current_text.capitalize()})
        config.count_names += 1
        self.next()

    def next(self):
        """
        Запуск интерфейса создания фотографии
        Для реализации данной функции используется graphic_interfaces и методы взаимодействия с другими интерфейсами.
        Сначала находится интерфейс с именем "picture".
        Далее текущий видимый интерфейс изменяется на найденный.
        """
        interface = self.graphic_interfaces.get_interface_by_name('picture')
        self.graphic_interfaces.change_interface(interface)


class PictureInterface(QWidget):
    """
    Класс PictureInterface:
    Шаблон окна для создания фотографии, которая будет использоваться для распознавания лица
    """

    def __init__(self, graphic_interfaces: GraphicInterfaces, camera_index: int):
        """
        Инициализация объекта класса.

        :param graphic_interfaces: Объект класса GraphicInterfaces, для взаимодействия с другими интерфейсами и управления основным окном.
        :param camera_index: camera_index: int - Целое число, индекс камеры для метода cv2.VideoCapture()
        """

        # Инициализация переменных
        self.graphic_interfaces = graphic_interfaces
        self.__camera_index = camera_index
        self.video_capture = cv2.VideoCapture(self.__camera_index)

        # Инициализация виджета
        super().__init__()

        # Инициализация графики
        self.init_ui()

    def init_ui(self):
        """
        Инициализация графики, виджетов и их расстановка на экране.
        """
        # Настройка изображения с камеры
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Инициализация виджетов надписей и кнопок
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.time_label = QLabel(self)
        self.time_label.setAlignment(Qt.AlignCenter)

        self.label = QLabel('Picture', parent=self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, 300, 50)

        self.button_photo = QPushButton('Take photo', parent=self)
        self.button_photo.setGeometry(100, 500, 300, 50)
        self.button_photo.clicked.connect(self.start)

        self.button_name = QPushButton('Change name', parent=self)
        self.button_name.setGeometry(600, 500, 300, 50)
        self.button_name.clicked.connect(self.prev)

        # Инициализация layout, для удобного размещения виджетов и добавление всех объектов в него
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.label)
        layout.addWidget(self.button_photo)
        layout.addWidget(self.button_name)
        self.setLayout(layout)

        # Инициализация таймера, для отображения видео с камеры
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Присваивание времени фотографии и камеры
        self.start_programm()

    def start_programm(self):
        """
        Присваивание времени фотографии и камеры.
        Функция вызывается при вызове данного интерфейса.
        """
        # Инициализация переменных
        self.timer_duration = 5
        self.remaining_time = 5
        self.video_capture = cv2.VideoCapture(self.__camera_index)

        self.update_time_label()

    def update_frame(self):
        """
        Обновление кадра.
        Метод, который вызывается при каждом такте таймера QTimer,
        что позволяет постоянно получать изображение и вести обратный отсчет.
        """

        # Получение кадра с камеры
        ret, frame = self.video_capture.read()
        if ret:
            # Преобразования изображения
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w

            # Загрузка изображения на экран
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pixmap)

            # Обратный отсчет
            self.remaining_time -= 0.03
            self.update_time_label()

            # Проверка осталось ли еще время, если нет - закрыть окно
            if self.remaining_time <= 0:
                self.close()

    def update_time_label(self):
        """
        Обновления надписи остатка времени.
        """

        time_str = QTime(0, 0).addSecs(int(self.remaining_time)).toString("mm:ss")
        self.time_label.setText(f"Time Left: {time_str}")

    def close(self):
        """
        Метод, который вызывается при закрытии окна.
        Для реализации функции переключения интерфейса используется graphic_interfaces и методы взаимодействия с другими интерфейсами.
        В первую очередь находится интерфейс с именем "like".
        После того, как интерфейс найден, текущий видимый интерфейс изменяется на найденный.
        """

        # Чтение кадра с камеры
        success, frame = self.video_capture.read()

        if success:
            # Запись кадра в файл с индивидуальным порядковым номером
            cv2.imwrite(f"dataset/{config.count_names-1}.jpg", frame)
            print("Successfully saved")

        # Закрытие всех окон opencv
        self.video_capture.release()
        cv2.destroyAllWindows()

        # Остановка таймера
        self.timer.stop()

        # Переключение на следующий интерфейс
        interface = self.graphic_interfaces.get_interface_by_name('like')
        interface.display_image()
        self.graphic_interfaces.change_interface(interface)

    def start(self):
        """
        Метод для старта таймера, чтобы начиналось отображения камеры и обратный отсчет.
        """

        self.timer.start(30)

    def prev(self):
        """
        Метод для изменения имени.
        Удаляется последний добавленный объект в словарь.
        Находится интерфейс с именем "name".
        Задается значение пустой строки для поля ввода в полученном интерфейсе, чтобы не было видно предыдущего имени.
        Далее следует замена текущего интерфейса на новый.
        """
        config.names.pop(config.count_names-1)
        config.count_names -= 1
        interface = self.graphic_interfaces.get_interface_by_name('name')
        interface.text_edit.setText('')
        self.graphic_interfaces.change_interface(interface)


class LikeInterface(QWidget):
    """
    Класс LikeInterface:
    Шаблон окна для показа получившегося фото.
    Если фото не понравилось, пользователь сможет сделать его еще раз.
    Если пользователя все устраивает, основной код начнет работу
    """

    def __init__(self, graphic_interfaces: GraphicInterfaces):
        """
        Инициализация объекта класса.

        :param graphic_interfaces: Объект класса GraphicInterfaces, для взаимодействия с другими интерфейсами и управления основным окном.
        """
        # Инициализация шрифта
        self.bold_font = QFont()
        self.bold_font.setPointSize(20)
        self.bold_font.setBold(True)

        # Инициализация переменных
        self.graphic_interfaces = graphic_interfaces
        self.__image_path = ''
        self.__image = None

        # Инициализация графики и самого виджета
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Инициализация графики, виджетов и их расстановка на экране.
        """

        # Инициализация элемента надписи заголовка
        self.label = QLabel('Like', parent=self)
        self.label.setFont(self.bold_font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, 300, 50)

        # Инициализация элемента показа фото
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        # Инициализация кнопки Да
        self.button_yes = QPushButton('Yes', parent=self)
        self.button_yes.setGeometry(100, 500, 300, 50)
        self.button_yes.clicked.connect(self.next)

        # Инициализация кнопки Нет
        self.button_no = QPushButton('No', parent=self)
        self.button_no.setGeometry(600, 500, 300, 50)
        self.button_no.clicked.connect(self.prev)

    def next(self):
        """
        Запуск основного кода.
        Изменение флага на значение True.
        """
        self.graphic_interfaces.isStart = True
        config.save()
        print('Saved!')

    def prev(self):
        """
        Переход на предыдущий интерфейс, для повторного создания фотографии.
        Для реализации функции переключения интерфейса используется graphic_interfaces и методы взаимодействия с другими интерфейсами.
        В первую очередь находится интерфейс с именем "picture".
        После того, как интерфейс найден, текущий видимый интерфейс изменяется на найденный.
        """
        interface = self.graphic_interfaces.get_interface_by_name('picture')
        interface.start_programm()
        self.graphic_interfaces.change_interface(interface)

    def display_image(self):
        """
        Отображения фото на экране.
        """

        # Загрузка фото
        print(config.count_names)
        self.__image_path = f'dataset/{config.count_names-1}.jpg'
        self.__image = cv2.imread(self.__image_path)

        # Если изображение существует
        if self.__image is not None:
            # Преобразования изображения
            rgb_image = cv2.cvtColor(self.__image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w

            # Загрузка изображения на экран
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pixmap)


if __name__ == '__main__':
    config.load()
    app = QApplication(sys.argv)
    window = GraphicInterfaces()
    window.show()
    sys.exit(app.exec_())
