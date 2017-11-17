'''
Runs unit tests on Monitors
'''
import unittest
import Tests.utils
import Monitors as mon
import Reporters as rep

class Test_Base_Monitor(unittest.TestCase):
    def setUp(self):
        self.monitor = mon.Base_Monitor(self.reporter): 

    # Test initialisation
    # Should have methods add_reporter and update_reporters
    # Should have a dictionary of reporters (initally empty) and a
    # data_signiture (empty dict for the base class as it passes no data)
    # May optionally take a list of pairs consitting of a reporter and 
    # appropriate collection for formatting_data and call add_reporter on
    # then automatically
    def test_initialisation_add_reporter(self):
        Tests.utils.check_has_method(self,self.monitor,'add_reporter')

    def test_initialisation_update_reporters(self):
        Tests.utils.check_has_method(self,self.monitor,'update_reporters')

    def test_initialisation_reporters(self):
        self.assertTrue(hasattr(self.monitor,'reporters'),
                        'The Base_Monitor has no reporters dictionary')
        self.assertEqual(self.monitor.reporters,{},
                        'The reporters attribute is not initalised to the '
                        'empty dictionary')

    def test_initialisation_data_signiture(self):
        self.assertTrue(hasattr(self.monitor,'data_signiture'),
                        'The Base_Monitor has no data_signiture')
        self.assertEqual(self.monitor.reporters,{},
                        'The data_signiture attribute is not initalised to '
                        'the empty dictionary for the Base_Monitor')
        

    # Tests add_reporter method
    # This call the register method of the reporter with the monitor and 
    # formatting_info as arguments and store the returned ID in the 
    # monitors reporters dictionary, with the reporter as its key

    # Test update_reporters method
    # This should call the update method of each reporter in reporters,
    # passing the corresponding ID as positional argument and 
    # data matching the monitor's signiture as keyword arguments
