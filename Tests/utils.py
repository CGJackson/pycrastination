'''
Utility functions for unit testing
'''

def check_has_method(test_case, test_object, method_name):
    '''
    given a TestCase, test_case, checks whether test_object has a method
    called method_name 
    '''
    test_case.assertTrue(hasattr(test_object,method_name),
                               'BaseReporter has no attribute '+method_name)
    test_case.assertTrue(callable(getattr(test_object,method_name)),
                        'Method '+method_name+' is uncallable')

