import random
import numpy as np
import logging
import graphviz
from bcolors import bcolors

class AttackStep:
    def __init__(self, name, graph, step_type='unknown', ttc=None, children=None):
        self.step_type = step_type
        self.name = name
        self.graph = graph
        if ttc:
            self.ttc = ttc
        else:
            self.ttc = -1
        self.parents = set()
        self.children = set()
        if children:
            for child in children:
                self.add_child(child)

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name

    def is_equal(self, other, ttc_error_margin):
        if self.step_type == other.step_type and self.name == other.name:
            if set([p.name for p in self.parents]) == set([o.name for o in other.parents]):
                if set([p.name for p in self.children]) == set([o.name for o in other.children]):
                    if abs(self.ttc - other.ttc) <= ttc_error_margin:
                        return True
        return False

    def mean_ttc(self):
        return self.ttc

    def add_child(self, child):
        if child not in self.children:
            self.children.add(child)
            child.parents.add(self)

    def add_parent(self, parent):
        if parent not in self.parents:
            self.parents.add(parent)
            parent.children.add(self)

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)
            child.parents.remove(self)

    def remove_parent(self, parent):
        if parent in self.parents:
            self.parents.remove(parent)
            parent.children.remove(self)

    def log_me(self, include_id=False, include_ttc=False, include_type=True, include_parents=False, include_children=True):
        self_string = f"{self.name} " 
        type_string = f"({self.step_type}) " 
        parent_string = f"{[step.name for step in self.parents]} --> "
        ttc_string = f"[{self.ttc:.1f}] "
        child_string = f"--> {[step.name for step in self.children]}"
        id_string = f"id: {hex(id(self))} "
        log_string = ""
        if include_id:
            log_string += "dfsfd "
            log_string += id_string 
        if include_parents:
            log_string += parent_string 
        log_string += self_string
        if include_type:
            log_string += type_string
        if include_ttc:
            log_string += ttc_string
        if include_children:
            log_string += child_string
        logging.info(log_string)


class AttackGraph:
    def __init__(self, name):
        self.name = name
        self.attack_steps = set([])

    def get_attack_step(self, name):
        return next(iter([step for step in self.attack_steps if step.name == name]))

    def log_attack_steps(self, include_ip=False, include_parents=False, include_ttc=False, include_type=False, include_children=True):
        for step in self.attack_steps:
            step.log_me(include_id=include_ip, include_parents=include_parents, include_ttc=include_ttc, include_children=include_children)

    def orphans(self):
        o = set()
        for a in self.attack_steps:
            if not a.parents:
                o.add(a)
        return o

    def compare(self, other, ttc_error_margin = 1.0):
        logging.info(f"{bcolors.OKBLUE}\nComparing {self.name} with {other.name}{bcolors.ENDC}")
        is_different = False
        if len(self.attack_steps) != len(other.attack_steps):
            logging.info(f"The graphs have different numbers of attack steps: {self.name} has {len(self.attack_steps)} steps, while {other.name} has {len(other.attack_steps)} steps.\n")
            is_different = True
        for a in self.attack_steps:
            for b in other.attack_steps:
                if a.name == b.name:
                    if not a.is_equal(b, ttc_error_margin=ttc_error_margin):
                        is_different = True
                        logging.info(f"{self.name}.{a.name} == {other.name}.{b.name} --> {a == b}")
                        a.log_me(include_parents=True, include_ttc=True, include_type=True, include_children=True)
                        b.log_me(include_parents=True, include_ttc=True, include_type=True, include_children=True)
        if is_different:
            logging.info(f"{bcolors.FAIL}The graphs differ.{bcolors.ENDC}\n")
            return False
        else:
            logging.info("The graphs are identical.\n")
            return True
        
    def write_pdf(self, filename='graph'):
        g = graphviz.Digraph('G', filename=f'{filename}.dot')
        for parent in self.attack_steps:
            g.node(f"{parent.name} ({parent.step_type})")
            for child in parent.children:
                g.edge(f"{parent.name} ({parent.step_type})", f"{child.name} ({child.step_type})")
        filepath = f"/root/files/{filename}"
        logging.debug(f'\nWriting graph file to {filepath}')
        g.render(filepath, format="pdf")

    # Attack steps with single parents could be either AND or OR attack steps, so make sure that they are marked as 'unknown'.
    def update_step_type_when_single_parent(self):
        for step in self.attack_steps:
            if len(step.parents) < 2:
                step.step_type = 'unknown'

