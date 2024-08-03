import random
import numpy as np
import logging

class Attacker:
    def __init__(self, graph, strategy, time_to_spend_per_step, unexplored_origins=None):
        self.graph = graph
        self.strategy = strategy
        self.time_to_spend_per_step = int(np.random.exponential(scale=time_to_spend_per_step))
        self.experience = dict()
        self.unexplored_origins = unexplored_origins

    def set_origins(self, n=2, method='sequential'):
        self.compromised = self.unexplored_origins.pop()
        return self.compromised
        
    def is_reachable(self, attack_step):
        if not attack_step.parents:
            return False
        if attack_step in self.failed:
            return False
        if attack_step.step_type == 'and' or attack_step.step_type == 'unknown':
            for parent in attack_step.parents:
                logging.log(4, f"    {parent.name} is a parent {attack_step.name} ({attack_step.step_type}). It is {parent in self.compromised} that it has been compromised.")
                if parent not in self.compromised:
                    logging.log(4, f"    {attack_step.name} is not reachable.")
                    return False
            logging.log(4, f"    {attack_step.name} is reachable.")
            return True
        if attack_step.step_type == 'or':
            for parent in attack_step.parents:
                logging.log(4, f"    {parent.name} is a parent {attack_step.name} ({attack_step.step_type}). It is {parent in self.compromised} that it has been compromised.")
                if parent in self.compromised:
                    logging.log(4, f"    {attack_step.name} is reachable.")
                    return True
            logging.log(4, f"    {attack_step.name} is not reachable.")
            return False
            
    def reachable_steps(self):
        surface = []
        for compr in self.compromised:
            surface.extend([child for child in compr.children if self.is_reachable(child) and child not in self.compromised and child not in self.failed])
        return surface   
 
    def attack_surface(self):
        if self.strategy == 'attack_only_possible':
            return self.reachable_steps()
        elif self.strategy == 'attack_any_uncompromised':
            return self.graph.attack_steps - self.compromised - self.failed
        else:
            logging.error("Selected a non-existent attacker strategy")

    def step(self):
        attack_step = random.choice(sorted(self.attack_surface()))
        logging.log(5, f"  Attempting to compromise {attack_step.name}")
        attack_step_ttc = int(np.random.exponential(scale=attack_step.ttc))
        if self.is_reachable(attack_step) and self.time_to_spend_per_step > attack_step_ttc:
            success = True
            self.ttc += attack_step_ttc
            self.compromised.add(attack_step)
            logging.log(5, f"  Compromised {attack_step.name}")
        else:
            success = False
            self.ttc += self.time_to_spend_per_step
            self.failed.add(attack_step)
            logging.log(5, f"  Failed to compromise {attack_step.name}")
        return attack_step.name, self.ttc, attack_step_ttc, success

    def add_to_experience(self, attack_step_name, local_ttc, success):
        state = frozenset(self.state)
        if state not in self.experience:
            self.experience[state] = dict()
        if attack_step_name not in self.experience[state]:
            self.experience[state][attack_step_name] = []
        self.experience[state][attack_step_name].append((local_ttc, success))


    def attack(self):
        self.failed = set()
        self.ttc = 0
        self.state = set([c.name for c in self.compromised])
        logging.log(6, f"Initiating attack from {[s.name for s in self.compromised]}")
        while self.attack_surface():
            attack_step_name, global_ttc, local_ttc, success = self.step()
            if success:
                self.add_to_experience(attack_step_name, local_ttc, True)
                self.state.add(attack_step_name)
            else:
                self.add_to_experience(attack_step_name, local_ttc, False)
        return self.experience

    def log_experience(self):
        logging.log(5, "\nExperience:")
        for state, targets in self.experience.items():
            for target, attempts in targets.items():
                for attempt in attempts:
                    ttc, success = attempt
                    logging.log(5, f"{set(state)}-->{target} in {ttc} days. Successful: {success}")

