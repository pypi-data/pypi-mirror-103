import xdl
import datetime
import logging

from xdl.python.framework.session import Hook
from xdl.python.training.training_utils import get_global_step


class XdlMetricsHook(Hook):
    def __init__(
        self, ts_tensor, other_tensors, collect_interval, log_interval, sinker,
    ):
        super(XdlMetricsHook, self).__init__()
        self._names = []
        self._values = []
        self._collect_interval = collect_interval
        self._log_interval = log_interval
        self._ts_tensor = ts_tensor
        self._other_tensors = []
        self._sinker = sinker
        self._lstep = 0

        logging.info(
            "create metrics interval: %s, log_interval: %s"
            % (self._collect_interval, self._log_interval)
        )

        logging.info("[XdlMetricsHook] init 1")
        for val in xdl.get_all_metrics():
            self._names.append(val.name)
            self._values.append(val.value)

        logging.info("[XdlMetricsHook] init 2")
        for name, tensor in other_tensors:
            self._names.append(name)
            self._values.append(tensor)
        logging.info("[XdlMetricsHook] init 3")

    def _p95(self, ts_tensor_value, key=lambda x: x):
        return sorted(ts_tensor_value, key=key)[
            int(len(ts_tensor_value) * 0.95)
        ]

    def before_run(self, v):
        logging.info("[XdlMetricsHook] before run 1")
        a1 = [get_global_step().value]
        logging.info("[XdlMetricsHook] before run 2")
        a2 = [self._ts_tensor]
        logging.info("[XdlMetricsHook] before run 3")
        a3 = self._values
        logging.info("[XdlMetricsHook] before run 4")
        # return [get_global_step().value] + [self._ts_tensor] + self._values
        return a1 + a2 + a3

    def after_run(self, v):
        self._lstep += 1
        logging.info("[XdlMetricsHook] type(v): %s", type(v))
        # logging.info("[XdlMetricsHook] v: %s", v)
        current_step, sample_ts_value = v[0], v[1]
        logging.info("[XdlMetricsHook] type(current_step): %s", type(current_step))
        logging.info("[XdlMetricsHook] current_step: %s", current_step)
        if len(sample_ts_value) == 0:
            logging.info("len(sample_ts_value) is 0")
            return
        logging.info("[XdlMetricsHook] len(sample_ts_value): %d", len(sample_ts_value))
        logging.info("[XdlMetricsHook] after run 1")

        # anchored ts 为这批样本锚定的时间戳，选取95分位样本作为代表
        anchor_ts = self._p95(sample_ts_value).item()
        logging.info("[XdlMetricsHook] anchor_ts: %s", str(anchor_ts))
        current_step = current_step.item()

        logging.info("[XdlMetricsHook] after run 2")
        logging.info("[XdlMetricsHook] after run names: %s", self._names)
        logging.info("[XdlMetricsHook] after run v: %s", v[2:])
        if self._sinker is not None and xdl.get_task_index() == 0:
            if self._collect_interval.reached_threshold(
                current_ts=anchor_ts, current_step=current_step
            ):
                logging.info("[XdlMetricsHook] after run call_sinker")
                self._sinker(
                    ts=datetime.datetime.now(),
                    metrics=zip(self._names, v[2:]),
                    sample_ts=anchor_ts,
                    step=current_step,
                )
        else:
            logging.info("[XdlMetricsHook] after run type(sinker): %s", type(self._sinker))
            logging.info("[XdlMetricsHook] after run get_task_index: %d", xdl.get_task_index())
        logging.info("[XdlMetricsHook] after run 3")

        if self._log_interval.reached_threshold(
            current_ts=anchor_ts, current_step=current_step
        ):
            ts_str = ",".join(
                [
                    "%s:%s" % (name, value)
                    for name, value in zip(self._names, v[2:])
                ]
            )
            logging.info(
                "ts:%s, lstep:%d, gstep:%s, sample_ts:%d\t%s"
                % (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s"),
                    self._lstep,
                    current_step,
                    anchor_ts,
                    ts_str,
                )
            )
        else:
            logging.info(
                "Not reached_threshold"
            )
        logging.info("[XdlMetricsHook] after run 4")

    def end(self):
        logging.info("[XdlMetricsHook] end 1")
        if self._sinker is not None:
            logging.info("[XdlMetricsHook] end 2")
            self._sinker.close()
