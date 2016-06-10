from django.db import models

class CareTaker():
    def push_item(self, state):
        self.memento_stack.append(state)

    def rollback_memento(self):
        return self.memento_stack.pop()

class Memento():
    pass
