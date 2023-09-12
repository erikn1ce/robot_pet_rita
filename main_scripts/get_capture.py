import interfaces
import cv2


class GetCapture(interfaces.GetCapture):
    """
    Класс GetCapture:
    Класс, который отвечает за получение кадра с камеры.
    Использует для упрощения получения изображения с камеры.
    """
    def __init__(self, index_of_camera: int):
        """
        Инициализация объекта класса.
        :param index_of_camera: Индекс камеры, который используется в методе cv2.VideoCapture().
        """
        self.__index = index_of_camera
        self.__camera = cv2.VideoCapture(self.__index)

    def read_capture(self) -> cv2.typing.MatLike:
        """
        Основной метод класса.
        Чтение камеры и возвращение текущего кадра.
        :return frame: Объект класса cv2.typing.MatLike, текущий кадр.
        """
        success, frame = self.__camera.read()
        if success:
            return frame
