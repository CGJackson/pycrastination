'''
Reporters output information about the state and progress of the program to
the user. They handle information about the formatting of this output, as 
well as any additional processing which is required to support it, such as
comunicating with a web or email server, for example.

They are derived from the Base_Reporter class
'''

import Reporters.utils

class Base_Reporter():
    '''    
    Reporters output information about the state and progress of the program
    to the user. They handle information about the formatting of this
    output, as well as any additional processing which is required to 
    support it, such as comunicating with a web or email server, for 
    example.
    '''
    def __init__(self):
        '''
        Creates Reporter object with an empty dictionary of 
        registered_monitors
        '''
        self.registered_monitors = {}

    def register(self, monitor, formatting_data):
        '''
        Registers a monitor with the reporter. 
        Records information about how data from the monitor should be 
        interpreded and displayed. Records this, along with the signiture of
        the data the Reportor can expect to recieve from the Monitor.
        Returns an id that is given to the Reporter with updates to identify
        which monitor is providing the update. 
        '''
        # Generates an id for the monitor.
        #
        # id shoud be unique to each registered monitor and small enough to 
        # avoid passing around large objects as dict keys.
        #
        # currently uses the python object id, but this is non-essential
        # and should not be relied upon outside of Reporter class (and 
        # and should avoid relying on it there.
        monitor_id = id(monitor)
        
        # The formatting data is processed by the parse_formatting_data 
        # method. This method will generally be overwritten in subclasses
        required_signiture, parsed_formatting_information = (
                                self.parse_formatting_data(formatting_data)
                                                       )
        # It is checked that the monitor will proved the information
        # nessarsery for the Reporters output. 
        if not Reporters.utils.is_compatable_data_signiture(
                            required_signiture, monitor.data_signiture):
            raise ValueError('The formatting data given to Reporter is not '
                             'compatable with the data provided by the '
                             'Monitor being registered')

        # The monitor's information is recorded (as you would expect for a
        # method called register
        self.registered_monitors[monitor_id] = (monitor.data_signiture, 
                                            parsed_formatting_information)

        # The monitor_id is returned so that the monitor can use it to
        # identify itself when updating the reporter. 
        return monitor_id

    def parse_formatting_data(self,formatting_data):
        '''
        Processes that formatting data passed with a newly registered
        Monitor to tell the Reporter how to display the data passed to it
        from that monitor

        Returns a tuple consiting of dictionary containing the data 
        signiture required to display the output requested and the processed
        data about how the Reporter should display the data passed by the
        monitor.
        '''
        # As the Base_Reporter does not display any data, the data signiture
        # is the empty dictionary (no data required) and the processed
        # formatting data is None
        return {}, None

    def update(self, monitor_id, **kwargs):
        '''
        Passes data from a monitor to the Reporter. The id returned when 
        the monitor was registerd with the reporter must be given, followed
        by any number of keyword arguemnts. The keyword arguments are
        interpreted by comparing withthe monitor's data signiture.
        '''
        try:
            if not Reporters.utils.is_compatable_data_signiture(kwargs,
                                self.registered_monitors[monitor_id][0]):
                raise ValueError("Data in update not compatable with the "
                             "passing monitor's data signiture")
        except KeyError:
                raise ValueError('ID does not corrispond to a registered'
                                 ' Monitor')

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

