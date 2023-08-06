import logging
from .exception import (UnsupportedTypeError)
from .constants import (RP_COMMON, FETCHED)


def add(repostitory, object, owner=None, dependencies=[]):
    """Register a python to the given repository stagging area

    :param repository: Target repository
    :type repository: Repository
    :param objet: Any registered object
    :type object: Any registered object type in the given factory
    :param dependencies: Object dependencies uuid
    :type dependencies: Array of string
    :raise: UnsupportedTypeError
    """
    assert(object)

    # Retrieve corresponding implementation and init a new instance
    implementation = repostitory.data_protocol.get_implementation_from_object(
        object)

    if implementation:
        default_owner = RP_COMMON

        new_owner = owner if owner else default_owner
        new_node = implementation(
            owner=new_owner,
            instance=object,
            dependencies=dependencies)

        dependencies = new_node.resolve_deps()

        for dependance in dependencies:
            dep_ref = repostitory.get_node_by_datablock(dependance)
            if dep_ref:
                new_node.add_dependency(dep_ref.uuid)
            else:
                if dependance:
                    try:
                        new_child_node = add(repostitory=repostitory,
                                                object=dependance,
                                                owner=new_owner)
                        if new_child_node:
                            new_node.add_dependency(new_child_node)
                    except UnsupportedTypeError:
                        logging.warning(f"Skipping {type(object)}.")
        logging.debug(
            f"Registering {object} as {new_node.uuid} (owner:{new_owner})")
        repostitory.do_commit(new_node)

        return new_node.uuid
    else:
        raise UnsupportedTypeError(
            f"{type(object)} not supported, skipping.")


def apply(repository, node_id, force=False, force_dependencies=False):
        """Apply proxy to version to local datablock

        :param node: node key to apply
        :type node: string
        :param force: force node apply
        :type force: bool
        :param force_dependencies: force node dependencies apply
        :type force_dependencies: bool
        """
        node = repository.get_node(node_id)

        if node and (node.state in [FETCHED] or force):
            deps = repository.get_dependencies_ordered(node.uuid)

            # Apply  dependenciesß
            for dep in deps:
                dep_node = repository.get_node(dep)

                if dep_node and (dep_node.state in [FETCHED] or force_dependencies):
                    dep_node.apply()

            node.apply()
        else:
            logging.warning(f"Can't apply node {node_id}")