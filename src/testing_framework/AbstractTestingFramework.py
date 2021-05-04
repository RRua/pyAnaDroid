from abc import ABC, abstractmethod


class AbstractTestingFramework(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def execute_test(self, w_unit, timeout=None):
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def install(self):
        pass

    @abstractmethod
    def uninstall(self):
        pass