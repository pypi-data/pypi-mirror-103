import zmail
from functools import wraps
import time
import datetime


class ENotification:
    """
    This is a decorator class
    """

    def __init__(self, send_from: str = "", password="", send_to: str = "") -> None:
        """
        send the mail from `send_from` to `send_to`. Note: the password is send_from's password.
        """
        self.send_from = send_from
        self.password = password
        self.send_to = send_to
        if self.send_to == "":
            self.send_to = self.send_from

    def _notify(self, start_time:str, end_time:str, func):
        def ts2str(timestamp):
            time_array = time.localtime(timestamp)
            return time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        
        cost_second = int(end_time - start_time)
        cost = str(datetime.timedelta(seconds=cost_second))
        start = ts2str(start_time)
        end = ts2str(end_time)
        server = zmail.server(self.send_from, self.password)
        server.send_mail(
            self.send_to,
            {
                "subject": "This is a notification from enotification!",
                "content_text": f"Your function {func.__name__} is finished!\nStart time: {start}\nEnd time: {end}\nTime cost: {cost}!",
            },
        )

    def __call__(self, func) -> None:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            self._notify(start_time, end_time, func)

        return wrapper