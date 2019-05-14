"""
This module models the host epigenetics raw sequence set object.
"""

import json
import logging
import os
import string
from cutlass.iHMPSession import iHMPSession
from cutlass.Base import Base
from cutlass.aspera import aspera
from cutlass.Util import *

# pylint: disable=W0703, C1801

# Create a module logger named after the module
module_logger = logging.getLogger(__name__)

# Add a NullHandler for the case if no logging is configured by the application
module_logger.addHandler(logging.NullHandler())

class HostEpigeneticsRawSeqSet(Base):
    """
    The class models host epigenetics raw sequence set data for the iHMP
    project. This class contains all the fields required to save a
    HostEpigeneticsRawSeqSet object to OSDF.

    Attributes:
        namespace (str): The namespace this class will use in the OSDF instance
    """
    namespace = "hmbr"

    aspera_server = "aspera.microbiome-bioactives.org"

    def __init__(self, *args, **kwargs):
        """
        Constructor for the HostEpigeneticsRawSeqSet class. This initializes
        the fields specific to the class, and inherits from the Base class.

        Args:
            None
        """
        self.logger = logging.getLogger(self.__module__ + '.' + self.__class__.__name__)

        self.logger.addHandler(logging.NullHandler())

        # These are common to all objects
        self._id = None
        self._version = None
        self._links = {}
        self._tags = []

        # These are particular to HostEpigeneticsRawSeqSet objects
        self._assay_type = None
        self._checksums = None
        self._comment = None
        self._exp_length = None
        self._format = None
        self._format_doc = None
        self._local_file = None
        self._seq_model = None
        self._size = None
        self._study = None
        self._subtype = None
        self._urls = ['']

        # Optional properties
        self._private_files = None
        self._sequence_type = None

        super(HostEpigeneticsRawSeqSet, self).__init__(*args, **kwargs)

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
            self.logger.info("Validation did not succeed for %s.", __name__)
            problems.append(error_message)

        if self._private_files:
            self.logger.info("User specified the files are private.")
        else:
            self.logger.info("Data is NOT private, so check that local_file is set.")
            if self._local_file is None:
                problems.append("Local file is not yet set.")
            elif not os.path.isfile(self._local_file):
                problems.append("Local file does not point to an actual file.")

        if 'sequenced_from' not in self._links.keys():
            problems.append("Must add a 'sequenced_from' link to a host_seq_prep.")

        self.logger.debug("Number of validation problems: %s.", len(problems))

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

        problems = self.validate()

        valid = True
        if len(problems):
            self.logger.error("There were %s problems.", str(len(problems)))
            valid = False

        self.logger.debug("Valid? %s", str(valid))

        return valid

    @property
    def checksums(self):
        """
        str: One or more checksums used to ensure file integrity.
        """
        self.logger.debug("In 'checksums' getter.")

        return self._checksums

    @checksums.setter
    @enforce_dict
    def checksums(self, checksums):
        """
        The setter for the checksum data.

        Args:
            checksums (dict): The checksums for the data file.

        Returns:
            None
        """
        self.logger.debug("In 'checksums' setter.")

        self._checksums = checksums

    @property
    def assay_type(self):
        """
        str: The assay_type for the sequence set. Identifies the type of
        assay peformed.
        """
        self.logger.debug("In 'assay_type' getter.")

        return self._assay_type

    @assay_type.setter
    @enforce_string
    def assay_type(self, assay_type):
        """
        The setter for the assay_type, which identifies the type of assay
        peformed. Must be one of RRBS, MBD-Seq, ChIP-Seq, or ATAC-Seq.

        Args:
            assay_type (str): The assay_type for the sequence set.

        Returns:
            None
        """
        self.logger.debug("In 'assay_type' setter.")

        self._assay_type = assay_type

    @property
    def comment(self):
        """
        str: Free-text comment.
        """
        self.logger.debug("In 'comment' getter.")

        return self._comment

    @comment.setter
    @enforce_string
    def comment(self, comment):
        """
        The setter for the comment field. The comment must be a string,
        and less than 512 characters.

        Args:
            comment (str): The new comment to add to the string.

        Returns:
            None
        """
        self.logger.debug("In 'comment' setter.")

        self._comment = comment

    @property
    def exp_length(self):
        """
        int: The number of raw bases or color space calls expected for the read,
             includes both mate pairs and all technical portions.
        """
        self.logger.debug("In 'exp_length' getter.")

        return self._exp_length

    @exp_length.setter
    @enforce_int
    def exp_length(self, exp_length):
        """
        The setter for the number of raw bases or color space calls.

        Args:
            exp_length (int): The new exp_length for the current instance.

        Returns:
            None
        """
        self.logger.debug("In 'exp_length' setter.")
        if exp_length < 0:
            raise ValueError("The 'exp_length' must be non-negative.")

        self._exp_length = exp_length

    @property
    def format(self):
        """
        str: The file format of the sequence file.
        """
        self.logger.debug("In 'format' getter.")

        return self._format

    @format.setter
    @enforce_string
    def format(self, format_str):
        """
        The setter for the format. This must be either 'fasta' or 'fastq'.

        Args:
            format_str (str): The new format string for the current object.

        Returns:
            None
        """
        self.logger.debug("In 'format' setter.")

        formats = ["fasta", "fastq"]
        if format_str in formats:
            self._format = format_str
        else:
            raise Exception("Format must be either fasta or fastq.")

    @property
    def format_doc(self):
        """
        str: URL for documentation of file format.
        """
        self.logger.debug("In 'format_doc' getter.")

        return self._format_doc

    @format_doc.setter
    @enforce_string
    def format_doc(self, format_doc):
        """
        The setter for the file format documentation URL.

        Args:
            format_doc (str): The new format_doc for the current object.

        Returns:
            None
        """
        self.logger.debug("In 'format_doc' setter.")

        self._format_doc = format_doc

    @property
    def local_file(self):
        """
        str: URL to the local file to upload to the server.
        """
        self.logger.debug("In 'local_file' getter.")

        return self._local_file

    @local_file.setter
    @enforce_string
    def local_file(self, local_file):
        """
        The setter for the local file.

        Args:
            local_file (str): The URL to the local file that should
                              be uploaded to the server.

        Returns:
            None
        """
        self.logger.debug("In 'local_file' setter.")

        self._local_file = local_file

    @property
    def private_files(self):
        """
        bool: Whether this object describes private data that should not
        be uploaded to the DCC. Defaults to false.
        """
        self.logger.debug("In 'private_files' getter.")

        return self._private_files

    @private_files.setter
    @enforce_bool
    def private_files(self, private_files):
        """
        The setter for the private files flag to denote this object
        describes data that should not be uploaded to the DCC.

        Args:
            private_files (bool):

        Returns:
            None
        """
        self.logger.debug("In 'private_files' setter.")

        self._private_files = private_files

    @property
    def seq_model(self):
        """
        str: Sequencing instrument model.
        """
        self.logger.debug("In 'seq_model' getter.")

        return self._seq_model

    @seq_model.setter
    @enforce_string
    def seq_model(self, seq_model):
        """
        The setter for the sequencing instrument model.

        Args:
            seq_model (str): The new sequencing instrument model.

        Returns:
            None
        """
        self.logger.debug("In 'seq_model' setter.")

        self._seq_model = seq_model

    @property
    def sequence_type(self):
        """
        str: Specifies whether the file contains peptide or nucleotide data.
        """
        self.logger.debug("In 'sequence_type' getter.")

        return self._sequence_type

    @sequence_type.setter
    @enforce_string
    def sequence_type(self, sequence_type):
        """
        The setter for the sequence type.

        Args:
            sequence_type (str): The new sequence type.

        Returns:
            None
        """
        self.logger.debug("In 'sequence_type' setter.")

        types = ["peptide", "nucleotide"]
        if sequence_type in types:
            self._sequence_type = sequence_type
        else:
            raise Exception("Sequence type must be either peptide or nucleotide")

    @property
    def size(self):
        """
        int: The size of the file in bytes.
        """
        self.logger.debug("In 'size' getter.")

        return self._size

    @size.setter
    @enforce_int
    def size(self, size):
        """
        The setter for the file size in bytes.

        Args:
            size (int): The size of the seq set in bytes.

        Returns:
            None
        """
        self.logger.debug("In 'size' setter.")

        if size < 0:
            raise ValueError("The size must be non-negative.")

        self._size = size

    @property
    def study(self):
        """
        str: One of the 3 studies that are part of the iHMP.
        """
        self.logger.debug("In 'study' getter.")

        return self._study

    @study.setter
    @enforce_string
    def study(self, study):
        """
        The setter for the sequence set's study. This is restricted to be one
        of preg_preterm, ibd, or prediabetes.

        Args:
            study (str): The study of the sequence set.

        Returns:
            None
        """
        self.logger.debug("In 'study' setter.")

        studies = ["preg_preterm", "ibd", "prediabetes"]

        if study in studies:
            self._study = study
        else:
            raise Exception("Not a valid study.")

    @property
    def urls(self):
        """
        list: An array of URL from where the file can be obtained,
              http, ftp, fasp, etc...
        """
        self.logger.debug("In 'urls' getter.")

        return self._urls

    @staticmethod
    def required_fields():
        """
        A static method. The required fields for the class.

        Args:
            None
        Returns:
            Tuple of strings of required properties.
        """
        module_logger.debug("In required_fields.")
        return ("assay_type", "checksums", "comment", "exp_length", "format",
                "format_doc", "lcoal_file", "seq_model", "size", "study",
                "tags", "urls")

    def _get_raw_doc(self):
        """
        Generates the raw JSON document for the current object. All required
        fields are filled into the JSON document, regardless they are set or
        not. Any remaining fields are included only if they are set. This
        allows the user to visualize the JSON to ensure fields are set
        appropriately before saving into the database.

        Args:
            None

        Returns:
            A dictionary representation of the JSON document.
        """
        self.logger.debug("In _get_raw_doc.")

        doc = {
            'acl': {
                'read': ['all'],
                'write': [HostEpigeneticsRawSeqSet.namespace]
            },
            'linkage': self._links,
            'ns': HostEpigeneticsRawSeqSet.namespace,
            'node_type': 'host_epigenetics_raw_seq_set',
            'meta': {
                "assay_type": self._assay_type,
                "checksums": self._checksums,
                "comment": self._comment,
                "exp_length": self._exp_length,
                "format": self._format,
                "format_doc": self._format_doc,
                "seq_model": self._seq_model,
                "size": self._size,
                "study": self._study,
                "subtype": "host",
                'tags': self._tags,
                "urls": self._urls
            }
        }

        if self._id is not None:
            self.logger.debug("%s object has the OSDF id set.", __name__)
            doc['id'] = self._id

        if self._version is not None:
            self.logger.debug("%s object has the OSDF version set.", __name__)
            doc['ver'] = self._version

        # Handle optional properties
        if self._private_files is not None:
            self.logger.debug("Object has the 'private_files' property set.")
            doc['meta']['private_files'] = self._private_files

        if self._sequence_type is not None:
            self.logger.debug("Object has the 'sequence_type' property set.")
            doc['meta']['sequence_type'] = self._sequence_type

        return doc

    @staticmethod
    def search(query="\"host_epigenetics_raw_seq_set\"[node_type]"):
        """
        Searches the OSDF database through all HostEpigeneticsRawSeqSet
        nodes. Any criteria the user wishes to add is provided by the user
        in the query language specifications provided in the OSDF
        documentation. A general format is (including the quotes and brackets):

        "search criteria"[field to search]

        If there are any results, they are returned as a
        HostEpigeneticsRawSeqSet instance, otherwise an empty list will be
        returned.

        Args:
            query (str): The query for the OSDF framework. Defaults to the
                         HostEpigeneticsRawSeqSet node type.

        Returns:
            Returns an array of HostEpigeneticsRawSeqSet objects. It returns
            an empty list if there are no results.
        """
        module_logger.debug("In search.")

        session = iHMPSession.get_session()
        module_logger.info("Got iHMP session.")

        if query != '"host_epigenetics_raw_seq_set"[node_type]':
            query = '({}) && "host_epigenetics_raw_seq_set"[node_type]'.format(query)

        module_logger.debug("Submitting OQL query: %s", query)

        raw_seq_set_data = session.get_osdf().oql_query("ihmp", query)

        all_results = raw_seq_set_data['results']

        result_list = list()

        if len(all_results) > 0:
            for result in all_results:
                raw_seq_set_result = HostEpigeneticsRawSeqSet. \
                                      load_host_epigenetics_raw_seq_set(result)
                result_list.append(raw_seq_set_result)

        return result_list

    @staticmethod
    def load_host_epigenetics_raw_seq_set(seq_set_data):
        """
        Takes the provided JSON string and converts it to a
        HostEpigeneticsRawSeqSet object.

        Args:
            seq_set_data (str): The JSON string to convert

        Returns:
            Returns a HostEpigeneticsRawSeqSet instance.
        """
        module_logger.info("Creating a template %s.", __name__)
        seq_set = HostEpigeneticsRawSeqSet()

        module_logger.debug("Filling in %s details.", __name__)

        # The attributes commmon to all iHMP nodes
        seq_set._set_id(seq_set_data['id'])
        seq_set.version = seq_set_data['ver']
        seq_set.links = seq_set_data['linkage']

        # The attributes that are required
        seq_set.assay_type = seq_set_data['meta']['assay_type']
        seq_set.checksums = seq_set_data['meta']['checksums']
        seq_set.comment = seq_set_data['meta']['comment']
        seq_set.exp_length = seq_set_data['meta']['exp_length']
        seq_set.format = seq_set_data['meta']['format']
        seq_set.format_doc = seq_set_data['meta']['format_doc']
        seq_set.seq_model = seq_set_data['meta']['seq_model']
        seq_set.size = seq_set_data['meta']['size']
        seq_set.tags = seq_set_data['meta']['tags']
        seq_set.study = seq_set_data['meta']['study']
        # We need to use the private attribute here because there is no
        # public setter.
        seq_set._urls = seq_set_data['meta']['urls']

        # Optional fields.
        if 'sequence_type' in seq_set_data['meta']:
            seq_set.sequence_type = seq_set_data['meta']['sequence_type']

        if 'private_files' in seq_set_data['meta']:
            seq_set.private_files = seq_set_data['meta']['private_files']

        module_logger.debug("Returning loaded %s", __name__)
        return seq_set

    @staticmethod
    def load(seq_set_id):
        """
        Loads the data for the specified input ID from OSDF to this object. If
        the provided ID does not exist, then an error message is provided
        stating the project does not exist.

        Args:
            seq_set_id (str): The OSDF ID for the document to load.

        Returns:
            A HostEpigeneticsRawSeqSet object with all the available OSDF
            data loaded into it.
        """
        module_logger.debug("In load. Specified ID: %s", seq_set_id)

        session = iHMPSession.get_session()
        module_logger.info("Got iHMP session.")
        seq_set_data = session.get_osdf().get_node(seq_set_id)
        seq_set = HostEpigeneticsRawSeqSet.load_host_epigenetics_raw_seq_set(seq_set_data)

        module_logger.debug("Returning loaded %s", __name__)

        return seq_set

    def _upload_data(self):
        self.logger.debug("In _upload_data.")

        session = iHMPSession.get_session()

        study = self._study

        study2dir = {
            "ibd": "ibd",
            "preg_preterm": "ptb",
            "prediabetes": "t2d"
        }

        if study not in study2dir:
            raise ValueError("Invalid study. No directory mapping for %s" % study)

        study_dir = study2dir[study]

        remote_base = os.path.basename(self._local_file)

        valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
        remote_base = ''.join(c for c in remote_base if c in valid_chars)
        remote_base = remote_base.replace(' ', '_') # No spaces in filenames

        remote_path = "/".join(["/" + study_dir, "epigenetics", "host",
                                "raw", remote_base])
        self.logger.debug("Remote path for this file will be %s.", remote_path)

        # Upload the file to the iHMP aspera server
        upload_result = aspera.upload_file(HostEpigeneticsRawSeqSet.aspera_server,
                                           session.username,
                                           session.password,
                                           self._local_file,
                                           remote_path)

        if not upload_result:
            self.logger.error("Experienced an error uploading the data. "
                              "Aborting save.")
            raise Exception("Unable to load host epigenetics raw sequence set.")
        else:
            self._urls = ["fasp://" + HostEpigeneticsRawSeqSet.aspera_server + remote_path]

    def save(self):
        """
        Saves the data in OSDF. The JSON form of the current data for the
        instance is validated in the save function. If the data is not valid,
        then the data will not be saved. If the instance was saved previously,
        then the node ID is assigned the alpha numeric found in the OSDF
        instance. If not saved previously, then the node ID is 'None', and upon
        a successful save, will be assigned to the alphanumeric ID found in
        OSDF.

        Args:
            None

        Returns;
            True if successful, False otherwise.
        """
        self.logger.debug("In save.")

        if not self.is_valid():
            self.logger.error("Cannot save, data is invalid")
            return False

        session = iHMPSession.get_session()
        self.logger.info("Got iHMP session.")

        success = False

        if self._private_files:
            self._urls = ["<private>"]
        else:
            try:
                self._upload_data()
            except Exception as uploadException:
                self.logger.exception(uploadException)
                # Don't bother continuing...
                return False

        osdf = session.get_osdf()

        if self.id is None:
            self.logger.info("About to insert a new %s OSDF node.", __name__)

            # Get the JSON form of the data and load it
            self.logger.info("Converting %s to parsed JSON form.", __name__)
            data = json.loads(self.to_json())

            try:
                self.logger.info("Attempting to save a new node.")
                node_id = osdf.insert_node(data)

                self._set_id(node_id)
                self._version = 1

                self.logger.info("Save for %s %s successful.", __name__, node_id)
                self.logger.info("Setting ID for %s %s.", __name__, node_id)

                success = True
            except Exception as saveException:
                self.logger.exception(saveException)
                self.logger.error("An error occurred while saving %s. Reason: %s",
                                  __name__,
                                  saveException
                                 )
        else:
            self.logger.info("%s already has an ID, so we do an update (not an insert).",
                             __name__
                            )

            try:
                seq_set_data = self._get_raw_doc()
                seq_set_id = self._id
                self.logger.info("Attempting to update %s with ID: %s.", __name__, seq_set_id)
                osdf.edit_node(seq_set_data)
                self.logger.info("Update for %s %s successful.", __name__, seq_set_id)

                seq_set_data = osdf.get_node(seq_set_id)
                latest_version = seq_set_data['ver']

                self.logger.debug("The version of this %s is now %s",
                                  __name__, str(latest_version)
                                 )
                self._version = latest_version

                success = True
            except Exception as update_exception:
                self.logger.exception(update_exception)
                self.logger.error("An error occurred while updating %s %s. " + \
                                  "Reason: %s", __name__, self._id,
                                  update_exception
                                 )

        self.logger.debug("Returning %s", str(success))
        return success