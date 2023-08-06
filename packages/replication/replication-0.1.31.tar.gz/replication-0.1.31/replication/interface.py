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


import copy
import gzip
import logging
import os
import pickle
import queue
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path

try:
    import _pickle as pickle
except ImportError:
    import pickle

import os
import queue
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

import zmq

from replication import __version__

from .constants import (ADDED, CLIENT_PING_FREQUENCY, COMMITED,
                        CONNECTION_TIMEOUT, FETCHED, MODIFIED, RP_COMMON,
                        SERVER_SCRIPT_PATH, STATE_ACTIVE, STATE_AUTH,
                        STATE_INITIAL, CONNECTING, STATE_LOBBY,
                        STATE_SRV_SYNC, STATE_SYNCING, STATE_WAITING, UP, 
                        TTL_SCRIPT_PATH, STATE_QUITTING)
from .data import (RepAuthCommand, RepDeleteCommand, RepDisconnectCommand,
                   RepKickCommand, ReplicatedCommand, ReplicatedCommandFactory,
                   ReplicatedDatablock, RepRightCommand,
                   RepServerSnapshotCommand, RepSnapshotCommand,
                   RepUpdateClientsState, RepUpdateUserMetadata, DataTranslationProtocol)
from .exception import (DataError, NetworkFrameError,
                        NonAuthorizedOperationError, StateError,
                        UnsupportedTypeError)
from .repository import Repository
from .utils import (current_milli_time,get_state_str)
from .porcelain import add

this = sys.modules[__name__]


