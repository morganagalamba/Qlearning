import numpy as np
import random
import connection as cn


class State:
    def __init__(self, turn_left: str, turn_right: str, jump: str):
        self.turn_left = float(turn_left)
        self.turn_right = float(turn_right)
        self.jump = float(jump)


class File_wrapper:
    def __init__(self, path="./resultado.txt") -> None:
        self.path = path

    def get_matrix(self):
        with open(self.path, "r") as f:
            content = f.readlines()
            states = [line.strip().split() for line in content]

            matrix = [State(state[0], state[1], state[2]) for state in states]
            return matrix

    def update_matrix(self, matrix: list[State]):
        with open(self.path, "w") as f:
            patch = ""
            for state in matrix:
                text = (
                    f"{state.turn_left:.6f} {state.turn_right:.6f} {state.jump:.6f}\n"
                )

                patch += text

            f.write(patch)


class Agent:
    def __init__(self) -> None:
        self.actions = ["left", "right", "jump"]

    def get_action(self, matrix: list[State], state: str) -> str:
        range = random.randint(0, 12)
        agent_state = int(state, 2)

        if range > 8:
            agent_state_value = matrix[agent_state]
            action = max(
                agent_state_value.turn_left,
                agent_state_value.turn_right,
                agent_state_value.jump,
            )

            if action == agent_state_value.turn_left:
                return self.actions[0]  # turn left

            elif action == agent_state_value.turn_right:
                return self.actions[1]  # turn right

            else:
                return self.actions[2]  # jump

        return self.actions[random.randint(0, 2)]

    def q_algorithm(
        self, matrix: list[State], state: str, last_state: str, action: str, reward: int
    ) -> list[State]:
        q_max = 0
        agent_state = int(state, 2)
        agent_last_state = int(last_state, 2)

        line_state = matrix[agent_state]
        q_max = max(line_state.turn_left, line_state.turn_right, line_state.jump)

        if action == "jump":
            matrix[agent_last_state].jump += 0.6 * (
                (reward + 0.42 * q_max) - matrix[agent_last_state].jump
            )
        elif action == "left":
            matrix[agent_last_state].turn_left += 0.6 * (
                (reward + 0.42 * q_max) - matrix[agent_last_state].turn_left
            )
        else:
            matrix[agent_last_state].turn_right += 0.6 * (
                (reward + 0.42 * q_max) - matrix[agent_last_state].turn_right
            )

        return matrix


class Controller:
    def __init__(self, Wrapper: File_wrapper) -> None:
        self.socket = cn.connect(2037)
        self.matrix_loader = Wrapper
        self.agent = Agent()

    def start_controller(self):
        matrix = self.matrix_loader.get_matrix()
        last_state = "000000"

        estudante_merecia_salario = True
        while estudante_merecia_salario:
            action = self.agent.get_action(matrix, last_state)
            print(action)
            state, reward = cn.get_state_reward(self.socket, action)
            matrix = self.agent.q_algorithm(matrix, state, last_state, action, reward)
            last_state = state
            self.matrix_loader.update_matrix(matrix)


if __name__ == "__main__":
    wrapper = File_wrapper()
    matrix = wrapper.get_matrix()
    matrix[0].jump = 1
    wrapper.update_matrix(matrix)

ctrl = Controller(File_wrapper())
ctrl.start_controller()
