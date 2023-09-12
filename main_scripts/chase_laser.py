import interfaces
import cv2


class ChaseLaser(interfaces.ChaseLaser):
    """
    Класс ChaseLaser:
    Класс, который отвечает за функцию распознавания лазера и перемещения за ним.
    Использует компьютерное зрение, пороговую обработку.
    """
    def __init__(self, camera: cv2.typing.MatLike) -> None:
        """
        Инициализация класса
        :param camera: Объект класса cv2.typing.MatLike, который можно получить, использовав метод cv2.VideoCapture().read()
        """

        # Инициализация переменных
        self.__camera = camera
        self.__action = ''
        self.__iSee = False
        self.__controlX = 0.0

    def __preparation(self) -> None:
        """
        Обработка кадра.
        """
        # Получаем разрешение кадра
        height, width = self.__camera.shape[0:2]

        # Преобразование кадра
        hsv = cv2.cvtColor(self.__camera, cv2.COLOR_BGR2HSV)

        # Пороговая обработка
        bin1 = cv2.inRange(hsv, (0, 60, 70), (10, 255, 255))
        bin2 = cv2.inRange(hsv, (160, 60, 70), (179, 255, 255))
        binary = bin1 + bin2

        # Контуры выделенных областей
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            # Находим наибольший контур
            maxc = max(contours, key=cv2.contourArea)

            # Получаем моменты этого контура и находим координаты центра
            moments = cv2.moments(maxc)
            if moments["m00"] > 10:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])

                iSee = True
                # Находим отклонение найденного объекта от центра кадра и нормализуем его
                controlX = 2 * (cx - width / 2) / width


    def __get_action(self) -> None:
        """
        Метод получение действия, в зависимости от координат объекта.
        """
        if self.__iSee:
            self.__action = 'F'
        else:
            self.__action = 'S'

        # если мы видим какие-то отклонения, то мы разворачиваемся в центральную часть
        if self.__controlX < -0.3:
            self.__action = 'R'
        if self.__controlX > 0.3:
            self.__action = 'L'


    def __move(self, serial: interfaces.Serial) -> None:
        """
        Отправление сигнала по serial порту для передвижения.
        :param serial: Объект класса interfaces.Serial, отвечает за Serial COM порт.
        """
        serial.write(self.__action)

    def chase(self):
        """
        Основной метод класса, при вызове которого выполнятся все операции в нужном порядке.
        """
        self.__preparation()
        self.__get_action()
        self.__move()