class Session(object):
    def __init__(self):
        self._stash = []
        self.repository = None
        self.callbacks = {}
        self._lock_operations = threading.Event()
        self._state = STATE_INITIAL
        self._state_progress = {
            'current': -1,
            'total': -1
        }
        self._server = None

        # Networking
        self._state = STATE_INITIAL
        self._srv_snapshot_size = 0
        self._srv_snapshot_progress = 0
        self._online_users = {}

    def _assert_modification_rights(self, node=None):
        if self.repository.get_node(node).owner not in [self._id, RP_COMMON]:
            raise NonAuthorizedOperationError(
                "Not authorized to modify the node {node}")

    def _evaluate_dependencies(self, node_uuid):
        node = self.repository.get_node(node_uuid)

        assert(node)
        if not node.instance:
            return

        if node.dependencies:
            logging.debug(f"Clearing {len(node.dependencies)} dependencies.")
            node.dependencies.clear()

        dependencies = node.resolve_deps()

        logging.debug(f"found dependencies: {dependencies}")
        for dep in dependencies:
            registered_dep = self.repository.get_node_by_datablock(dep)
            if registered_dep:
                node.add_dependency(registered_dep.uuid)
            else:
                try:
                    dep_node_uuid = add(self.repository,
                                        dep,
                                        owner=node.owner)
                except UnsupportedTypeError:
                    logging.warning(f"Skipping {type(dep)}")
                else:
                    node.add_dependency(dep_node_uuid)

    def register(self, name):
        def func_wrapper(func):
            self.callbacks[name] = func
            return func
        return func_wrapper

    def call_registered(self, name=None, **kwargs):
        func = self.callbacks.get(name, None)
        if func is None:
            logging.info("No function registered against - " + str(name))
            return None
        return func(**kwargs)

    def connect(self,
                repository: Repository = None,
                id="Default",
                address="127.0.0.1",
                port=5560,
                timeout=1000,
                password=None):
        """Connect to a session

        :param id: user name
        :type id: string
        :param address: host ip address
        :type address: string
        :param port: host port
        :type port: int
        """
        self.repository = repository
        self._data_protocol = repository.data_protocol

        self._id = id
         # uuid needed to avoid reconnexion problems on router sockets
        self._uuid = uuid.uuid4()
        self._port = port
        self._address = address
        self._connection_timeout = timeout
        self.context = zmq.Context()
        self._state = CONNECTING

        try:
            self._poller = zmq.Poller()
            self._command = self.context.socket(zmq.DEALER)
            self._command.setsockopt(zmq.IDENTITY, self._uuid.bytes)
            self._command.connect(f"tcp://{address}:{port}")
            self._command.linger = 0

            self._subscriber = self.context.socket(zmq.DEALER)
            self._subscriber.setsockopt(zmq.IDENTITY, self._uuid.bytes)
            self._subscriber.connect(f"tcp://{address}:{port+1}")
            self._subscriber.linger = 0
            self._subscriber.setsockopt(zmq.RATE, 1000000)
            self._subscriber.setsockopt(zmq.RCVBUF, 2000000)

            self._poller.register(self._command, zmq.POLLIN)
            self._poller.register(self._subscriber, zmq.POLLIN)
            self._command_data_protocol = ReplicatedCommandFactory()

            self._publish = self.context.socket(zmq.PUSH)
            self._publish.setsockopt(zmq.IDENTITY,  self._uuid.bytes)
            self._publish.connect(f"tcp://{address}:{port+2}")
            self._publish.linger = 0
            self._publish.setsockopt(zmq.RATE, 1000000)
            self._publish.setsockopt(zmq.SNDBUF, 2000000)
        except Exception as e:
            logging.error(e)
        else:
            auth_type = 'ADMIN' if password else 'CLIENT'
            auth_request = RepAuthCommand(
                owner=self._id, data={
                    "AUTH_TYPE": auth_type,
                    "AUTH_ID": self._id,
                    "PWD": password,
                    "VERSION": __version__,
                })
            auth_request.push(self._command)

        self._state = STATE_AUTH
        self._connection_start_time = current_milli_time()
        self._ttl = subprocess.Popen([
                        sys.executable,
                        TTL_SCRIPT_PATH,
                        '-p', str(port),
                        '-d', address,
                        '-i', str(self._uuid),
                        '-t', str(timeout)]
                    )

    def host(self,
             id="Default",
             repository: Repository = None,
             port=5560,
             timeout=1000,
             password=None,
             cache_directory='',
             server_log_level='INFO'):
        """Host a session

        :param id: user name
        :type id: string
        :param address: host ip address
        :type address: strings
        :param port: host port
        :type port: int
        """
        # Create a server and serve
        self._server = subprocess.Popen([
            sys.executable,
            SERVER_SCRIPT_PATH,
            '-p', str(port),
            '-t', str(timeout),
            '-pwd', str(password),
            '--attached',
            '--log-level', server_log_level,
            '--log-file', os.path.join(cache_directory, 'multiuser_server.log')]
        )

        self.connect(repository=repository,
                     id=id,
                     address='127.0.0.1',
                     port=port,
                     timeout=timeout,
                     password=password)

    def init(self):
        """ Init the repository data

            commit and push initial graph to the server
        """
        if len(self.repository.object_store) == 0:
            logging.error("Add some data first")
            return

        self.request_server_repository_init()

    def disconnect(self, reason: str = 'None'):
        """Disconnect from session
        """
        self._state = STATE_QUITTING
        self._publish.close()
        self._command.close()
        self._subscriber.close()
        logging.info(f"Exiting session, reason {reason}")
        if self.is_connection_alive():
            self._ttl.kill()
        if self._server:
            self._server.kill()
        self.context.destroy()
        self.call_registered('on_exit', reason=reason)
        
        self._state = STATE_INITIAL

    def remove(self, uuid, remove_dependencies=True):
        """
        Unregister for replication the given object.

        :param uuid: node uuidñ
        :type uuid: string
        :param remove_dependencies: remove all dependencies
        :type remove_dependencies: bool (default: True)
        :raise NonAuthorizedOperationError:
        :raise KeyError:
        """
        self._assert_modification_rights(uuid)
        self._assert_state([STATE_ACTIVE, STATE_SRV_SYNC])

        if self.is_registered(uuid):
            nodes_to_delete = []

            if remove_dependencies:
                nodes_to_delete.extend(
                    self.repository.get_dependencies_ordered(node=uuid))

            nodes_to_delete.append(uuid)

            logging.debug(f"Removing {nodes_to_delete}")
            for node in nodes_to_delete:
                delete_command = RepDeleteCommand(
                    owner='client', data=node)
                # remove the key from our store
                delete_command.execute(self.repository.object_store)
                delete_command.push(self._command)
        else:
            raise KeyError("Cannot unregister key")

    def kick(self, user):
        """
        Kick a user from the session.
        """
        self._assert_state([STATE_ACTIVE])

        if user == self._id:
            logging.error("You can't kick ypurself")
            return
        if self.is_admin():
            kick_order = RepKickCommand(owner=self._id,
                                        data={'user': user})
            kick_order.push(self._command)
        else:
            logging.error("Insufisent rights to kick.")

    def commit(self, uuid):
        """Commit the given node

        :param uuid: node uuid
        :type uuid: string
        :raise ReferenceError:
        :raise StateError:
        :raise ContextError:
        """
        # TODO: refactoring
        assert(self.is_registered(uuid))

        node = self.repository.get_node(uuid)

        if node.state == COMMITED:
            return

        self._evaluate_dependencies(uuid)

        for dep_uuid in self.repository.get_dependencies_ordered(node=uuid):
            dep = self.repository.get_node(dep_uuid)
            if dep.state in [ADDED, MODIFIED]:
                dep.commit()
        node.commit()

    def push(self, uuid, check_data=True):
        """Replicate a given node to all users. Send all node in `COMMITED` by default.

        :param uuid: node key to push
        :type uuid: string
        """
        # TODO: Refactoring
        if uuid:
            self._assert_modification_rights(uuid)

            node = self.repository.get_node(uuid)

            for dep in self.repository.get_dependencies_ordered(node=uuid):
                dep_node = self.repository.get_node(dep)
                if dep_node.state in [COMMITED, ADDED]:
                    dep_node.push(self._publish, check_data=check_data)
            node.push(self._publish, check_data=check_data)

    def change_owner(self,
                     uuid,
                     new_owner,
                     ignore_warnings=True,
                     affect_dependencies=True):
        """Change a node owner

        :param uuid: node key
        :type uuid: string
        :param new_owner: new owner id
        :type new_owner: string
        :param ignore_warnings: ignore NonAuthorizedOperationError
        :type ignore_warnings: bool
        :param affect_dependencies: change dependencies owner
        :type affect_dependencies: bool

        """
        assert(self.is_registered(uuid))

        affected_nodes = []

        if affect_dependencies:
            affected_nodes.extend(
                self.repository.get_dependencies_ordered(node=uuid))
        affected_nodes.append(uuid)

        for n in affected_nodes:
            try:
                self._assert_modification_rights(n)
            except NonAuthorizedOperationError as e:
                if ignore_warnings:
                    node_ref = self.repository.get_node(n)
                    logging.debug(
                        f"Node {n} already owned by {node_ref.owner}")
                    continue
                else:
                    raise e
            else:
                # Setup the right override command
                right_command = RepRightCommand(
                    owner=self._id,
                    data={
                        'uuid': n,
                        'owner': new_owner}
                )

                right_command.execute(self.repository.object_store)
                right_command.push(self._command)

    def update_user_metadata(self, dikt):
        """Update user metadata

        Update local client informations to others (ex: localisation)

        :param json:
        :type dict:
        """
        assert(dikt)

        user_state_update = RepUpdateUserMetadata(
            owner=self._id,
            data=dikt
        )

        user_state_update.push(self._command)

    # TODO: remove
    def is_registered(self, uuid=None, reference=None):
        """Check for a node existence

        :param uuid: node uuid
        :type uuid: string
        :return: bool
        """
        if uuid:
            return uuid in self.repository.object_store.keys()
        if reference:
            for k, v in self.repository.object_store.items():
                if reference == v.instance:
                    return True

        return False

    def save(self, filepath: str):
        """ Save all session data to a .db file
        """

        nodes_ids = self.list()
        # TODO: add dump graph to replication

        nodes = []
        for n in nodes_ids:
            nd = self.repository.get_node(n)
            nodes.append((
                n,
                {
                    'owner': nd.owner,
                    'str_type': nd.str_type,
                    'data': nd.data,
                    'dependencies': nd.dependencies,
                }
            ))

        db = dict()
        db['nodes'] = nodes
        db['users'] = copy.copy(self._online_users)

        stime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S')

        filepath = Path(filepath)
        filepath = filepath.with_name(
            f"{filepath.stem}_{stime}{filepath.suffix}")

        with gzip.open(filepath, "wb") as f:
            logging.info(f"Writing session snapshot to {filepath}")
            pickle.dump(db, f, protocol=4)

    def is_readonly(self, node_id: str) -> bool:
        """ Check local user modification rights on a node

        :param node_id: node identifier
        :type node_id: str
        :return: bool
        """
        node = self.repository.get_node(node_id)
        return node and (node.owner in [self._id, RP_COMMON])

    # TODO: remove
    def list(self, filter=None, filter_owner=None):
        """List all graph nodes keys
        :param filter: node type
        :type filter: ReplicatedDatablock class (or child class)
        """
        base_list = self.repository.list(filter_type=filter)
        if filter_owner:
            return [key for key in base_list
                    if self.repository.get_node(key).owner == filter_owner]
        else:
            return base_list

    # NETWORKING
    def is_connection_alive(self):
        return self._ttl.poll() is None

    def _assert_state(self, state):
        if self._state not in state:
            raise StateError("Client in wrong state")

    def request_snapshot_init(self):
        """ Ask to the server for repository init. """

        logging.info('Requestion snapshots init')

        self._snapshot_progress = 0
        self._snapshot_total = 0

        snapshot_request = RepSnapshotCommand(
            owner=self._id,
            data={'STATE': "REQUEST_INIT"})

        snapshot_request.push(self._command)

    def request_server_repository_init(self):
        """ Ask to the server for repository init.

            :param command: incoming command
            :type command: RepAuthCommand
        """
        logging.info('Request server init')

        self._srv_snapshot_size = len(self.repository.object_store)
        keys = [k for k, v in self.repository.object_store.items()]
        assert(self._srv_snapshot_size > 0)

        snapshot_cmd = RepServerSnapshotCommand(
            owner='server',
            data={'STATE': 'INIT',
                  'SIZE': self._srv_snapshot_size,
                  'NODES': keys})
        snapshot_cmd.push(self._command)

        self._state = STATE_SRV_SYNC

    def handle_authentification(self, command):
        """ Manage client authentification

            :param command: incoming command
            :type command: RepAuthCommand
        """
        self._assert_state([STATE_AUTH])

        connection_status = command.data

        if 'LOBBY' in connection_status:
            self._state = STATE_LOBBY
            if self._server:
                self.request_server_repository_init()
        if 'RUNNING' in connection_status:
            self._state = STATE_LOBBY
            self.request_snapshot_init()
        if 'FAILED' in connection_status:
            self.disconnect(
                reason='Failed to connect, authentification refused.')

    def handle_client_snapshot(self, command):
        """ Manage incoming snapshot commands

            :param command: incoming command
            :type command: RepSnapshotCommand
        """
        self._assert_state([STATE_SYNCING, STATE_LOBBY])

        snapshot_state = command.data['STATE']
        if snapshot_state == 'INIT':
            logging.info("client init")
            self._snapshot_progress = 0
            self._snapshot_catalog = command.data.get('CATALOG')
            self._snapshot_total = len(self._snapshot_catalog)
            self._snapshot_late_updates = queue.Queue()

            self._state_progress = {
                'current': self._snapshot_progress,
                'total': self._snapshot_total
            }

            self._current_snapshot = self._snapshot_catalog.pop()
            self.get_snapshot(self._current_snapshot)

            self._state = STATE_SYNCING

    def handle_server_repository_init(self, command):
        """ Manage server initialization commands

            :param command: incoming command
            :type command: RepServerSnapshotCommand
        """
        self._assert_state([STATE_SRV_SYNC])

        cli_snapshot_state = command.data.get('STATE')

        if cli_snapshot_state == 'ACCEPTED':
            for index, node in enumerate(self.repository.object_store.values()):
                node.commit()
                node.state = UP
                snapshot_cmd = RepServerSnapshotCommand(
                    owner='server',
                    data={
                        'STATE': 'SET',
                        'DATA': {
                            'owner': node.owner.encode(),
                            'uuid': node.uuid.encode(),
                            'dependencies':  pickle.dumps(node.dependencies, protocol=4),
                            'type': node.str_type.encode(),
                            'data': node._serialize()
                        }
                    }
                )

                snapshot_cmd.push(self._command)
                self._state_progress = {
                    'current': index,
                    'total': len(self.repository.object_store)
                }

            snapshot_cmd = RepServerSnapshotCommand(
                owner='server',
                data={'STATE': 'END'})
            snapshot_cmd.push(self._command)
        elif cli_snapshot_state == 'DONE':
            self._state = STATE_ACTIVE
            self.call_registered('on_connection')
        elif cli_snapshot_state == 'REJECTED':
            logging.error("client snapshot refused by the server.")
            self._state = STATE_LOBBY

    def get_snapshot(self, id):
        """ Ask a specific snapshot to the server

            :param id: uuid of the data
            :type id: str
        """
        logging.debug(f"get {id}")
        snapshot_request = RepSnapshotCommand(
            owner=self._id,
            data={
                'STATE': "GET",
                'ID': id})

        snapshot_request.push(self._command)

    def listen(self, timeout: int = 0):
        """ Non-blocking network listening

            :param timeout: network packet waiting time in millisecond
            :type timeout: int
        """
        if self._state in [STATE_INITIAL, STATE_QUITTING]:
            return

        if not self.is_connection_alive():
            self.disconnect(reason='Server lost')
            return

        sockets = dict(self._poller.poll(timeout))
        # COMMANDS I/O
        if self._command in sockets:
            try:
                command = ReplicatedCommand.fetch(
                    self._command,
                    self._command_data_protocol)
            except Exception as e:
                logging.error(
                    f"Corrupted frame received, skipping it. Cause:{e}")
            else:
                # AUTHENTIFICATION
                if isinstance(command, RepAuthCommand):
                    self.handle_authentification(command)

                # DISCONNECT CONFIRMATION
                if isinstance(command, RepDisconnectCommand):
                    self.disconnect(reason=command.data)

                # CLIENTS INFO UPDATE
                if isinstance(command, RepUpdateClientsState):
                    self._online_users = command.data

                # SERVER-->CLIENT SNAPSHOT
                if isinstance(command, RepSnapshotCommand):
                    self.handle_client_snapshot(command)

                # CLIENT -> SERVER SNAPSHOT
                if isinstance(command, RepServerSnapshotCommand):
                    self.handle_server_repository_init(command)

                # GRAPH OPERATION (DELETE, CHANGE_RIGHT)
                if type(command) in [RepDeleteCommand, RepRightCommand]:
                    command.execute(self.repository.object_store)

        # DATA IN
        if self._subscriber in sockets:
            try:
                datablock = ReplicatedDatablock.fetch(
                    self._subscriber,
                    self._data_protocol)
            except Exception as e:
                logging.error(
                    f"Corrupted frame received, skipping it. Cause:{e}")
            else:
                # Client snapshot
                if self._state == STATE_SYNCING:
                    # If the snapshot is expected in the snapshot catalog we store
                    # it and ask for the next
                    if datablock.uuid == self._current_snapshot:
                        self._snapshot_progress += 1
                        self._state_progress = {
                            'current': self._snapshot_progress,
                            'total': self._snapshot_total
                        }
                        self.repository.do_commit(datablock)

                        if not self._snapshot_catalog:
                            # Apply late updates
                            while not self._snapshot_late_updates.empty():
                                late_update = self._snapshot_late_updates.get()
                                logging.info(f"Applying late update: {late_update.uuid}")
                                self.repository.do_commit(late_update)

                            snapshot_request = RepSnapshotCommand(
                                owner=self._id,
                                data={'STATE': "DONE"})
                            snapshot_request.push(self._command)
                            logging.info("Snapshot done.")
                            self._state = STATE_ACTIVE
                            self.call_registered('on_connection')
                        else:
                            self._current_snapshot = self._snapshot_catalog.pop()
                            self.get_snapshot(self._current_snapshot)
                    # If it isn't expected why keep it in order to apply it
                    #  at the end of the snapshot process.
                    else:
                        logging.info(
                            "Adding an update for the late one...")
                        self._snapshot_late_updates.put(datablock)

                # Store received updates
                if self._state == STATE_ACTIVE:
                    self.repository.do_commit(datablock)

        # Various timeout checks
        # auth
        if self._state == STATE_AUTH:
            if (current_milli_time()-self._connection_start_time) > self._connection_timeout:
                self.disconnect(
                    reason='Connection failed, server not found')

    @property
    def state(self):
        """Get active session state

        :return: session state
        """
        return self._state

    @property
    def state_progress(self):
        """Get active session state

        :return: session state
        """
        return self._state_progress

    @property
    def online_users(self):
        return self._online_users

    @property
    def id(self):
        return self._id

    def is_admin(self):
        return self._online_users[self.id]['admin']


this.session = Session()
