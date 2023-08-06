
class ListPort:
    """
    Класс для проверки корректности номера порта.
    """
    def __init__(self, name):
        self.name = '_' + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not (1024 <= value <= 65535):
            raise ValueError("Порт должен быть от 1024 до 65535! Exit!")
        setattr(instance, self.name, value)
