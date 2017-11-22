'''
Runs unit tests on Reporters
'''
import unittest
import Tests.utils
import Reporters, Monitors

class TestBaseReporter(unittest.TestCase):
    def setUp(self):
        self.base_reporter = Reporters.Base_Reporter()
    
    # Tests whether the Base_Reporter class initalizes correctly
    # Should have methods update, register and parse_formatting_data.
    # Should have a dictionary, registered_monitors (initally empty)
    def test_initialization_update(self):
        Tests.utils.check_has_method(self,self.base_reporter,'update')

    def test_initialization_register(self):
        Tests.utils.check_has_method(self,self.base_reporter,'register')

    def test_initialization_parse_formatting_data(self):
        Tests.utils.check_has_method(self,self.base_reporter,
                               'parse_formatting_data')

    def test_initialization_registered_monitors(self):
        self.assertTrue(
                        hasattr(self.base_reporter,'registered_monitors'),
                        'BaseReporter has no attribute registered_monitors')
        self.assertEqual(self.base_reporter.registered_monitors,{})
    
    # Tests the register method of the Base reporter class. 
    # This should take a monitor and some formatting information as
    # inputs. An ID for the monitor should be generated. The monitor's ID,
    # data signiture and formatting information should be added to 
    # dictionary of registered monitors. The monitor's ID should be
    # returned.
    def test_register_id_generation(self):
        monitor1, monitor2 = Monitors.Base_Monitor(),Monitors.Base_Monitor()

        # tests id generation
        id1 = self.base_reporter.register(monitor1,{})
        self.assertIsNotNone(id1,'Did not return monitor ID')
        self.assertIn(id1,self.base_reporter.registered_monitors,
                                    'Monitor ID not registered')
        # tests that id generation is unique
        id2 = self.base_reporter.register(monitor2,{}) 
        self.assertNotEqual(id2,id1)

    def test_register_data_recording(self):
        monitor1, monitor2 = Monitors.Base_Monitor(),Monitors.Base_Monitor()

        id1 = self.base_reporter.register(monitor1,{})
        # tests that monitor information is recorded sucseffully
        monitor1_data = self.base_reporter.registered_monitors[id1]
        self.assertEqual(monitor1_data[0],monitor1.data_signiture,
                            'Monitor data signiture recorded incorrectly')
        self.assertIsNone(monitor1_data[1],'Monitor formatting '
                                'informaiton recorded incorerectly')

        # Check that the foramatting data stored is, in fact, what is
        # returned by parse_formatting_data
        def parse_formatting_with_data(data):
            return {},data

        self.base_reporter.parse_formatting_data=parse_formatting_with_data
        id2 = self.base_reporter.regiser(monitor2, 'Some Data')
        monitor2_data = self.base_reporter.registered_monitors[id2]
        self.assertEqual(monitor2_data[1],'Some Data')
        
    def test_register_incompatable_formatting_data_raises_ValueError(self):
        
        def dumby_parse_formatting_data(data):
            return {'random_keyword':str}, None

        self.base_reporter.parse_formatting_data=dumby_parse_formatting_data

        monitor = Monitors.Base_Monitor()

        self.assertRaises(ValueError,self.base_reporter.register,monitor,{})

    def test_parse_formatting_data(self):
        '''
        Should accept 1 argument (The formatting data).
        Should return {}, None for all inputs, as the Base_Reporter does 
        nothing with any data it is given.
        '''
        signiture,formatting = self.base_reporter.parse_formatting_data(
                                                    'dumby formatting data')
        self.assertEqual(signiture,{},'Did not return an empty signiture')
        self.assertIsNone(formatting, 'Did not return None for formatting '
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
        
        dud_id = self.base_reporter.register(Monitors.Base_Monitor(),{})
        self.base_reporter.registered_monitors.pop(dud_id)
        
        self.assertRaises(ValueError,self.base_reporter.update,dud_id)


class Test_is_compatable_data_signiture(unittest.TestCase):
    '''
    Runs unit tests on the function is_compatable_data_signiture
    One data signiture is compatable with the second if each element of
    the first is in the second. Dicts should be acceptable as data 
    signitures, but carrently only keys are considered
    '''
    def setUp(self):

        self.is_compatable = Reporters.utils.is_compatable_data_signiture  

        # data_signiture1 should be compatable with 2, but not vis versa
        self.data_signiture1 = {'name_one':int,'name_2':float}
        self.data_signiture2 = {'name_one':int,'name_2':float,'name_3':int}
    def test_basic_usage(self):
        self.assertTrue(self.is_compatable(self.data_signiture1,self.data_signiture2),
                            'Compatable data signitures returned false')

        self.assertFalse(self.is_compatable(self.data_signiture2,self.data_signiture1),
                            'Incompatable data signitures returned true')
    def test_on_identical_data_signitures(self):
        self.assertTrue(self.is_compatable(self.data_signiture1,self.data_signiture1),
                            'Giving identical data signtures returned false'
                            )
    def test_on_empty_data_signitures(self):
        self.assertTrue(self.is_compatable({},self.data_signiture1),
                            'The empty data signiture was incompatable with'
                            'another data signiture')
        self.assertTrue(self.is_compatable({},{}),
                            'Two empty data signitures were incompatable')
if __name__ == '__main__':
    unittest.main()
