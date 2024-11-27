from random import randint
from .abstract_use_case import AbstractLoginUseCase


class LoginUseCase(AbstractLoginUseCase):
    def match_email_to_id(self, email) -> str:
        email_to_user_id = {
            "liuyimeng01@gmail.com": 21,
            "gabrielezrathompson@gmail.com": 1,
            "chongwan.w@gmail.com": 4,
            "benrockehenderson@gmail.com": 3,
            "jennifer.r.chiou@gmail.com": 95,
            "callum.sharrock@gmail.com": 0,
            "kiarashsotoudeh@gmail.com": 10,
        }
        if email in email_to_user_id.keys():
            user_id = email_to_user_id[email]
        else:
            user_id = randint(0, 99)

        return str(user_id)
