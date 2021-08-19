from anadroid.Types import TESTING_APPROACH, TESTING_FRAMEWORK, BUILD_SYSTEM, PROFILER, INSTRUMENTER, ANALYZER
from anadroid.instrument.Types import INSTRUMENTATION_TYPE

SUPPORTED_TESTING_APPROACHES = {
    TESTING_APPROACH.WHITEBOX
}

SUPPORTED_TESTING_FRAMEWORKS = {
    TESTING_FRAMEWORK.MONKEY,
    TESTING_FRAMEWORK.RERAN,
    TESTING_FRAMEWORK.APP_CRAWLER,
    TESTING_FRAMEWORK.MONKEY_RUNNER,
    TESTING_FRAMEWORK.JUNIT,
    TESTING_FRAMEWORK.DROIDBOT
}

SUPPORTED_BUILDING_SYSTEMS = {
    BUILD_SYSTEM.GRADLE
}

SUPPORTED_PROFILERS = {
    PROFILER.TREPN,
    PROFILER.MANAFA,
    PROFILER.GREENSCALER
}

SUPPORTED_INSTRUMENTERS = {
    INSTRUMENTER.JINST
}

SUPPORTED_ANALYZERS = {
    ANALYZER.OLD_ANADROID_ANALYZER,
    ANALYZER.MANAFA_ANALYZER
}

SUPPORTED_INSTRUMENTATION_TYPES = {
    INSTRUMENTATION_TYPE.TEST,
    INSTRUMENTATION_TYPE.ANNOTATION
}

SUPPORTED_SUITES = {
    PROFILER.TREPN: [INSTRUMENTATION_TYPE.TEST, INSTRUMENTATION_TYPE.METHOD],
    PROFILER.MANAFA: [INSTRUMENTATION_TYPE.ANNOTATION],
    PROFILER.GREENSCALER: [INSTRUMENTATION_TYPE.ANNOTATION]
}