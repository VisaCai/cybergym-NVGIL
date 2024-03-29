
import sys
sys.path.append("/home/kalic/Desktop/AI_P/CyberBattleSim")
import logging
import gym
import pickle
import cyberbattle.agents.baseline.learner as learner
import cyberbattle.agents.baseline.plotting as p
import cyberbattle.agents.baseline.agent_wrapper as w
import cyberbattle.agents.baseline.agent_randomcredlookup as rca
import cyberbattle.agents.baseline.agent_tabularqlearning as tqa
import cyberbattle.agents.baseline.agent_dql as dqla
from cyberbattle.agents.baseline.agent_wrapper import Verbosity

logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format="%(levelname)s: %(message)s")

# Papermill notebook parameters

#############
gymid = "network4-v0"
env_size = None
iteration_count = 1500
training_episode_count = 10
eval_episode_count = 10
maximum_node_count = 12
maximum_total_credentials = 10

# Load the Gym environment
if env_size:
    gym_env = gym.make(gymid)
else:
    gym_env = gym.make(gymid)

ep = w.EnvironmentBounds.of_identifiers(
    maximum_node_count=maximum_node_count,
    maximum_total_credentials=maximum_total_credentials,
    identifiers=gym_env.identifiers
)



state = "not_random"
os_type = ["Windows", "Ubuntu", "Windows", "Ubuntu", "Windows", "Windows", "Windows", "Windows", "Windows", "Windows"]
Local_vulnerabilities = [[], ["CVE-2017-16995"], ["CVE-2009-0079"], ["CVE-2017-16995"], ["MS15-015"], [], [], [], [], []]
Remote_vulnerabilities = [[], ["CVE-2019-2729"], ["S2-048"], [], ["CNVD-2019-32204"], ["MS17-010"], ["MS17-010"], ["MS08-067"], ["CVE-2019-0708"],["MS09-050"]]
node_values = [0, 50, 30, 60, 60, 50, 50, 50, 300, 1000]
topology_graph = {"0":["1","2"], "1":["3"],"3":["4","5","6","7","8"], "4":["5","6","7","8"], "5":["6","7","8"], "6":["7", "8"], "7":["8"], "8":["9"]}
network1 = gym.make(gymid, state = state, os_type = os_type, Local_vulnerabilities = Local_vulnerabilities, Remote_vulnerabilities = Remote_vulnerabilities, node_values = node_values, topology_graph = topology_graph)


state = "not_random"
os_type = ["Ubuntu", "Ubuntu", "Windows", "Ubuntu", "Windows", "Windows", "Windows", "Windows", "Windows", "Ubuntu"]
Local_vulnerabilities = [[], ["CVE-2017-16995"], ["CVE-2009-0079"], ["CVE-2017-16995"], ["MS15-015"], ["MS16-111"], ["CVE-2009-0079"], [], [], ["CVE-2022-0847"]]
Remote_vulnerabilities = [[], ["CVE-2019-2729"], ["S2-048"], [], ["CNVD-2019-32204"], ["MS17-010"], ["MS17-010"], ["MS08-067"], ["CVE-2019-0708"],["S2-048"]]
node_values = [0, 30, 50, 60, 60, 100, 20, 300, 50, 1000]
topology_graph = {"0":["1", "2"],"1":["3"],"3":["5"] , "5":["7","8"],"7":["9"],"2":["4"], "4":["6"], "6":["8"]}
network2 = gym.make(gymid, state = state, os_type = os_type, Local_vulnerabilities = Local_vulnerabilities, Remote_vulnerabilities = Remote_vulnerabilities, node_values = node_values, topology_graph = topology_graph)


os_type = ["Windows", "Ubuntu", "Windows", "Ubuntu", "Windows", "Windows", "Windows", "Windows", "Windows", "Windows"]
Local_vulnerabilities = [[], ["CVE-2017-16995"], ["CVE-2009-0079"], ["CVE-2017-16995"], ["MS15-015"], ["MS16-111"], ["CVE-2009-0079"], [], ["CVE-2009-0079"], []]
Remote_vulnerabilities = [[], ["CVE-2019-2729"], ["S2-048"], [], ["CNVD-2019-32204"], ["MS17-010"], ["MS17-010"], ["MS08-067"], ["CVE-2019-0708"],["MS09-050"]]
node_values = [0, 70, 50, 100, 60, 200, 50, 100, 500, 100]
topology_graph = {"0":["3"], "3":["1", "2", "6"], "2":["9"], "1":["4"], "5":["7", "8"], "6":["8"]}
network3 = gym.make(gymid, state = state, os_type = os_type, Local_vulnerabilities = Local_vulnerabilities, Remote_vulnerabilities = Remote_vulnerabilities, node_values = node_values, topology_graph = topology_graph)
# topology_graph = {(0,3),(3,1),(3,2),(3,6),(2,9),(1,4),(4,7),(5,7),(5,8),(6,8)}


os_type = ["Windows", "Ubuntu", "Windows", "Ubuntu", "Windows", "Windows", "Windows", "Windows", "Windows", "Windows"]
Local_vulnerabilities = [[], [], ["CVE-2009-0079"], ["CVE-2017-16995"], ["MS15-015"], ["MS16-111"], ["CVE-2009-0079"], [], ["CVE-2019-0708"], []]
Remote_vulnerabilities = [[], ["CVE-2019-2729"], ["S2-048"], [], ["CNVD-2019-32204"], [], ["MS17-010"], ["MS08-067"], ["MS16-111"],[]]
node_values = [0, 30,50,60,60,100,100,200,200,600]
topology_graph = {"0":["3"], "3":["1"], "4":["2", "6"], "2":["5"], "6":["8"], "5":["7"], "8":["7","9"]}
network4 = gym.make(gymid, state = state, os_type = os_type, Local_vulnerabilities = Local_vulnerabilities, Remote_vulnerabilities = Remote_vulnerabilities, node_values = node_values, topology_graph = topology_graph)
# topology_graph = {(0,3),(3,1),(4,2),(4,6),(2,5),(6,8),(5,7),(8,7),(8,9)}

Network_List = [network1, network2, network3, network4]

gym_env_for_train = gym.make(gymid, state = 'not_random', os_type = [], Local_vulnerabilities = [], Remote_vulnerabilities = [], node_values = [], topology_graph = set())



for j in range(4):
    # Evaluate the Deep Q-learning agent
    dql_run = learner.epsilon_greedy_search(
        cyberbattle_gym_env=Network_List[j],
        environment_properties=ep,
        learner=dqla.DeepQLearnerPolicy(
            ep=ep,
            gamma=0.015,
            replay_memory_size=10000,
            target_update=10,
            batch_size=512,
            # torch default learning rate is 1e-2
            # a large value helps converge in less episodes
            learning_rate=0.01
        ),
        # episode_count=training_episode_count,
        # iteration_count=iteration_count,
        # epsilon=0.90,
        # epsilon_exponential_decay=5000,
        # epsilon_minimum=0.10,
        # verbosity=Verbosity.Quiet,
        # render=False,
        # plot_episodes_length=False,
        episode_count=eval_episode_count,
        iteration_count=iteration_count,
        epsilon=0.0,
        epsilon_minimum=0.00,
        render=False,
        plot_episodes_length=False,
        verbosity=Verbosity.Quiet,
        title="DQL-Random"
    )
    filenamei = './Network4_results/dql_random_run' + 'network' + str(j+1) + '.pkl'
    with open(filenamei,'wb') as file:
        pickle.dump(dql_run, file)
    

