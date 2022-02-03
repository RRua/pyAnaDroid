import os
import time

from anadroid.Types import TESTING_FRAMEWORK, PROFILER
from anadroid.testing_framework.AbstractTestingFramework import AbstractTestingFramework
from anadroid.testing_framework.work.MonkeyWorkUnit import MonkeyWorkUnit
from anadroid.testing_framework.work.WorkLoad import WorkLoad
from anadroid.utils.Utils import get_resources_dir
from manafa.utils.Logger import log, LogSeverity


#DEFAULT_RES_DIR = "resources/testingFrameworks/monkey/"
DEFAULT_RES_DIR = os.path.join(get_resources_dir(), "testingFrameworks", "monkey")
DEFAULT_SEEDS_FILE = "monkey_seeds.txt"
DEFAULT_CONFIG_FILE = "monkey_cmd.cfg"


class MonkeyFramework(AbstractTestingFramework):
    def __init__(self, profiler, analyzer, default_workload=False, resdir=DEFAULT_RES_DIR):
        super(MonkeyFramework, self).__init__(id=TESTING_FRAMEWORK.MONKEY, profiler=profiler, analyzer=analyzer)
        self.executable_prefix = "adb shell monkey"
        self.workload = None
        self.res_dir = resdir
        if default_workload:
            self.init_default_workload(DEFAULT_SEEDS_FILE)

    def init_default_workload(self, pkg, seeds_file=DEFAULT_SEEDS_FILE):
        self.workload = WorkLoad()
        wl_filename = os.path.join(self.res_dir, seeds_file)
        config = self.__load_config_file()
        ofile = open(wl_filename, "r")
        i=0
        max_tests_per_app = self.get_config("tests_per_app", 100000000)
        for seed in ofile:
            if i >= max_tests_per_app:
                break
            wk = MonkeyWorkUnit(self.executable_prefix)
            wk.config(seed=seed.strip(), **config)
            self.workload.add_unit(wk)
            i = i+1
        ofile.close()

    def execute_test(self, package, wunit=None, timeout=None, *args, **kwargs):
        if wunit is None:
            wunit = self.workload.consume()
        if timeout or self.get_config("test_timeout", None):
            timeout_val = timeout if timeout is not None else self.get_config("test_timeout", None)
            wunit.add_timeout(timeout_val)
        if self.profiler.profiler == PROFILER.GREENSCALER:
            cmd = wunit.build_command(package, *args, **kwargs)
            self.profiler.exec_greenscaler(package, cmd)
        else:
            wunit.execute(package, *args, **kwargs)

    def init(self):
        pass

    def install(self):
        pass

    def uninstall(self):
        pass

    def __load_config_file(self, cfg_filename=DEFAULT_CONFIG_FILE):
        cfg_file = os.path.join(self.res_dir, cfg_filename)
        cfg = {}
        ofile = open(cfg_file, "r")
        for aline in ofile:
            key, pair = aline.split("=")
            cfg[key] = pair.strip()
        ofile.close()
        return cfg

    def test_app(self, device, app):
        retries_per_test = self.get_config("test_fail_retries", 1)
        for i, wk_unit in enumerate(self.workload.work_units):
            self.exec_one_test(i, device, app, wk_unit, n_retries=retries_per_test)

    def exec_one_test(self, test_id, device, app,  wk_unit, n_retries=1):
        if n_retries < 0:
            log(f"Validation failed. Ignoring test {test_id}", log_sev=LogSeverity.ERROR)
            return
        device.unlock_screen()
        time.sleep(1)
        self.profiler.init(**{'app': app})
        self.profiler.start_profiling()
        app.start()
        log_file = os.path.join(app.curr_local_dir, f"test_{test_id}.logcat")
        self.execute_test(app.package_name, wk_unit, **{'log_filename': log_file})
        app.stop()
        self.profiler.stop_profiling()
        device.clear_logcat()
        self.profiler.export_results(f"GreendroidResultTrace{test_id}.csv")
        self.profiler.pull_results(f"GreendroidResultTrace{test_id}.csv", app.curr_local_dir)
        app.clean_cache()
        if not self.analyzer.validate_test(app, test_id, **{'log_filename': log_file}):
            log("Validation failed. Retrying", log_sev=LogSeverity.WARNING)
            self.exec_one_test(test_id, device, app, wk_unit, n_retries=n_retries-1)
        else:
            log(f"Test {test_id} PASSED ", log_sev=LogSeverity.SUCCESS)

