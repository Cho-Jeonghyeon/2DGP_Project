class StateMachine:
    def __init__(self, start_state):
        self.current_state = start_state

    def update(self):
        self.current_state.do()

    def draw(self):
        self.current_state.draw()