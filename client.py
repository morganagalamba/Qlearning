import numpy as np
import random
import connection as cn

# Definir parâmetros do ambiente
num_states = 96 # número de estados possíveis
num_actions = 3 # número de ações possíveis
q_table = np.zeros((num_states, num_actions)) # tabela Q

# Define the possible actions
actions = ["jump", "right", "left"]

# Configurar parâmetros do algoritmo
epsilon = 0.9 # taxa de exploração
discount_factor = 0.9 # fator de desconto
learning_rate = 0.1 # taxa de aprendizagem
num_episodes = 1000 # número de episódios

# Definir a função de atualização da tabela Q
def update_q_table(state, action, reward, next_state):
    next_state = int(next_state,2)
    state = int(state,2)
    print(state)
    action = float(action)
    q_next = np.max(q_table[next_state]) # valor Q do próximo estado
    q_table[state, action] += learning_rate * (reward + discount_factor * q_next - q_table[state, action])

# Iniciar o treinamento do agente
s = cn.connect(2037)
for episode in range(num_episodes):
    # Definir o estado inicial aleatório do jogo
    state = random.randint(0, num_states-1)
    next_state = '000000'
    done = False # flag para verificar se o episódio terminou
    while not done:
        # Selecionar uma ação
        action = random.choice(actions)
        print(action)
       
        # Executar a ação e obter o próximo estado e recompensa
        #next_state = int(state) + 1
        state, reward = cn.get_state_reward(s,action)        
       
        # Atualizar a tabela Q
        update_q_table(state, action, reward, next_state)
        
        # Atualizar o estado atual do jogo
        next_state = state

        # Verificar se o episódio terminou
        done = (state == 95)
    print(episode)


# ler tabela Q
with open('resultado.txt', 'w') as f:
    for row in q_table:
        for val in row:
            f.write(str(val) + ' ')
        f.write('\n')