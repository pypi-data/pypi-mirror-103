import itertools
import os
from configparser import ConfigParser


class ConfigNode:
    """Class to store node names and parent/children relationships"""

    def __init__(self, name):
        """Initializeds the ConfigNode class

        Args: a name for the node
        """
        self.name = name
        self.children = set()
        self.parents = set()
        self.type = None
        # remove the children suffix. This makes things easier in the long run
        if name.endswith(":children"):
            self.name = name.replace(":children", "")

    def get_children(self):
        """Return the set of children for this node."""
        return self.children

    def has_children(self):
        if self.children:
            return True
        return False

    def add_child(self, child):
        """Add a child to this nodes children."""
        self.children.add(child)

    def get_parents(self):
        """Return the set of parents for this node."""
        return self.parents

    def add_parent(self, parent):
        """Add a parent to this nodes parents."""
        self.parents.add(parent)

    def get_ancestors(self, ancestors):
        """Return a list of ancestors of this node"""
        for p in self.get_parents():
            ancestors.append(p)
            p.get_ancestors(ancestors)
        return ancestors

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class ConfigTree:

    def __init__(self, path=None):
        self.cfg = ConfigParser(allow_no_value=True)
        if path:
            self.cfg.read(path)
        self.root = set()
        self.nodes = set()
        self.add_nodes()
        self._build_tree()

    def add_nodes(self):
        """Add all nodes to the tree."""
        for sec in self.cfg.sections():
            node = ConfigNode(sec)
            if not self.get_node(node.name):
                self.nodes.add(node)
            for option in self.cfg.options(sec):
                child_node = ConfigNode(option)
                if not self.get_node(child_node.name):
                    self.nodes.add(child_node)

    def get_node(self, name):
        """Find node in this tree"""
        for n in self.nodes:
            if n.name == name:
                return n
        return None

    def _build_tree(self):
        """Iterate through all of the sections, and build each parent-child relationship for each node."""
        for sec in self.cfg.sections():
            tmp_sec = sec
            if sec.endswith(":children"):
                tmp_sec = sec.replace(":children", "")
            # in this context, the section is always the parent node
            parent_node = self.get_node(tmp_sec)
            parent_node.type = 'internal'
            self.root.add(parent_node)
            for option in self.cfg.options(sec):
                child_node = self.get_node(option)
                parent_node.add_child(child_node)
                child_node.add_parent(parent_node)
                if child_node.has_children():
                    child_node.type = 'internal'
                else:
                    child_node.type = 'edge'
            # remove any of this parents children.
            tmp_root = self.root.copy()
            for node in tmp_root:
                if node in parent_node.get_children():
                    self.root.remove(node)


class PlaybookLimit:

    def __init__(self, hosts_path=None):
        self.ct = ConfigTree(hosts_path)

    def infer_playbook_limit(self, file_paths):
        """Given a list of file paths, return the list of 'ansible inventory groups or hosts' that can be inferred
        from those file paths. As an example, assume the only filepath provided is `inventory/group_vars/databases/config.yaml`
        then the output will simply be `databases`.

        Args:
            file_paths (List[strings]): A list of filepaths to be parsed to determine the playbook limit.
        """
        limits = set()
        for changed_file_path in file_paths:
            split_file_path = changed_file_path.split(os.path.sep)
            # Looking for paths that are of format "inventory/[host_vars|group_vars]/{targeted_host}"
            if len(split_file_path) < 3:
                continue
            if split_file_path[0] == 'inventory' and (
                    split_file_path[1] == 'group_vars' or split_file_path[1] == 'host_vars'):
                limits.add(split_file_path[2].strip())

        return self._optimize_limits(limits)

    def _optimize_limits(self, limits):
        """Optimize the limits provided.

        :param limits: The playbook limit to be optimized.
        :return: The optimized playbook limit.

        Discussion: This happens in two phases.
        1. First iterate through each limit and compare it to all other limits.
            1. If a common ancestor is found that is in the current list of limit, mark the current limit for removal.
            2. Or, if the current limit is an only child, add the parent to the only_child_parent set and add to limits after
                interation.
        2. For the remaining limits, find their lowest common ancestor, then check to see if the children of that ancestor
        are a subset of the current limits.

        """
        # phase 1
        changes_made = True
        while changes_made:
            to_be_removed = set()
            only_child_parents = set()
            for l in limits:
                l_ancestors = set([a.name for a in self.ct.get_node(l).get_ancestors([])])
                if limits.intersection(l_ancestors):
                    to_be_removed.add(l)
                # corner case where an edge node as a single parent and no siblings
                else:
                    l_node = self.ct.get_node(l)
                    for l_a in l_ancestors:
                        if set([l_node]) == self.ct.get_node(l_a).get_children():
                            to_be_removed.add(l)
                            only_child_parents.add(l_a)
            limits = limits.union(only_child_parents)

            # phase2
            # iterate through all possible combinations.
            best_parent = None
            for a, b in itertools.combinations(limits, 2):
                # only compare parents.
                a_parents = self.ct.get_node(a).get_parents()
                b_parents = self.ct.get_node(b).get_parents()
                for a_p in a_parents:
                    for b_p in b_parents:
                        if a_p == b_p:
                            # don't add parents that have no ancestors.
                            if limits.issuperset(set([c.name for c in a_p.get_children()])) and len(
                                    a_p.get_parents()) > 0:
                                best_parent = a_p

                if best_parent:
                    # mark children for removal
                    to_be_removed.add(a)
                    to_be_removed.add(b)
                    # add ancestor to limits.
                    limits.add(best_parent.name)
                    best_parent = None
            if not to_be_removed:
                changes_made = False
            else:
                limits -= to_be_removed
                changes_made = True
        return limits
