import argparse
import logging
import random
import numpy as np
from experimenter import Experimenter
 
parser = argparse.ArgumentParser(description="This program attempts to (re)learn attack graphs from attack traces created by random attackers wandering about randomly generated graphs.")

parser.add_argument('--graph', type=str, default='random', choices=['random', 'test1', 'test2'], help="The attack graph to explore.")
parser.add_argument('--n_attackers', type=int, default=10000, help="The number of attackers.")
parser.add_argument('--attack_time', type=int, default=5000, help="The mean time an attacker spends on an attack step.")
parser.add_argument('--attack_origins', type=int, default=3, help="The maximum number of attack steps that the attacker controls at the start of each simulation. The actual number will be randomized between 1 and the provided value.")
parser.add_argument('--attack_origins_method', type=str, default='sequential', choices=['sequential', 'random'], help="At the start of an attack, the attacker will control a certain set of attack steps. With the random origins method, those steps will be selected based on chance. With the sequential origins method, all possible attack step combinations of size --attack_origins and less will be exhausted in sequential order.")
parser.add_argument('--attack_strategy', type=str, default='attack_any_uncompromised', choices=['attack_any_uncompromised', 'attack_only_possible'], help="The strategy the attacker employs. attack_only_possible is constrained to attempting attacks on children of compromised attack steps. attack_any_uncompromised may attempt any attack step, but will of course fail with certainty if the step is not among the possible.")
parser.add_argument('--graph_size', type=int, default=-1, help="The number of attack steps in the attack graph (will override min_graph_size and max_graph_size.")
parser.add_argument('--min_graph_size', type=int, default=5, help="The number of attack steps in the smallest attack graph, when assessing comutational complexity.")
parser.add_argument('--max_graph_size', type=int, default=5, help="The number of attack steps in the largest attack graph, when assessing computational complexity.")
parser.add_argument('--random_links', type=int, default=3, help="The number of random edges between vertices in addition to a basic tree structure.")
parser.add_argument('--loglevel', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="The level of logs to print to console.")
parser.add_argument('--loglevel_numeric', type=int, default=-1, help="The numeric level of logs to print to console (as a more granular alternative to the --loglevel flag), 0-100. DEBUG = 10, INFO = 20, etc")
parser.add_argument('--experiments', type=int, default=1, help="The number of experiments to run. One experiment consists of --n_attackers number of simulations. Will break when inference fails.")
parser.add_argument('--simulation_batch_size', type=int, default=100, help="The number of attackers to collect experiencees from between inference attempts.")
parser.add_argument('--random_seed', type=int, default=-1, help="Random seed.")

if __name__ == "__main__":

    args = parser.parse_args()

    if not args.random_seed < 0:
        random.seed(args.random_seed)
        np.random.seed(args.random_seed)

    if args.loglevel_numeric == -1:
        numeric_loglevel = getattr(logging, args.loglevel.upper(), None)
    else:
        numeric_loglevel = args.loglevel_numeric
    logging.getLogger("graphviz").setLevel(logging.WARNING)
    logging.basicConfig(format='%(message)s', level=numeric_loglevel)

    min_graph_size = args.min_graph_size
    max_graph_size = args.max_graph_size
    if args.graph_size > 1:
        min_graph_size = args.graph_size
        max_graph_size = args.graph_size

    experimenter = Experimenter()
    experimenter.experiment(args.experiments, args.graph, min_graph_size, max_graph_size, args.random_links, args.n_attackers, args.attack_time, args.attack_origins, args.attack_strategy, args.attack_origins_method, init_simulation_batch_size=args.simulation_batch_size)

