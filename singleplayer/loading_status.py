class LoadingStatus:
    _status = "Loading..."

    @classmethod
    def set_status(cls, text):
        cls._status = text

    @classmethod
    def get_status(cls):
        return cls._status