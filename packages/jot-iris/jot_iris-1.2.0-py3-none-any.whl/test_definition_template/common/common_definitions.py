"""Common definitions for all test sequencies"""
import os
from test_runner.test_position import TestPosition
from test_runner.dut import Dut
from test_runner.test_case import FlowControl


TEST_POSITIONS = [
    TestPosition('1', 'left'),
    TestPosition('2', 'middle'),
    TestPosition('3', 'right'),
]

# FlowControl.CONTINUE keeps testing even some test fails
# FlowControl.STOP_ON_FAIL stops on first fail

FLOW_CONTROL = FlowControl.CONTINUE

# Wait DUT serial number from UI
SN_FROM_UI = False

# List of test sequences' directory names
TEST_SEQUENCES = os.listdir('test_definitions')
if 'common' in TEST_SEQUENCES:
    TEST_SEQUENCES.remove('common')


def parse_dut_info(info, test_position):
    return Dut(serial_number=info['sn'], test_position=test_position)
