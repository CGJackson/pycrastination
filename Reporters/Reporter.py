'''
Reporters output information about the state and progress of the program to
the user. They handle information about the formatting of this output, as 
well as any additional processing which is required to support it, such as
comunicating with a web or email server, for example.

They are derived from the Base_Reporter class
'''

class Base_Reporter():
    '''    
    Reporters output information about the state and progress of the program
    to the user. They handle information about the formatting of this
    output, as well as any additional processing which is required to 
    support it, such as comunicating with a web or email server, for 
    example.
    '''
    pass    #TODO

class Text_Reporter(Base_Reporter):
    '''
    Generates text detailing the information to be reported,
    '''
    pass    #TODO

class Cmd_Line_Reporter(Text_Reporter):
    '''
    Text Reporter the prints text to stdout
    '''
    pass    #TODO
