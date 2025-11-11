class StateMachine:
    def __init__(self, start_state, state_transitions):
        self.cur_state = start_state
        self.state_transitions = state_transitions
        # 상태의 enter는 event를 선택적으로 받도록 설계되어 있으므로 초기화 시에는 이벤트 없이 호출
        self.cur_state.enter()

    def update(self):
        self.cur_state.do()

    def handle_state_event(self, event):
        # 현재 상태에 대한 전이 테이블이 없으면 이벤트 처리 안 함
        if self.cur_state not in self.state_transitions:
            return

        for check_event in self.state_transitions[self.cur_state].keys():
            if check_event(event):
                self.cur_state.exit(event)
                self.next_state = self.state_transitions[self.cur_state][check_event]
                self.next_state.enter(event)
                self.cur_state = self.next_state
                return

    def draw(self):
        self.cur_state.draw()