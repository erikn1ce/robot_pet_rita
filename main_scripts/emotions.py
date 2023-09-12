import interfaces
import cv2
import threading
import time


class ShowEmotions(interfaces.ShowEmotions):
    """
    Класс ShowEmotions:
    Класс, который отвечает за показ эмоций на экране.
    Использует opencv для отображения заранее заготовленных эмоций.
    """
    def __init__(self, emotion_folder: str):
        """
        Инициализация объекта класса.
        :param emotion_folder: Путь к директории с эмоциями
        """
        self.__folder = emotion_folder
        self.__current_emotion = ''
        self.__speed = 0
        self.change_emotion('blink.mp4')
        self.__video_capture = cv2.VideoCapture(self.__current_emotion)

    def show(self) -> None:
        """
        Основной метод.
        Отображение эмоции.
        """
        # Чтение видео с выбранной эмоцией
        success, frame = self.__video_capture.read()

        # Если успешно, выводит изображение
        if success:
            cv2.imshow("Image", frame)
        if cv2.waitKey(self.__speed) & 0xFF == ord('q'):
            print('end')

    def change_emotion(self, emotion: str, speed=60) -> None:
        """
        Метод для смены эмоции.
        :param emotion: Строка, название эмоции, на которую необходимо сменить нынешнюю.
        :param speed: Скорость смены кадров в миллисекундах.
        """
        self.__current_emotion = self.__folder + emotion
        self.__speed = speed
        self.__video_capture = cv2.VideoCapture(self.__current_emotion)


show = ShowEmotions('emojis/')


'''def show_():
    while True:
        show.show()


def main():
    thread = threading.Thread(target=show_)
    thread.start()
    time.sleep(5)
    show.change_emotion('sadblink.mp4')
    show.show()


if __name__ == '__main__':
    main()

Example of usage
    
'''