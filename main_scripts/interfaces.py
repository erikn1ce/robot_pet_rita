from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QMainWindow, QWidget
import cv2

'''
Интерфейсы для всех функций и методов, используемых в проекте
'''


class Serial(ABC):
    @abstractmethod
    def __init__(self, port: str):
        pass

    @abstractmethod
    def write(self, data: str) -> None:
        pass

    @abstractmethod
    def read(self) -> str:
        pass


class RecognizeSpeech(ABC):
    @abstractmethod
    def __init__(self, model_name: str):
        pass

    @abstractmethod
    def listen(self):
        pass

    @abstractmethod
    def recognize(self) -> None:
        pass


class SynthesisSpeech(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def synthesis(self, phrase: str) -> None:
        pass


class GetCapture(ABC):
    @abstractmethod
    def __init__(self, index_of_camera: int):
        pass

    @abstractmethod
    def read_capture(self) -> cv2.typing.MatLike:
        pass


class FaceRecognition(ABC):
    @abstractmethod
    def __init__(self, index_camera: int, dataset: str):
        pass

    @abstractmethod
    def recognize(self) -> None:
        pass

    @abstractmethod
    def findEncodings(self):
        pass





class ChaseLaser(ABC):
    @abstractmethod
    def __init__(self, camera: cv2.typing.MatLike) -> None:
        pass

    @abstractmethod
    def __preparation(self) -> None:
        pass

    @abstractmethod
    def __get_action(self) -> None:
        pass

    @abstractmethod
    def __move(self, serial: Serial) -> None:
        pass

    @abstractmethod
    def chase(self) -> None:
        pass


class ChaseBall(ABC):
    @abstractmethod
    def __init__(self, camera: cv2.typing.MatLike) -> None:
        pass

    @abstractmethod
    def preparation(self) -> None:
        pass

    @abstractmethod
    def get_action(self) -> None:
        pass

    @abstractmethod
    def move(self, serial: Serial) -> None:
        pass


class ChaseMouse(ABC):
    @abstractmethod
    def __init__(self, camera: cv2.typing.MatLike) -> None:
        pass

    @abstractmethod
    def preparation(self) -> None:
        pass

    @abstractmethod
    def get_action(self) -> None:
        pass

    @abstractmethod
    def send(self, serial: Serial) -> None:
        pass




class ShowEmotions(ABC):
    @abstractmethod
    def __init__(self, emotion_folder: str):
        pass

    @abstractmethod
    def show(self) -> None:
        pass

    @abstractmethod
    def change_emotion(self, emotion: str, speed: int) -> None:
        pass


class GraphicInterfaces(QMainWindow):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def __init_ui(self) -> None:
        pass

    @abstractmethod
    def change_interface(self, widget: QWidget) -> None:
        pass

    @abstractmethod
    def get_interface_by_name(self, name: str):
        pass

