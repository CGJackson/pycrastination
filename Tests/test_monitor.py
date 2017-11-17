'''
Runs unit tests on Monitors
'''
import unittest
import Monitors.Monitor as mon
import Reporters.Reporter as rep

class TestBaseMonitor(unittest.TestCase):
    def setUp(self):
        self.reporter = rep.Text_Reporter():
        self.monitor = mon.BaseMonitor(self.reporter): 

    def tearDown(self):
        pass

    def test_initialisation(self):
