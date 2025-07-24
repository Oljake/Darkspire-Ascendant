# loading_status.py
class LoadingStatus:
    status = ""

    @classmethod
    def set_status(cls, new_status: str):
        cls.status = new_status

    @classmethod
    def get_status(cls) -> str:
        return cls.status
