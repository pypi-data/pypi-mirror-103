import enum
import datetime
import logging


class IntervalChoice(enum.Enum):
    BY_TIME = 0
    BY_STEP = 1


class Interval:
    _interval_type: IntervalChoice = None
    _interval_value: int = None

    _last_value = None

    @property
    def interval_type(self):
        return self._interval_type

    @property
    def interval_value(self):
        return self._interval_value

    @classmethod
    def create_interval(cls, step=None, time=None):
        assert bool(step) != bool(time), "could only as time or step interval"
        if step:
            r = Interval()
            r._interval_type = IntervalChoice.BY_STEP
            r._interval_value = step
            r._last_value = 0
        else:
            r = Interval()
            r._interval_type = IntervalChoice.BY_TIME
            r._interval_value = time
            r._last_value = 0
        return r

    def reached_threshold(self, current_ts=None, current_step=None, reset=True) -> bool:
        logging.info("type(current_ts): %s", type(current_ts))
        logging.info("current_ts: %s", current_ts)
        logging.info("type(current_step): %s", type(current_step))
        logging.info("current_step: %s", current_step)
        logging.info("type(last_value): %s", type(self._last_value))
        logging.info("last_value: %s", self._last_value)
        logging.info("type(interval_value): %s", type(self.interval_value))
        logging.info("interval_value: %s", self.interval_value)
        if self.interval_type == IntervalChoice.BY_TIME:
            logging.info("interval_type is bytime.")
            if self._last_value + self.interval_value <= current_ts:
                if reset:
                    self._last_value = current_ts
                return True
        elif self.interval_type == IntervalChoice.BY_STEP:
            logging.info("interval_type is bystep.")
            logging.info("last_value + interval_value: %s, current_step: %s", self._last_value + self.interval_value, current_step)
            if self._last_value + self.interval_value <= current_step:
                if reset:
                    self._last_value = current_step
                return True
        return False

    def __str__(self):
        return "Interval %s : %s" % (
            "step" if self.interval_type == IntervalChoice.BY_STEP else "time",
            self.interval_value
        )
