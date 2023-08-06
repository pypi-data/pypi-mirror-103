""" Run a triggered frequency sweep with the SHFQA
"""

# Copyright 2021 Zurich Instruments AG

import time


def set_trigger_loopback(daq, dev):
    """
    Start a continuous trigger pulse from marker 1 A using the internal loopback to trigger in 1 A
    """

    m_ch = 0
    continuous_trig = 1
    daq.setInt(f"/{dev}/raw/markers/{m_ch}/testsource", continuous_trig)
    daq.setDouble(f"/{dev}/raw/markers/{m_ch}/frequency", 1e3)
    daq.setInt(f"/{dev}/raw/triggers/{m_ch}/loopback", 1)
    time.sleep(0.2)
