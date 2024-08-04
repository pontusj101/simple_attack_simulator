import random
import numpy as np
import logging
from .graph import AttackGraph, AttackStep

class AttackGraphGenerator:
    def __init__(self):
        self.name_number = 0

    def test_graph_1(self):
        graph = AttackGraph('test_graph_1')
        k = AttackStep('K', graph, step_type='or', ttc=150)
        j = AttackStep('J', graph, step_type='and', ttc=70, children=set([k]))
        i = AttackStep('I', graph, step_type='unknown', ttc=90, children=set([j]))
        h = AttackStep('H', graph, step_type='unknown', ttc=15, children=set([j]))
        g = AttackStep('G', graph, step_type='unknown', ttc=30, children=set([j]))
        f = AttackStep('F', graph, step_type='and', ttc=20, children=set([k]))
        e = AttackStep('E', graph, step_type='or', ttc=120, children=set([f]))
        d = AttackStep('D', graph, step_type='unknown', ttc=50, children=set([f, g, h]))
        c = AttackStep('C', graph, step_type='unknown', ttc=100, children=set([e]))
        b = AttackStep('B', graph, step_type='unknown', ttc=10, children=set([e]))
        a = AttackStep('A', graph, step_type='unknown', ttc=30, children=set([b, c, d, i]))

        graph.attack_steps = set([a, b, c, d, e, f, g, h, i, j, k])

        return graph

    def test_graph_2(self):
        name='test_graph_2'
        a1 = AttackStep('A1', step_type='unknown')
        a2 = AttackStep('A2', step_type='unknown')
        a3 = AttackStep('A3', step_type='and')
        a4 = AttackStep('A4', step_type='unknown')
        a5 = AttackStep('A5', step_type='unknown')
        
        a1.add_child(a2)
        a1.add_child(a4)
        a1.add_child(a5)
        a2.add_child(a3)
        a3.add_child(a1)
        a4.add_child(a3)
        a5.add_child(a3)

        graph = AttackGraph(name)
        graph.attack_steps = set([a1, a2, a3, a4, a5])

        return graph

    def random_type(self):
        return random.choice(['or', 'or', 'and'])

    def random_name(self):
        self.name_number += 1
        return f"A{self.name_number}"

    def random_graph(self, name='random_graph', size=100, random_links=100, mean_ttc=10):
        graph = AttackGraph(name)
        for step in range(0, size):
            ttc = int(np.random.exponential(scale=mean_ttc)) + 1
            step = AttackStep(self.random_name(), graph, step_type=self.random_type(), ttc=ttc)
            if graph.attack_steps:
                parent = random.choice(sorted(graph.attack_steps))
                graph.attack_steps.add(step)
                step.add_parent(parent)
            graph.attack_steps.add(step)
        for link_number in range(0,random_links):
            parent = random.choice(sorted(graph.attack_steps))
            child = random.choice(sorted(graph.attack_steps-set([parent])))
            child.add_parent(parent)
        graph.update_step_type_when_single_parent()
        return graph
                    
