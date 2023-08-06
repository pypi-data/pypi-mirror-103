import abc
import logging
from collections import deque
from typing import List, Union

from flywheel_gear_toolkit.utils.datatypes import Container

log = logging.getLogger(__name__)


class Walker:
    """A class to walk the container hierarchically

    example usage:

    .. code-block:: python

        proj = fw.lookup('test/test_proj')
        proj_walker = walker.Walker(proj, depth_first=True)
        for container in proj.walk():
            if container.container_type == 'session':
                print('Found a session')
        proj = fw.lookup('test/test_proj')
    """

    def __init__(self, root: Container, depth_first: bool = True, reload: bool = False):
        """
        Args:
            root (Container):
                The root container, one of `flywheel.Project,flywheel.Subject, flywheel.Session, flywheel.Acquisition, flywheel.FileEntry, flywheel.AnalysisOutput`
            depth_first (bool): Depth first of breadth first traversal, True for depth first, False fo breadth first
            reload (bool): If `True`, reload containers when walking to load all metadata (default: False)
        """
        self.deque = deque([root])
        self.depth_first = depth_first
        self.reload = reload
        self.subject = True

    def next(self):
        """Returns the next element from the walker and adds its children.

        Returns:
            Container|FileEntry
        """
        if self.depth_first:
            next_element = self.deque.pop()
        else:
            next_element = self.deque.popleft()

        log.debug(f"Element returned is {next_element.container_type}")

        self.queue_children(next_element)

        return next_element

    def add(self, element: Union[List[Container], Container]):
        """Adds an element to the walker.

        Args:
            element (List[Container] or Container): Element or list of elements to add to deque
        """
        try:
            self.deque.extend(element)
        except TypeError:
            # element not an iterable
            self.deque.append(element)
        except AttributeError:
            self.deque.append(element)

    def _reload_container(self, container):
        """Returns reloaded container is `self.reload` is True."""
        if self.reload:
            return container.reload()
        return container

    def queue_children(self, element: Container) -> None:
        """Returns children of the element.

        Args:
            element (Container): container to find children of.
        """
        container_type = element.container_type

        # No children of files
        if container_type == "file":
            return []

        if container_type == "analysis":
            return []

        log.info(
            f"Queueing children for {container_type} "
            f"ID: {element.id}, "
            f"label: {element.label}"
        )

        self.deque.extend(element.files or [])

        # Make sure that the analyses attribute is a list before iterating
        if isinstance(element.analyses, list):
            self.deque.extend(
                [self._reload_container(analysis) for analysis in element.analyses]
            )
        if container_type == "project":
            self.deque.extend(
                [self._reload_container(subject) for subject in element.subjects()]
            )
        elif container_type == "subject":
            self.deque.extend(
                [self._reload_container(session) for session in element.sessions()]
            )
        elif container_type == "session":
            self.deque.extend(
                [
                    self._reload_container(acquisition)
                    for acquisition in element.acquisitions()
                ]
            )

    def is_empty(self):
        """Returns True if the walker is empty.

        Returns:
            bool
        """
        return len(self.deque) == 0

    def walk(self):
        """Walks the hierarchy from a root container.

        Yields:
            Container|FileEntry
        """

        while not self.is_empty():
            yield self.next()
