from FileData import FileData
from Service import Service

class Problem(object):
    def __init__(self, problem : str):
        self.services = list()
        self.problem = problem

    def addService(self, filedata : FileData):
        for x in self.services:
            if x.service == filedata.service:
                x.addGoal(filedata)
                return

        t = Service(filedata.service)
        t.addGoal(filedata)
        self.services.append(t)