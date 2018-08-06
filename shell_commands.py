# Replicating some of the unix shell commands - ls, touch, rm
import os
import abc

history = []

class Command(object):
    """ The command interface """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self):
        """ Method which will executethe command """
        pass
    
    @abc.abstractmethod
    def undo(self):
        """ Method to undo the command """
        pass


class LsCommand(Command):
    """ The concrete command that emulates the unix command behaviour"""
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        """ The command delegaing the call to it's receiver """
        self.receiver.show_current_dir()

    def undo(self):
        """ This command does not have an undo functionality """
        pass

#LS command
class LsReceiver(object):
    def show_current_dir(self):
        cur_dir = './'

        filenames = []
        for filename in os.listdir(cur_dir):
            if os.path.isfile(os.path.join(cur_dir, filename)):
                filenames.append(filename)
        print "The current dir contains: ", os.path.join(filenames)

#Touch command
class touchCommand(Command):
    """ class emulating the touch command """
    def __init__(self,  receiver):
        self.receiver = receiver
    
    def execute(self):
        self.receiver.create_file()

    def undo(self):
        self.receiver.delete_file()
    
class touchReceiver(object):
    def __init__(self, filename):
        self.filename = filename

    def create_file(self):
        with file(self.filename,'a'):
            os.utime(self.filename, None)
        
    def delete_file(self):
        os.remove(self.filename)
    
class RmCommand(Command):
    """ class that emulates the unix command """
    def __init__(self, receiver):
        self.receiver = receiver
    
    def execute(self):
        self.receiver.delete_file()
    
    def undo(self):
        self.receiver.undo()
    
class RmReceiver(object):
    def __init__(self, filename):
        self.filename = filename
    
    def delete_file(self):
        """  Deletes the file and creates a backup for the undo command """
        self.backup_name = '.'+ self.filename
        os.rename(self.filename, self.backup_name)
    
    def undo(self):
        """ Restores the deleted file from the backup """
        original_name = self.backup_name[1:]
        os.rename(self.backup_name, original_name)
        self.backup_name = None
    
class Invoker(object):
    def __init__(self, create_file_commands, delete_file_commands):
        self.create_file_commands = create_file_commands
        self.delete_file_commands= delete_file_commands
        self.history = []
    
    def create_file(self):
        print "Creating file..."

        for command in self.create_file_commands:
            command.execute()
            self.history.append(command)
        print "File created. \n"

    def delete_file(self):
        print "Deleting file..."

        for command in self.delete_file_commands:
            command.execute()
            self.history.append(command)
        print "File deleted.\n"
    
    def undo_all(self):
        print  "Undo all..."

        for command in reversed(self.history):
            command.undo()
        print "Undo all has finished.\n"

if __name__ == "__main__":
    #List files in current dir
    ls_receiver = LsReceiver()
    ls_command = LsCommand(ls_receiver)

    #Create file
    touch_receiver = touchReceiver('test_file')
    touch_command = touchCommand(touch_receiver)

    #Delete file
    rm_receiver = RmReceiver('test_file')
    rm_command = RmCommand(rm_receiver)

    create_file_commands = [ls_command, touch_command, ls_command]
    delete_file_commands = [ls_command, rm_command, ls_command]

    invoker = Invoker(create_file_commands, delete_file_commands)
    invoker.create_file()
    invoker.delete_file()
    invoker.undo_all()






