'''
Runs unit tests on Monitors
'''
import unittest
import Tests.utils
import Monitors
import Reporters

class Test_Base_Monitor(unittest.TestCase):
    def setUp(self):
        self.monitor = Monitors.Base_Monitor() 

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
        
    # TODO test optional argument to add reporters at initialisation

    # Tests add_reporter method
    # This call the register method of the reporter with the monitor and 
    # formatting_info as arguments and store the returned ID in the 
    # monitors reporters dictionary, with the reporter as its key
    def test_add_reporter_reporter_added(self):
        '''
        Checks that the add reporter method adds the reporter to the list of
        reporters, together with the monitors id for that reporter.
        '''
        reporter = Reporters.Base_Reporter()
        self.monitor.add_reporter(reporter,{})
        self.assertIn(reporter,self.monitor.reporters,
                      'Reporter was not added to dictonary of reporters')
        self.assertIsNotNone(self.monitor.reporters[reporter],
                            'added reporter does not record a valid id')

    def test_add_reporter_monitor_registered(self):
        '''
        Checks that add_reporter method also registers the monitor with the 
        reporter
        '''
        
        class Dumby_Reporter(Reporters.Base_Reporter):
            '''
            a dumby reporter class which keeps track of the number of times
            register has been called and what arguments were  passed
            on each call
            '''
            def __init__(self):
                Reporters.Base_Reporter.__init__(self)
                self.register_calls = 0
                self.register_args = []

            def register(self,monitor,formatting_data):
                self.register_calls += 1
                self.register_args.append((monitor,formatting_data))
                return Reporters.Base_Reporter.register(
                                               self,monitor,formatting_data)
        reporter = Dumby_Reporter()

        monitor2 = Monitors.Base_Monitor()

        formatting_data1 = 'Some formatting data'
        formatting_data2 = ['Totally', 'different', 'formatting', 'data']

        # Checks that register is called each time add_reporter is called

        assert reporter.register_calls == 0

        self.monitor.add_reporter(reporter, formatting_data1)
        self.assertEqual(reporter.register_calls,1,
                'after being added to one monitor, the reporter had been '
                'called {} times'.format(reporter.register_calls))
            

        monitor2.add_reporter(reporter, formatting_data2)
        self.assertEqual(reporter.register_calls,2,
                'after being added to 2 monitors, the reporter had been '
                'called {} times'.format(reporter.register_calls))

        # Checks that register was called with the correct arguments
        expected_args = ((self.monitor, formatting_data1),
                         (monitor2, formatting_data2))
        for expected, actual in zip(expected_args, reporter.register_args):
            self.assertIs(expected[0],actual[0],
           'register was not called with the monitor as the first argument')
            self.assertEqual(expected[1],actual[1], 
                            'register was not called with the expected '
                            'formatting data the second argument')

        
    # Test update_reporters method
    # This should call the update method of each reporter in reporters,
    # passing the corresponding ID as positional argument and 
    # data matching the monitor's signiture as keyword arguments
    def test_update_reporters_check_all_reporters_updated(self):
        '''
        Checks that each reporter in Reporters is updated exactly once
        each time unpdate_reporters is called
        '''
        reporter_update_count = {}

        class Dumby_Reporter(Reporters.Base_Reporter):
            '''
            a reporter that updates reporter_update_count with the number
            of times its update method has bee called
            '''
            def __init__(self):
                reporter_update_count[self] = 0
                Reporters.Base_Reporter.__init__(self)

            def update(self,monitor_id, **kwargs):
                reporter_update_count[self] += 1
                return Reporters.Base_Reporter.update(
                                                self,monitor_id,**kwargs)

        reporter1,reporter2,reporter3 = [Dumby_Reporter() for i in range(3)]

        assert len(reporter_update_count) == 3
        assert all(i == 0 for i in reporter_update_count.values())

        self.monitor.add_reporter(reporter1, {})
        
        self.monitor.update_reporters()

        self.assertEqual(reporter_update_count[reporter1],1,
            'Reporter should have been updated once, had actually been '
            'updated {} times'.format(reporter_update_count[reporter1]))
        self.assertEqual(reporter_update_count[reporter2],0, 
        'reporter was updated when it had not been added to the monitor')
        self.assertEqual(reporter_update_count[reporter3],0,
        'reporter was updated when it had not been added to the monitor')

        self.monitor.update_reporters()

        self.assertEqual(reporter_update_count[reporter1],2,
            'Reporter should have been updated twice, had actually been '
            'updated {} times'.format(reporter_update_count[reporter1]))
        self.assertEqual(reporter_update_count[reporter2],0, 
        'reporter was updated when it had not been added to the monitor')
        self.assertEqual(reporter_update_count[reporter3],0,
        'reporter was updated when it had not been added to the monitor')

        self.monitor.add_reporter(reporter2,{})

        self.monitor.update_reporters()

        self.assertEqual(reporter_update_count[reporter1],3,
            'Reporter should have been updated 3 times, had actually been '
            'updated {} times'.format(reporter_update_count[reporter1]))
        self.assertEqual(reporter_update_count[reporter2],1, 
            'Second reporter should have been updated once, had actually '
            'been updated {} times'.format(
                                        reporter_update_count[reporter2]))
        self.assertEqual(reporter_update_count[reporter3],0,
        'reporter was updated when it had not been added to the monitor')

        self.monitor.add_reporter(reporter3,{})

        self.monitor.update_reporters()

        self.assertEqual(reporter_update_count[reporter1],4,
            'Reporter should have been updated 4 times, had actually been '
            'updated {} times'.format(reporter_update_count[reporter1]))
        self.assertEqual(reporter_update_count[reporter2],2, 
            'Second reporter should have been updated twice, had actually '
            'been updated {} times'.format(
                                        reporter_update_count[reporter2]))
        self.assertEqual(reporter_update_count[reporter3],1,
            'Third reporter should have been updated once, had actually '
            'been updated {} times'.format(
                                        reporter_update_count[reporter3]))

    def test_update_reporters_check_reporters_recieve_correct_data(self):
        '''
        Checks that each reporter is updated with the correct id and data 
        '''
        class Dumby_Reporter(Reporters.Base_Reporter):
            '''
            A reporter which records the arguments passed to update
            '''
            def __init__(self):
                self.passed_args = []
                Reporters.Base_Reporter.__init__(self)

            def update(self,monitor_id,**kwargs):
                self.passed_args.append((monitor_id,kwargs))
                return Reporters.Base_Reporter.update(
                                                self,monitor_id,**kwargs)

        reporter1, reporter2 = Dumby_Reporter(), Dumby_Reporter()
        
        self.monitor.add_reporter(reporter1,{})
        self.monitor.update_reporters()
        
        self.assertEqual(reporter1.passed_args[-1][0], 
                        (self.monitor.reporters[reporter1]),
                        'Monitor did not pass reporter the correct id')
        self.assertEqual(reporter1.passed_args[-1][1],{},
                        'Base_Monitor passed non-trivial data to updated '
                        'reporter')

        self.monitor.data_signiture = {'Dumby':'data','Some':'stuff'}
        self.monitor.update_reporters()
        self.assertEqual(reporter1.passed_args[-1][0], 
                        (self.monitor.reporters[reporter1][0]),
                        'Monitor did not pass reporter the correct id when '
                        'given non-trivial extra data')
        self.assertEqual(reporter1.passed_args[-1][1],
                        self.monitor.data_signiture,
                        'Did not pass correct data to updated reporters')

        self.monitor.add_reporter(reporter2,{})
        self.update_reporters()
        self.assertEqual(reporter1.passed_args[-1][0], 
                        (self.monitor.reporters[reporter1][0]),
                        'Monitor did not pass the correct id to the first '
                        'updated reporter of 2')
        self.assertEqual(reporter1.passed_args[-1][1],
                        self.monitor.data_signiture,
                        'Did not pass correct data to first updated'
                        'reporter of 2')
        self.assertEqual(reporter2.passed_args[-1][0], 
                        (self.monitor.reporters[reporter2][0]),
                        'Monitor did not pass the correct id to the second '
                        'updated reporter of 2')
        self.assertEqual(reporter2.passed_args[-1][1],
                        self.monitor.data_signiture,
                        'Did not pass correct data to second updated'
                        'updated reporter of 2')
