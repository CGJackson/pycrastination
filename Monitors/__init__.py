'''
Monitors keep track of the progress your program has made and then pass 
this information to reporters

They are derived from the Base_Monitor class
'''

class Base_Monitor():
    '''
    Base class for monitors. Monitors keep track of the state and progress 
    of the program and pass this information to Reporters
    '''
    def __init__(self):
        self.data_signiture = {}
        self.reporters = {}

    def update_reporters(self):
        '''
        Updates reporters with data from the monitor stored in 
        data_signiture
        '''
        for reporter, id_with_reporter in self.reporters.items():
            reporter.update(id_with_reporter,**self.data_signiture)

    def add_reporter(self,reporter,formatting_data):
        '''
        Adds a reporter to the list of reporters updated with 
        information by the monitor.
        
        Takes a reporter and some relevant formatting information which 
        is passed to the reporter to detail how the data passed to it by
        the monitor should be interpretted.
        '''
        id_with_reporter = reporter.register(self,formatting_data)
        self.reporters[reporter] = id_with_reporter

class Fixed_Point_Monitor(Base_Monitor):
    '''
    Monitor which detects that certain fixed checkpoints in the program have
    been reached.
    '''
    pass    #TODO

class Loop_Monitor(Base_Monitor):
    '''
    Monitor which tracks progress through a iteration or for loop.
    '''
    pass    #TODO
