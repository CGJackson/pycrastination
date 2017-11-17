'''
Runs unit tests on Reporters
'''
import unittest
import Reporters, Monitors

class TestBaseReporter(unittest.TestCase):
    def setUp(self):
        self.base_reporter = Reporters.Base_Reporter()
    
    def test_base_reporter_initialization(self):
        '''
        Tests whether the Base_Reporter class initalizes correctly
        Should have methods update, register and parse_formatting_data.
        Should have a dictionary, registered_monitors (initally empty)
        '''
        for method_name in ('update','register','parse_formatting_data'):
            self.assertTrue(hasattr(self.base_reporter,method_name),
                               'BaseReporter has no attribute '+method_name)
            self.assertTrue(
                        callable(getattr(self.base_reporter,method_name)),
                        'Method '+method_name+' is uncallable')

        self.assertTrue(
                        hasattr(self.base_reporter,'registered_monitors'),
                        'BaseReporter has no attribute registered_monitors')
        self.assertEqual(self.base_reporter.registered_monitors,{})
    
    def test_register(self):
        '''
        Tests the register method of the Base reporter class. 
        This should take a monitor and some formatting information as
        inputs. An ID for the monitor should be generated. The monitor's ID,
        data signiture and formatting information should be added to 
        dictionary of registered monitors. The monitor's ID should be
        returned.
        '''
        monitor1, monitor2 = Monitors.Base_Monitor(),Monitors.Base_Monitor()

        # tests id generation
        id1 = self.base_reporter.register(monitor1,{})
        self.assertIsNotNone(id1,'Did not return monitor ID')
        self.assertIn(id1,self.base_reporter.registered_monitors,
                                    'Monitor ID not registered')
        # tests that monitor information is recorded sucseffully
        monitor1_data = self.base_reporter.registered_monitors[id1]
        self.assertEqual(monitor1_data[0],monitor1.data_signiture,
                            'Monitor data signiture recorded incorrectly')
        self.assertIsNone(monitor1_data[1],'Monitor formatting '
                                'informaiton recorded incorerectly')

        # tests that id generation is unique
        id2 = self.base_reporter.register(monitor2,{}) 
        self.assertNotEqual(id2,id1)

    def test_parse_formatting_data(self):
        '''
        Should accept 1 argument (The formatting data).
        Should return {}, None for all inputs, as the Base_Reporter does 
        nothing with any data it is given.
        '''
        signiture,formatting = self.base_reporter.parse_formatting_data(
                                                    'dumby formatting data')
        unittest.IsEqual(signiture,{},'Did not return an empty signiture')
        unittest.IsNone(formatting, 'Did not return None for formatting '
                                    'data')

    def test_update(self):
        '''
        Accepts an ID and set of keywords as arguments.
        The ID must correspond to a registered monitor, otherwise ValueError
        is raised. 
        All parts of the data signiture for that monitor must corrispond 
        to one of the keywords given, otherwise ValueError is raised. 
        '''
        monitor = Monitors.Base_Monitor()
        monitor.data_signiture = {'dat1':int,'dat2':str}
        monitor_id = self.base_reporter.register(monitor,{})
        
        self.assertIsNone(self.base_reporter.update(monitor_id),
                                'update did not return None with no '
                                 'keywords given')
        self.assertIsNone(self.base_reporter.update(monitor_id,dat1=5),
                                'update did not return none when passed '
                                'compatable keywords')

        self.assertRaises(ValueError,self.base_reporter.update,
                                        monitor_id,some_keyword=0)
        
        dud_id = self.base_reporter.register(Monitor.Base_Monitor(),{})
        self.base_reporter.registered_monitors.pop(dud_id)
        
        self.assertRaises(ValueError,self.base_reporter.update,dud_id)

class Testis_compatable_data_signiture(unittest.TestCase):
    '''
    Runs unit tests on the function is_compatable_data_signiture
    '''
    def test_is_compatable_data_signiture(self):
        '''
        Unit tests on is_compatable_data_signiture.
        One data signiture is compatable with the second if each element of
        the first is in the second. Dicts should be acceptable as data 
        signitures, but carrently only keys are considered
        '''
        is_compatable = Reporters.is_compatable_data_signiture  # for sanity

        # data_signiture1 should be compatable with 2, but not vis versa
        data_signiture1 = {'name_one':int,'name_2':float}
        data_signiture2 = {'name_one':int,'name_2':float,'name_3':int}

        self.assertTrue(is_compatable(data_signiture1,data_signiture2),
                            'Compatable data signitures returned false')

        self.assertFalse(is_compatable(data_signiture2,data_signiture1),
                            'Incompatable data signitures returned true')

        self.assertTrue(is_compatable(data_signiture1,data_signiture1),
                            'Giving identical data signtures returned false'
                            )
        self.assertTrue(is_compatable({},data_signiture1),
                            'The empty data signiture was incompatable with'
                            'another data signiture')
        self.assertTrue(is_compatable({},{}),
                            'Two empty data signitures were incompatable')
if __name__ == '__main__':
    unittest.main()
