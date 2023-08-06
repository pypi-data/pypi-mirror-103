# ##### BEGIN GPL LICENSE BLOCK #####
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


import collections
import logging
from .data import DataTranslationProtocol, ReplicatedDatablock
from .constants import HEAD


class GraphObjectStore(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __repr__(self):
        str = "\n"
        for key, item in self.store.items():
            str += repr(item)
        return str


class Repository():
    """
    Structure responsible for replication graph manipulation
    """

    def __init__(self, data_protocol: DataTranslationProtocol = None, *args, **kwargs):
        self.object_store = GraphObjectStore()
        self.data_protocol = data_protocol
        self._roots = []

    def add_root(self, node_id):
        logging.info(f"Adding node {node_id} to  roots")
        self._roots.append(node_id)

    def remove_root(self, node_id):
        if node_id in self.object_store[HEAD]:
            self._roots.remove(node_id)

    def list(self, filter_state=None, filter_type=None):
        if filter_state:
            return [key for key, item in self.object_store.items()
                    if item.state == filter_state]
        if filter_type:
            return [key for key, item in self.object_store.items()
                    if isinstance(item, filter_type)]
        return [key for key, item in self.object_store.items()]

    def get_dependencies(self, node, deps=[]):
        node_ref = self.get_node(node)

        if node_ref and node_ref.dependencies:
            for child in node_ref.dependencies:
                if child not in deps:
                    deps.append(child)
                self.get_dependencies(child, deps)

    def get_node(self, uuid):
        return self.object_store.get(uuid,None)

    def get_node_by_datablock(self, datablock, default=None):
        for v in self.object_store.values():
            if not v.instance:
                continue
            if datablock == v.instance:
                return v
        return default

    def get_parents(self, child):
        parents = []
        for node in self.object_store.values():
            if node.dependencies and child in node.dependencies:
                parents.append(node)

        return parents

    def bfs_from_node(self, start_node):
        visited = []
        queue = start_node

        while queue:
            current = queue.pop(0)

            if current not in visited:
                visited.append(current)
                current_ref = self.object_store.get(current)
                if current_ref and current_ref.dependencies:
                    queue.extend(current_ref.dependencies)

        return visited

    def list_ordered(self):
        return reversed(self.bfs_from_node(self._roots))

    def get_dependencies_ordered(self, node):
        assert(node)

        deps = []
        self.get_dependencies(node, deps=deps)

        return reversed(deps)

    def get_nodes_in_state(self, state=None):
        added_items = self.list(filter_state=state)
        selected_nodes = []

        for item in added_items:
            item_deps = []
            self.get_dependencies(item, deps=item_deps)

            for deps in item_deps:
                if deps not in selected_nodes and self.object_store[deps].state == state:
                    selected_nodes.append(deps)

            if item not in selected_nodes and self.object_store[item].state == state:
                selected_nodes.append(item)

        return selected_nodes

    def do_commit(self, node: ReplicatedDatablock):
        node_id = getattr(node, 'uuid', None)
        if node_id:
            if node_id in self.object_store:
                self.object_store[node_id].data = node.data
                self.object_store[node_id].state = node.state
                self.object_store[node_id].dependencies = node.dependencies
            else:
                self.object_store[node_id] = node