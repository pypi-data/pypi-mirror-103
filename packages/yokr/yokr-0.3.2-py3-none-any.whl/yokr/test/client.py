import logging
logging.basicConfig(level=logging.DEBUG)

import yokr
yokr.report_val('my_timeseries', 1.0)
yokr.report_val('my_timeseries', 1.3, flush=True)
