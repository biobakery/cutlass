#!/usr/bin/env python

import json
import logging
import os
import string
from iHMPSession import iHMPSession
from Base import Base
from aspera import aspera


# Create a module logger named after the module
module_logger = logging.getLogger(__name__)
# Add a NullHandler for the case if no logging is configured by the application
module_logger.addHandler(logging.NullHandler())

class WgsAssembledSeqSet(Base):
    """
    The class encapsulating the Wgs Assembled Sequence Set data for the iHMP.
    This class contains all the fields required to save a Wgs Assembled
    Sequence Set object in the OSDF instance.

    Attributes:
        namespace (str): The namespace this class will use in the OSDF instance

        aspera_server (str): The name of the aspera where files are transferred to

        date_format (str): The format of the date
    """
    namespace = "ihmp"

    aspera_server = "aspera.ihmpdcc.org"

    date_format = '%Y-%m-%d'

    def __init__(self):
        """
        Constructor for the WgsAssembledSeqSet class. This initializes the fields specific
        to the WgsAssembledSeqSet class, and inherits from the Base class.

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

        # These are particular to WgsAssembledSeqSet objects
        self._assembler = None
        self._assembly_name = None
        self._checksums = None
        self._comment = None
        self._format = None
        self._format_doc = None
        self._sequence_type = None
        self._size = None
        self._study = None
        self._local_file = None
        self._urls = ['']

        # Optional
        self._date = None
        self._sop = None

    @property
    def assembler(self):
        """
        str: The software and version used to generate the assembly.
        """
        self.logger.debug("In assembler getter.")

        return self._assembler

    @assembler.setter
    def assembler(self, assembler):
        """
        The setter for the assembler.

        Args:
            assembler (str): The software and version used to generate the
            assembly.

        Returns:
            None
        """
        self.logger.debug("In assembler setter.")

        if type(assembler) != str:
            raise ValueError("assembler must be a string.")

        self._assembler = assembler

    @property
    def assembly_name(self):
        """
        str: Get the name of the assembly provided by the submitter.
        """
        self.logger.debug("In assembly_name getter.")

        return self._assembly_name

    @assembly_name.setter
    def assembly_name(self, assembly_name):
        """
        Name/version of the assembly provided by the submitter.

        Args:
            assembly_name (str): Name/version of the assembly provided by the
            submitter.

        Returns:
            None
        """
        self.logger.debug("In assembly_name setter.")

        if type(assembly_name) != str:
            raise ValueError("assembly_name must be a string.")

        self._assembly_name = assembly_name

    @property
    def checksums(self):
        """ str: One or more checksums used to ensure file integrity. """
        self.logger.debug("In checksums getter.")

        return self._checksums

    @checksums.setter
    def checksums(self, checksums):
        """
        The setter for the WgsAssembledSeqSet checksums.

        Args:
            checksums (dict): The checksums for the WgsAssembledSeqSet.

        Returns:
            None
        """
        self.logger.debug("In checksums setter.")

        if 'md5' not in checksums:
            raise ValueError("Checksum data must contain at least the 'md5' value")

        self._checksums = checksums

    @property
    def comment(self):
        """
        str: Free-text comment.
        """
        self.logger.debug("In comment getter.")

        return self._comment

    @comment.setter
    def comment(self, comment):
        """
        The setter for the WgsAssembledSeqSet comment. The comment must be a string,
        and less than 512 characters.

        Args:
            comment (str): The new comment to add to the string.

        Returns:
            None
        """
        self.logger.debug("In comment setter.")

        if type(comment) != str:
            raise ValueError("comment must be a string.")

        if len(comment) > 512:
            raise Exception("Comment is too long, must be less than 512 characters.")

        self._comment = comment

    @property
    def format(self):
        """ str: The file format of the sequence file """
        self.logger.debug("In format getter.")

        return self._format

    @format.setter
    def format(self, format_str):
        """
        The setter for the WgsAssembledSeqSet format. This must be either fasta or fastq.

        Args:
            format_str (str): The new format string for the current object.

        Returns:
            None
        """
        self.logger.debug("In format setter.")

        if type(format_str) != str:
            raise ValueError("format must be a string.")

        formats = ["fasta", "fastq"]
        if format_str in formats:
            self._format = format_str
        else:
            raise Exception("Format must be fasta or fastq only.")

    @property
    def format_doc(self):
        """ str: URL for documentation of file format. """
        self.logger.debug("In format_doc getter.")

        return self._format_doc

    @format_doc.setter
    def format_doc(self, format_doc):
        """
        The setter for the WgsAssembledSeqSet format doc.

        Args:
            format_doc (str): The new format_doc for the current object.

        Returns:
            None
        """
        self.logger.debug("In format_doc setter.")

        if type(format_doc) != str:
            raise ValueError("format_doc must be a string.")

        self._format_doc = format_doc

    @property
    def local_file(self):
        """ str: URL to the local file to upload to the server. """
        self.logger.debug("In local_file getter.")

        return self._local_file

    @local_file.setter
    def local_file(self, local_file):
        """
        The setter for the WgsAssembledSeqSet local file.

        Args:
            local_file (str): The URL to the local file that should
                              be uploaded to the server.

        Returns:
            None
        """
        self.logger.debug("In local_file setter.")

        if type(local_file) != str:
            raise ValueError("local_file must be a string.")

        self._local_file = local_file

    @property
    def sequence_type(self):
        """ str: Specifies whether the file contains peptide or nucleotide data. """
        self.logger.debug("In sequence_type getter.")

        return self._sequence_type

    @sequence_type.setter
    def sequence_type(self, sequence_type):
        """
        The setter for the WgsAssembledSeqSet sequence type. This must be either
        peptide or nucleotide.

        Args:
            sequence_type (str): The new sequence type.

        Returns:
            None
        """
        self.logger.debug("In sequence_type setter.")

        if type(sequence_type) != str:
            raise ValueError("sequence_type must be a string.")

        types = ["peptide", "nucleotide"]
        if sequence_type in types:
            self._sequence_type = sequence_type
        else:
            raise Exception("Sequence type must be either peptide or nucleotide")

    @property
    def size(self):
        """ int: The size of the file in bytes. """
        self.logger.debug("In size getter.")

        return self._size

    @size.setter
    def size(self, size):
        """
        The setter for the WgsAssembledSeqSet size.

        Args:
            size (int): The size of the seq set.

        Returns:
            None
        """
        self.logger.debug("In size setter.")

        if type(size) != int:
            raise ValueError("The size must be a string.")

        if size < 0:
            raise ValueError("The size must be non-negative.")

        self._size = size

    @property
    def study(self):
        """ str: One of the 3 studies that are part of the iHMP. """
        self.logger.debug("In study getter.")

        return self._study

    @study.setter
    def study(self, study):
        """
        The setter for the WgsAssembledSeqSet study. This is restricted to be either
        preg_preterm, ibd, or prediabetes.

        Args:
            study (str): The study of the seq set.

        Returns:
            None
        """
        self.logger.debug("In study setter.")

        studies = ["preg_preterm", "ibd", "prediabetes"]

        if type(study) != str:
            raise ValueError("study must be a string.")

        if study in studies:
            self._study = study
        else:
            raise Exception("Not a valid study")

    @property
    def urls(self):
        """
        array: An array of URL from where the file can be obtained,
               http, ftp, fasp, etc... """
        self.logger.debug("In urls getter.")

        return self._urls

    @staticmethod
    def required_fields():
        """
        A static method. The required fields for the class.

        Args:
            None
        Returns:
            Tuple of strings of the required properties.
        """
        module_logger.debug("In required fields.")
        return ("assembler", "assembly_name", "checksums", "comment",
                "format", "format_doc", "sequence_type", "size",
                "study", "tags", "urls", "local_file")

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
            An object representation of the JSON document.
        """
        self.logger.debug("In _get_raw_doc.")

        assembled_doc = {
            'acl': {
                'read': [ 'all' ],
                'write': [ WgsAssembledSeqSet.namespace ]
            },
            'linkage': self._links,
            'ns': WgsAssembledSeqSet.namespace,
            'node_type': 'wgs_assembled_seq_set',
            'meta': {
                "assembler": self._assembler,
                "assembly_name": self._assembly_name,
                "checksums": self._checksums,
                "comment": self._comment,
                "format": self._format,
                "format_doc": self._format_doc,
                "sequence_type": self.sequence_type,
                "size": self._size,
                "study": self._study,
                "urls": self._urls,
                "subtype": self._study,
                'tags': self._tags
            }
        }

        if self._id is not None:
           self.logger.debug(__name__ + " object has the OSDF id set.")
           assembled_doc['id'] = self._id

        if self._version is not None:
           self.logger.debug(__name__ + " object has the OSDF version set.")
           assembled_doc['ver'] = self._version

        # Handle optional properties
        if self._date is not None:
           self.logger.debug(__name__ + " object has the date set.")
           assembled_doc['meta']['date'] = self._date

        if self._sop is not None:
           self.logger.debug(__name__ + " object has the sop set.")
           assembled_doc['meta']['sop'] = self._sop

        return assembled_doc

    def to_json(self, indent=4):
        """
        Converts the raw JSON doc (the dictionary representation)
        to a printable JSON string.

        Args:
            indent (int): The indent for each successive line of the JSON string output

        Returns:
            A printable JSON string
        """
        self.logger.debug("In to_json.")

        visit_doc = self._get_raw_doc()

        self.logger.debug("Encoding structure to JSON.")

        json_str = json.dumps(visit_doc, indent=indent)

        self.logger.debug("Dump to JSON successful. Length: %s characters" % len(json_str))

        return json_str

    @staticmethod
    def search(query = "\"wgs_assembled_seq_set\"[node_type]"):
        """
        Searches the OSDF database through all WgsAssembledSeqSet node types. Any
        criteria the user wishes to add is provided by the user in the query language
        specifications provided in the OSDF documentation. A general format
        is (including the quotes and brackets):

        "search criteria"[field to search]

        If there are any results, they are returned as a WgsAssembledSeqSet instance,
        otherwise an empty list will be returned.

        Args:
            query (str): The query for the OSDF framework. Defaults to the
                         WgsAssembledSeqSet node type.

        Returns:
            Returns an array of WgsAssembledSeqSet objects. It returns an empty list if
            there are no results.
        """
        module_logger.debug("In search.")
        #searching without any parameters will return all different results
        session = iHMPSession.get_session()
        module_logger.info("Got iHMP session.")

        if query != "\"wgs_assembled_seq_set\"[node_type]":
            query = query + " && \"wgs_assembled_seq_set\"[node_type]"

        wgsAssembledSeqSet_data = session.get_osdf().oql_query(WgsAssembledSeqSet.namespace, query)

        all_results = wgsAssembledSeqSet_data['results']

        result_list = list()

        if len(all_results) > 0:
            for result in all_results:
                wgs_result = WgsAssembledSeqSet.load_wgsAssembledSeqSet(result)
                result_list.append(wgs_result)

        return result_list

    @staticmethod
    def load_wgsAssembledSeqSet(seq_set_data):
        """
        Takes the provided JSON string and converts it to a WgsAssembledSeqSet
        object

        Args:
            seq_set_data (str): The JSON string to convert

        Returns:
            Returns a WgsAssembledSeqSet instance.
        """
        module_logger.info("Creating a template " + __name__ + ".")
        seq_set = WgsAssembledSeqSet()

        module_logger.debug("Filling in " + __name__ + " details.")

        # The attributes commmon to all iHMP nodes
        seq_set._set_id(seq_set_data['id'])
        seq_set._version = seq_set_data['ver']
        seq_set._links = seq_set_data['linkage']

        # The attributes that are particular to WgsAssembledSeqSet documents
        seq_set._checksums = seq_set_data['meta']['checksums']
        seq_set._comment = seq_set_data['meta']['comment']
        seq_set._exp_length = seq_set_data['meta']['exp_length']
        seq_set._format = seq_set_data['meta']['format']
        seq_set._format_doc = seq_set_data['meta']['format_doc']
        seq_set._seq_model = seq_set_data['meta']['seq_model']
        seq_set._size = seq_set_data['meta']['size']
        seq_set._urls = seq_set_data['meta']['urls']
        seq_set._tags = seq_set_data['meta']['tags']
        seq_set._study = seq_set_data['meta']['study']

        if 'sequence_type' in seq_set_data['meta']:
            module_logger.info(__name__ + " data has 'sequence_type' present.")
            seq_set._sequence_type = seq_set_data['meta']['sequence_type']

        module_logger.debug("Returning loaded " + __name__)

        return seq_set

    @staticmethod
    def load(seq_set_id):
        """
        Loads the data for the specified input ID from the OSDF instance to this object.
        If the provided ID does not exist, then an error message is provided stating the
        project does not exist.

        Args:
            seq_set_id (str): The OSDF ID for the document to load.

        Returns:
            A WgsAssembledSeqSet object with all the available OSDF data loaded into it.
        """
        module_logger.debug("In load. Specified ID: %s" % seq_set_id)

        session = iHMPSession.get_session()
        module_logger.info("Got iHMP session.")

        seq_set_data = session.get_osdf().get_node(seq_set_id)

        module_logger.info("Creating a template " + __name__ + ".")
        seq_set = WgsAssembledSeqSet()

        module_logger.debug("Filling in " + __name__ + " details.")

        # The attributes commmon to all iHMP nodes
        seq_set._set_id(seq_set_data['id'])
        seq_set._version = seq_set_data['ver']
        seq_set._links = seq_set_data['linkage']

        # The attributes that are particular to WgsAssembledSeqSet documents
        seq_set._checksums = seq_set_data['meta']['checksums']
        seq_set._comment = seq_set_data['meta']['comment']
        seq_set._exp_length = seq_set_data['meta']['exp_length']
        seq_set._format = seq_set_data['meta']['format']
        seq_set._format_doc = seq_set_data['meta']['format_doc']
        seq_set._seq_model = seq_set_data['meta']['seq_model']
        seq_set._size = seq_set_data['meta']['size']
        seq_set._urls = seq_set_data['meta']['urls']
        seq_set._tags = seq_set_data['meta']['tags']
        seq_set._study = seq_set_data['meta']['study']

        # Optional properties
        if 'date' in seq_set_data['meta']:
            module_logger.info(__name__ + " data has 'date' present.")
            seq_set._date = seq_set_data['meta']['date']

        if 'sop' in seq_set_data['meta']:
            module_logger.info(__name__ + " data has 'sop' present.")
            seq_set._sop = seq_set_data['meta']['sop']

        module_logger.debug("Returning loaded " + __name__)

        return seq_set

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
            self.logger.info("Validation did not succeed for " + __name__ + ".")
            problems.append(error_message)

        if self._local_file is None:
            problems.append("Local file is not yet set.")
        elif not os.path.isfile(self._local_file):
            problems.append("Local file does not point to an actual file.")

        if 'computed_from' not in self._links.keys():
            problems.append("Must add a 'computed_from' link to a wgs_dna_prep.")

        self.logger.debug("Number of validation problems: %s." % len(problems))

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

        (valid, error_message) = session.get_osdf().validate_node(document)

        if self._local_file is None:
            self.logger.error("Must set the local file of the sequence set.")
            valid = False
        elif not os.path.isfile(self._local_file):
            self.logger.error("Local file does not point to an actual file.")
            valid = False

        if 'computed_from' not in self._links.keys():
            self.logger.error("Must have of 'computed_from' linkage.")
            valid = False

        self.logger.debug("Valid? %s" % str(valid))

        return valid

    def save(self):
        """
        Saves the data in the current instance. The JSON form of the current data
        for the instance is validated in the save function. If the data is not valid,
        then the data will not be saved. If the instance was saved previously, then
        the node ID is assigned the alpha numeric found in the OSDF instance. If not
        saved previously, then the node ID is 'None', and upon a successful, will be
        assigned to the alpha numeric ID found in the OSDF instance. Also, the
        version is updated as the data is saved in the OSDF instance.

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

        study = self._study

        study2dir = { "ibd": "ibd",
                      "preg_preterm": "ptb",
                      "prediabetes": "t2d"
                    }

        if study not in study2dir:
            raise ValueError("Invalid study. No directory mapping for %s" % study)

        study_dir = study2dir[study]

        remote_base = os.path.basename(self._local_file);

        valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
        remote_base = ''.join(c for c in remote_base if c in valid_chars)
        remote_base = remote_base.replace(' ', '_') # No spaces in filenames

        remote_path = "/".join(["/" + study_dir, "genome", "microbiome", "wgs",
                                "hmasm", remote_base])
        self.logger.debug("Remote path for this file will be %s." % remote_path)

        # Upload the file to the iHMP aspera server
        upload_result = aspera.upload_file(WgsAssembledSeqSet.aspera_server,
                                           session.username,
                                           session.password,
                                           self._local_file,
                                           remote_path)

        if not upload_result:
            self.logger.error("Experienced an error uploading the sequence set. Aborting save.")
            return False
        else:
            self._urls = [ "fasp://" + WgsAssembledSeqSet.aspera_server + remote_path ]

        if self.id is None:
            # The document has not yet been save
            seq_set_data = self._get_raw_doc()
            self.logger.info("Got the raw JSON document.")

            try:
                self.logger.info("Attempting to save a new node.")
                node_id = session.get_osdf().insert_node(seq_set_data)
                self.logger.info("Save for " + __name__ + " %s successful." % node_id)
                self.logger.info("Setting ID for " + __name__ + " %s." % node_id)
                self._set_id(node_id)
                self._version = 1
                success = True
            except Exception as e:
                self.logger.error("An error occurred while saving " + __name__ + ". " +
                                  "Reason: %s" % e)
        else:
            seq_set_data = self._get_raw_doc()

            try:
                self.logger.info("Attempting to update " + __name__ + " with ID: %s." % self._id)
                session.get_osdf().edit_node(seq_set_data)
                self.logger.info("Update for " + __name__ + " %s successful." % self._id)
                success = True
            except Exception as e:
                self.logger.error("An error occurred while updating " +
                                  __name__ + " %s. Reason: %s" % self._id, e)

        self.logger.debug("Returning " + str(success))

        return success