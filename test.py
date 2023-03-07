# Aqui vocês irão colocar seu algoritmo de aprendizado
import connection as cn
from random import randint
from connection import connect, get_state_reward


class State:
    def __init__(self, left: str, right: str, jump: str):
        self.left = float(left)
        self.right = float(right)
        self.jump = float(jump)


class GameController:
    def __init__(self):
        self.__matrix_loader = Matrix()
        self.__agent = QAgent()
        self.__start_connection_with_qlearning_app()

    def __start_connection_with_qlearning_app(self):
        self.__socket = connect(2037)

    def start_controller(self):
        matrix = self.__matrix_loader.get_matrix()
        last_state = "000000"
        while True:
            action = self.__agent.get_action(matrix, last_state)
            print(action)
            state, reward = get_state_reward(self.__socket, action)

            print(set)
            matrix = self.__agent.q_algorithm(matrix, state, last_state, action, reward)
            last_state = state
            self.__matrix_loader.update_matrix(matrix)


class QAgent:

    ACTIONS = ["left", "right", "jump"]

    def __init__(self):
        print("10")

    def get_action(self, matrix: list[State], state: str) -> str:
        exploration = randint(0, 12)
        agent_state = int(state, 2)

        if exploration > 8:
            agent_state_value = matrix[agent_state]
            action_value = max(
                agent_state_value.left, agent_state_value.right, agent_state_value.jump
            )

            if action_value == agent_state_value.left:
                return "left"
            elif action_value == agent_state_value.right:
                return "right"
            return "jump"

        return QAgent.ACTIONS[randint(0, 2)]

    def q_algorithm(
        self, matrix: list[State], state: str, last_state: str, action: str, reward: int
    ) -> list[State]:
        q_max = 0
        agent_state = int(state, 2)
        agent_last_state = int(last_state, 2)

        line_state = matrix[agent_state]
        q_max = max(line_state.left, line_state.right, line_state.jump)

        if action == "jump":
            matrix[agent_last_state].jump += 0.6 * (
                (reward + 0.42 * q_max) - matrix[agent_last_state].jump
            )
        elif action == "left":
            matrix[agent_last_state].left += 0.6 * (
                (reward + 0.42 * q_max) - matrix[agent_last_state].left
            )
        else:
            matrix[agent_last_state].right += 0.6 * (
                (reward + 0.42 * q_max) - matrix[agent_last_state].right
            )

        return matrix


class Matrix:

    FILE_CONTENT = "./resultado.txt"
    NUMBER_PRECISION = 4

    def get_matrix(self):
        with open(Matrix.FILE_CONTENT, "r") as file:
            text = file.readlines()
            states = [line.strip().split() for line in text]

            for state in states:
                print(state)

            matrix = [State(state[0], state[1], state[2]) for state in states]
            return matrix

    def update_matrix(self, matrix: list[State]):
        with open(Matrix.FILE_CONTENT, "w") as file:
            new_states = ""
            for state in matrix:
                new_states += f"{state.left:.6f} {state.right:.6f} {state.jump:.6f}\n"
            file.write(new_states)


if __name__ == "__main__":
    matrix_loader = Matrix()
    matrix = matrix_loader.get_matrix()
    matrix[0].left = 1
    matrix_loader.update_matrix(matrix)


gameController = GameController()
gameController.start_controller()
