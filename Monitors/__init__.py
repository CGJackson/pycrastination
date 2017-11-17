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
    pass    #TODO

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
