import json
import logging
from osdf import OSDF
from itertools import islice
from cutlass.iHMPSession import iHMPSession
from cutlass.Util import *

# Create a module logger named after the module
module_logger = logging.getLogger(__name__)
# Add a NullHandler for the case if no logging is configured by the application
module_logger.addHandler(logging.NullHandler())

# pylint: disable=C0302, W0703, C1801

class Base(object):
    """
    The parent class from which all objects inherit specific features from. This class
    contains all the fields required to all sub-classes (ID, version, links, and tags).

    Attributes:
        namespace (str): The namespace this class will use in the OSDF instance
    """
    namespace = "ihmp"

    def __init__(self):
        """
        Constructor for the Base class. This should not be called from the user, so the
        user should instantiate an instance of the Base class. This initializes the
        OSDF ID, Version, Links, and Tags for all sub-classes

        Args:
            None
        """
        self.logger = logging.getLogger(self.__module__ + '.' + self.__class__.__name__)

        self.logger.addHandler(logging.NullHandler())

        self._id = None
        self._version = None
        self._links = {}
        self._tags = []

    @property
    def id(self):
        """
        str: An alphanumeric indicating the specific ID assigned to the document
             in OSDF.
        """
        self.logger.debug("In 'id' getter.")
        return self._id

    def _set_id(self, node_id):
        """
        The setter for the OSDF ID. This is a private method, so the user should not
        call this. In property form.

        Args:
            node_id (str): The new node ID to assign to this instance

        Returns:
            None
        """
        self.logger.debug("In private _set_id.")
        self._id = node_id

    @property
    def version(self):
        """
        int: The specific version of this instance in the OSDF instance.
             The version must be of type integer, and must be a number
             greater than 0
        """
        self.logger.debug("In 'version' getter.")
        return self._version

    @version.setter
    @enforce_int
    def version(self, version):
        self.logger.debug("In 'version' setter.")

        if version <= 0:
            raise ValueError("Invalid version. Must be a postive integer.")

        self._version = version

    @property
    def links(self):
        """
        Dictionary[str]: The dictionary of links between the current instance
                         and another instance. The link must follow the key-value
                         pair specified by the JSON schema indicating links in the
                         OSDF instance.
        """
        self.logger.debug("In 'links' getter.")
        return self._links

    @links.setter
    @enforce_dict
    def links(self, links):
        self.logger.debug("In 'links' setter.")

        for (link, node_list) in links.items():
            if (type(link) != str) or (type(node_list) != list):
                raise ValueError("Links must be a dict of strings to lists.")

        self._links = links

    @property
    def tags(self):
        """
        List[str]: The list of tags for the instance. This is a required field for
                   all OSDF objects. The tag provided must be of type list. If not,
                   a ValueError is raised indicating the tags must be of type list.
        """
        self.logger.debug("In 'tags' getter.")
        return self._tags

    @tags.setter
    @enforce_list
    def tags(self, tags):
        self.logger.debug("In 'tags' setter.")

        self._tags = tags

    def add_tag(self, tag):
        """
        Adds a new tag to the current tags list for the instance.
        The method checks to make sure that the tag is not already
        present in the current tags list.

        Args:
            tag (str): The new tag to add

        Returns:
            None

        Exceptions:
            ValueError exception if the tag is already present
        """
        self.logger.debug("In add_tag. New tag: %s", tag)
        if tag not in self._tags:
            self._tags.append(tag)
        else:
            raise ValueError("Tag already present for this subject")

    def validate(self):
        """
        Validates the current object's data/JSON against the current
        schema in the OSDF instance for that specific object. All required
        fields for that specific object must be present.

        Args:
            None

        Returns:
            A list of strings, where each string is the error that the
            validation raised during OSDF validation
        """
        self.logger.debug("In validate.")

        document = self._get_raw_doc()

        session = iHMPSession.get_session()
        self.logger.info("Got iHMP session.")

        (valid, error_message) = session.get_osdf().validate_node(document)

        problems = []
        if not valid:
            self.logger.info("Validation did not succeed.")
            problems.append(error_message)

        self.logger.debug("Number of validation problems: %s.", str(len(problems)))
        return problems

    def is_valid(self):
        """
        Validates the current object's data/JSON against the current schema
        in the OSDF instance for the specific object. However, unlike
        validates(), this method does not provide exact error messages,
        it states if the validation was successful or not.

        Args:
            None

        Returns:
            True if the data validates, False if the current state of
            fields in the instance do not validate with the OSDF instance
        """
        self.logger.debug("In is_valid.")

        document = self._get_raw_doc()

        session = iHMPSession.get_session()
        self.logger.info("Got iHMP session.")

        (valid, _error_message) = session.get_osdf().validate_node(document)

        self.logger.debug("Valid? %s", str(valid))

        return valid

    def to_json(self, indent=4):
        """
        Converts the current object from a raw dictionary to a pretty-printed
        JSON string.

        Args:
            indent (int): The indent used to pretty print the JSON string

        Returns:
            A JSON string with all fields/properties of the current instance
        """
        self.logger.debug("In to_json.")

        doc = self._get_raw_doc()

        self.logger.debug("Encoding structure to JSON.")

        json_str = json.dumps(doc, indent=indent)

        self.logger.debug("Dump to JSON successful. Length: %s characters", str(len(json_str)))

        return json_str

    def search(self, query):
        """
        Searches the OSDF instance using the specified input parameters

        Args:

        Returns:

        """
        self.logger.debug("In search.")

        session = iHMPSession.get_session()

        self.logger.info("Got iHMP session.")

    def delete(self):
        """
        Deletes the current object. The object must already have been saved/present
        in the OSDF instance, so an ID for the object must have been already set.

        Args:
            None

        Returns:
            True if the object was successfully deleted, False otherwise

        Exceptions:
            Exception: If the instance does not have an ID set (was never saved in OSDF)
        """
        self.logger.debug("In delete.")

        if self._id is None:
            self.logger.warn("Attempt to delete a node with no ID.")
            raise Exception("Node does not have an ID.")

        visit_node_id = self._id

        session = iHMPSession.get_session()
        self.logger.info("Got iHMP session.")

        # Assume failure
        success = False

        try:
            self.logger.info("Deleting node with OSDF ID %s.", visit_node_id)
            session.get_osdf().delete_node(visit_node_id)
            success = True
        except Exception as delete_exception:
            self.logger.exception(delete_exception)
            self.logger.error("An error occurred when deleting %s.", self)

        return success

    def children(self, flatten=False):
        """ Returns the children of this node. """
        self.logger.debug("In children.")

        # local imports to avoid cyclic imports
        from .dependency import dependency_methods
        from .dependency import generator_flatten

        def _children(obj):
            yield obj
            name = obj.__class__.__name__
            dep_method = getattr(obj, dependency_methods.get(name, ''), None)
            if dep_method:
                for child in dep_method():
                    yield _children(child)
        cs = islice(_children(self), 1, None)
        if flatten:
            return generator_flatten(cs)
        else:
            return cs

    def __call__(self):
        return self

    def __str__(self):
        _id = "no ID" if not self._id else self._id[-8:]
        name = None

        for attr in ("_name", "_rand_subject_id", "_date", "_local_file"):
            if hasattr(self, attr):
                name = getattr(self, attr)
                break

        if name:
            return "<{} `{}' ({})>".format(self.__class__.__name__, name, _id)
        else:
            return "<{} ({})>".format(self.__class__.__name__, _id)


    __repr__ = __str__

    def __hash__(self):
        if not self._id:
            raise TypeError("Unhashable; must have ID: '{}')".format(str(self)))

        return hash(self._id)

    def __eq__(self, other):
        if self._id and other._id:
            return self._id == other._id

        return False
