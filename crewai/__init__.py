class Agent:
    def __init__(self, **kwargs):
        pass

class Task:
    def __init__(self, description, agent):
        self.description = description
        self.agent = agent

class Crew:
    def __init__(self, agents, tasks, process):
        self.agents = agents
        self.tasks = tasks
        self.process = process
        self.inputs = {}

    def kickoff(self):
        return "ok"

class Process:
    sequential = "sequential"
