import os

from multiprocessing import Process, Queue, Lock, Pool
from .Log import Logger

class TrainingManager(object):

    def __init__(self):
        pass

    @staticmethod
    def shell_training(cmd_str):
        Logger.get_logger().(f"Process {os.getpid()} is running")
        os.system(cmd_str)

    def start_shell_training(self, cmd_strs):
        self.training_pool = Pool(len(cmd_strs))
        self.training_pool.map(TrainingManager.shell_training, cmd_strs)
        self.training_pool.close()
        self.training_pool.join()
    
    def start_api_training(self, entry, arg_list):
        self.training_pool = Pool(arg_list)
        self.training_pool.map(entry, arg_list)
        self.training_pool.close()
        self.training_pool.join()

