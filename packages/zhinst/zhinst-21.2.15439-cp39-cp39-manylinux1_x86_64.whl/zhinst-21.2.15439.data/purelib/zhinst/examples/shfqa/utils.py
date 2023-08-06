"""
Zurich Instruments LabOne Python API Utility Functions for SHF.
"""
# pylint: disable=bad-continuation

import time
import numpy as np
from zhinst.utils import assert_node_changes_to_expected_value

# Max waveform length of the signal generator
QA_SG_CARRIER_WVF_LENGTH = 4 * 2 ** 10
QA_SG_NUM_CARRIERS = 16

SAMPLING_FREQUENCY = 2e9


def get_num_channels(daq, device):
    """
    Returns the number of QA channels.

    Arguments:

      daq (instance of ziDAQServer): A ziPython API session.

      device (str): device id, e.g. "dev12024"

    Returns:

      number of channels (int): number of QA channels.
    """
    return len(daq.listNodes(f"/{device}/QACHANNELS/"))


def load_sequencer_program(daq, device, channel, seqc_program):
    """
    Compiles the given program and loads it to the specified sequencer.

    Arguments:

      daq (instance of ziDAQServer): A ziPython API session.

      device (str): device id, e.g. "dev12024"

      channel (int): QA channel

      seqc_program (str): sequencer C program
    """

    timeout_compile = 10
    timeout_ready = 10

    awgModule = daq.awgModule()
    awgModule.set("device", device)
    awgModule.set("index", channel)
    awgModule.execute()

    t_start = time.time()
    awgModule.set("compiler/sourcestring", seqc_program)
    while awgModule.getInt("compiler/status") == -1:
        if time.time() - t_start > timeout_compile:
            statusstring = awgModule.getString("compiler/statusstring")
            raise RuntimeError(
                f"Failed to compile program for channel {channel} after {timeout_compile} s, "
                f"compiler/statusstring: `{statusstring}`."
            )
        time.sleep(0.1)

    assert_node_changes_to_expected_value(
        daq,
        f"/{device}/qachannels/{channel}/generator/sequencer/ready",
        1,
        sleep_time=0.1,
        max_repetitions=int(timeout_ready / 0.1),
    )
    time.sleep(0.1)


def configure_scope(
    daq,
    device,
    input_select,
    scope_length,
    segments_count=1,
    scope_time_setting=0,
    scope_averaging_count=1,
    scope_trig_delay=0,
):
    """
    Prepares the scope for measurements with the given configuration parameters.

    Arguments:

      daq (instance of ziDAQServer): A ziPython API session.

      device (str): device id, e.g. "dev12024"

      input_select (dict of int : str): choose the input signal for each scope channel,
            for example use {1: "channel0_signal_input"} to use the RF input of channel 0
            with the 2nd scope channel, all unspecified scope channels will be disabled

      segments_count (int): number of segments in device memory

      scope_time_setting (int): time base of scope. The resulting sampling time is 2^n/2GHz.

      scope_averaging_count (int): number of scope measurements to average

      scope_trig_delay (float): delay between trigger and measurement in seconds
    """

    daq.setInt(f"/{device}/scopes/0/segments/count", segments_count)
    if segments_count > 1:
        daq.setInt(f"/{device}/scopes/0/segments/enable", 1)
    else:
        daq.setInt(f"/{device}/scopes/0/segments/enable", 0)

    if scope_averaging_count > 1:
        daq.setInt(f"/{device}/scopes/0/averaging/enable", 1)
    else:
        daq.setInt(f"/{device}/scopes/0/averaging/enable", 0)
    daq.setInt(f"/{device}/scopes/0/averaging/count", scope_averaging_count)

    daq.setInt(f"/{device}/scopes/0/channels/*/enable", 0)
    for channel, selected_input in input_select.items():
        daq.setString(
            f"/{device}/scopes/0/channels/{channel}/inputselect", selected_input
        )
        daq.setInt(f"/{device}/scopes/0/channels/{channel}/enable", 1)

    daq.setInt(f"/{device}/scopes/0/time", scope_time_setting)  # decimation rate

    daq.setDouble(f"/{device}/scopes/0/trigger/delay", scope_trig_delay)

    daq.setInt(f"/{device}/scopes/0/length", scope_length)


def get_vector(daq, node):
    """
    Reads a vector node.

    Arguments:

      daq (instance of ziDAQServer): A ziPython API session.

      node (str): path to vector node

    Returns:

      dictionary with data from vector node or None in case no data are available
    """
    path = node.lower()
    daq.getAsEvent(path)
    tmp = daq.poll(1.0, 500, 4, True)
    if path in tmp:
        return tmp[path]
    return None


def get_scope_data(daq, device):
    """
    Waits until the scope was triggered and returns the measured data.

    Arguments:

      daq (instance of ziDAQServer): A ziPython API session.

      device (str): device id, e.g. "dev12024"

    Returns:

      recorded_data (array): contains an array per scope channel with the measured data

      recorded_data_range (array): contains the full scale range for each scope channel

      scope_time (array): relative time for each point in recorded_data in seconds starting from 0
    """

    # wait until scope has been triggered
    assert_node_changes_to_expected_value(daq, f"/{device}/scopes/0/enable", 0)
    daq.sync()

    # read and post-process the recorded data
    recorded_data = [[], [], [], []]
    recorded_data_range = [0.0, 0.0, 0.0, 0.0]
    num_bits_of_adc = 14
    max_adc_range = 2 ** (num_bits_of_adc - 1)

    for channel in range(4):
        if daq.getInt(f"/{device}/scopes/0/channels/{channel}/enable"):
            vector = get_vector(daq, f"/{device}/scopes/0/channels/{channel}/wave")

            recorded_data[channel] = vector[0]["vector"]
            averagecount = vector[0]["properties"]["averagecount"]
            scaling = vector[0]["properties"]["scaling"]
            voltage_per_lsb = scaling * averagecount
            recorded_data_range[channel] = voltage_per_lsb * max_adc_range

    # generate the time base
    scope_time = [[], [], [], []]
    decimation_rate = 2 ** daq.getInt(f"/{device}/scopes/0/time")
    sampling_rate = SAMPLING_FREQUENCY / decimation_rate  # [Hz]
    for channel in range(4):
        scope_time[channel] = (
            np.array(range(0, len(recorded_data[channel]))) / sampling_rate
        )

    # return the scope data
    return recorded_data, recorded_data_range, scope_time
