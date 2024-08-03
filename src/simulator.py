import random
import logging
import time
from graph import AttackGraph, AttackStep
from generator import AttackGraphGenerator
from attacker import Attacker
from itertools import combinations
from bcolors import bcolors
 
class Simulator:
    def __init__(self, graph_type='random', graph_size=10, random_links=3):
        logging.info(f"{bcolors.OKBLUE}\nOriginal graph{bcolors.ENDC}")
        generator = AttackGraphGenerator()
        if graph_type == 'random':
            self.graph = generator.random_graph(size=graph_size, random_links=random_links)
        elif graph_type == 'test1': 
            self.graph = generator.test_graph_1()
        elif graph_type == 'test2': 
            self.graph = generator.test_graph_2()
        else:
            raise Exception("That graph name is not among the options.")
       
        self.graph.log_attack_steps(include_parents=True, include_children=True, include_ttc=True)
        self.graph.write_pdf(filename='original_graph')

    def initialize_unexplored_origins(self, n_attackers, max_attack_origins, method):
        self.unexplored_origins = list()
        if method == 'sequential':
            while len(self.unexplored_origins) < n_attackers:
                for i in range(1, max_attack_origins + 1):
                    self.unexplored_origins += sorted([set(uo) for uo in combinations(self.graph.attack_steps, i)])
            logging.debug(f"Positioning the attacker sequentially in the following {len(list(combinations(self.graph.attack_steps, i)))} starting points:\n")
            for uo in self.unexplored_origins:
                logging.log(5, [o.name for o in uo])
        if method == 'random':
            for i_attacker in range(0, n_attackers):
                origin_set = set()
                for i_origin in range (0, max_attack_origins):
                    origin_set.add(random.choice(sorted(self.graph.attack_steps)))
                self.unexplored_origins.append(origin_set)    


    def simulate(self, n_attackers=10000, attack_time=5000, max_attack_origins=2, attack_strategy='attack_any_uncompromised', origins_method='sequential'): 
        self.initialize_unexplored_origins(n_attackers, max_attack_origins, origins_method)
        self.attacker = Attacker(self.graph, attack_strategy, attack_time, self.unexplored_origins)

        self.explored_origins = set()
        logging.debug(f"\nCollecting traces from {n_attackers} attackers randomly traversing the graph.")
        start = time.time()
        log_time = start
        for lap in range(1, n_attackers+1):
            logging.log(5, f"Lap {lap}")
            n_attack_origins = random.randrange(1, max_attack_origins + 1)
            attack_origins = self.attacker.set_origins(n_attack_origins)
            self.explored_origins.add(frozenset([o.name for o in attack_origins]))
            self.attacker.attack()
            current = time.time()
            mean_lap = (current-start)/lap
            if current - log_time > 5:
                logging.info(f"Simulation lap {lap} = {current-start:.0f}s. Remaining = {(n_attackers - lap)*mean_lap:.0f}s")
                log_time = current

        logging.debug(f"\nStates explored as origins: {[list(o) for o in self.explored_origins]}")
        self.attacker.log_experience()
        return self.attacker.experience

