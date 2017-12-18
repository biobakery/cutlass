#!/usr/bin/env python

""" A unittest script for the Annotation module. """

import unittest
import json
import tempfile
from datetime import date

from cutlass import Annotation

from CutlassTestConfig import CutlassTestConfig
from CutlassTestUtil import CutlassTestUtil

# pylint: disable=W0703, C1801

class AnnotationTest(unittest.TestCase):
    """ A unit test class for the Annotation module. """

    session = None
    util = None

    @classmethod
    def setUpClass(cls):
        """ Setup for the unittest. """
        # Establish the session for each test method
        cls.session = CutlassTestConfig.get_session()

        cls.util = CutlassTestUtil()

    def testImport(self):
        """ Test the importation of the Annotation module. """
        success = False
        try:
            from cutlass import Annotation
            success = True
        except Exception:
            pass

        self.failUnless(success)
        self.failIf(Annotation is None)

    def testSessionCreate(self):
        """ Test the creation of a Annotation via the session. """
        success = False
        annot = None

        try:
            annot = self.session.create_annotation()

            success = True
        except Exception:
            pass

        self.failUnless(success)
        self.failIf(annot is None)

    def testAnnotationPipeline(self):
        """ Test the annotation_pipeline property. """
        annot = self.session.create_annotation()

        self.util.stringTypeTest(self, annot, "annotation_pipeline")

        self.util.stringPropertyTest(self, annot, "annotation_pipeline")

    def testChecksumsLegal(self):
        """ Test the checksums property with a legal value. """
        annot = self.session.create_annotation()
        success = False
        checksums = {"md5": "d8e8fca2dc0f896fd7cb4cb0031ba249"}

        try:
            annot.checksums = checksums
            success = True
        except Exception:
            pass

        self.assertTrue(success, "Able to use the checksums setter")

        self.assertEqual(annot.checksums['md5'], checksums['md5'],
                         "Property getter for 'checksums' works.")

    def testIllegalDate(self):
        """ Test the date property with an illegal value. """
        annot = self.session.create_annotation()

        with self.assertRaises(Exception):
            annot.date = "random"

    def testIllegalFutureDate(self):
        """ Test the date property with an illegal future date. """
        annot = self.session.create_annotation()
        success = False
        today = date.today()
        next_year = str(date(today.year + 1, today.month, today.day))

        try:
            annot.date = next_year
            success = True
        except Exception:
            pass

        self.assertFalse(success, "Annotation class rejects future dates.")

    def testLegalDate(self):
        """ Test the date property with a legal date. """
        annot = self.session.create_annotation()
        success = False
        test_date = "2015-07-27"

        try:
            annot.date = test_date
            success = True
        except Exception:
            pass

        self.assertTrue(success, "Able to use the date setter")

        self.assertEqual(annot.date, test_date, "Property getter for 'date' works.")

    def testFormat(self):
        """ Test the format property. """
        annot = self.session.create_annotation()

        self.util.stringTypeTest(self, annot, "format")

        self.util.stringPropertyTest(self, annot, "format")

    def testFormatDoc(self):
        """ Test the format_doc property. """
        annot = self.session.create_annotation()

        self.util.stringTypeTest(self, annot, "format_doc")

        self.util.stringPropertyTest(self, annot, "format_doc")

    def testOrfProcess(self):
        """ Test the orf_process property. """
        annot = self.session.create_annotation()

        self.util.stringTypeTest(self, annot, "orf_process")

        self.util.stringPropertyTest(self, annot, "orf_process")

    def testPrivateFiles(self):
        """ Test the private_files property. """
        annot = self.session.create_annotation()

        self.util.boolTypeTest(self, annot, "private_files")

        self.util.boolPropertyTest(self, annot, "private_files")

    def testSize(self):
        """ Test the size property. """
        annot = self.session.create_annotation()

        self.util.intTypeTest(self, annot, "size")

        self.util.intPropertyTest(self, annot, "size")

    def testStudy(self):
        """ Test the study property. """
        annot = self.session.create_annotation()

        self.util.stringTypeTest(self, annot, "study")

        self.util.stringPropertyTest(self, annot, "study")

    def testComment(self):
        """ Test the comment property. """
        annot = self.session.create_annotation()

        self.util.stringTypeTest(self, annot, "comment")

        self.util.stringPropertyTest(self, annot, "comment")

    def testToJson(self):
        """ Test the to_json() method. """
        annot = self.session.create_annotation()
        success = False

        annotation_pipeline = "test_annotation_pipeline"
        orf_process = "test_orf_process"
        study = "prediabetes"
        format_ = "gff3"
        format_doc = "test_format_doc"
        private_files = False

        annot.annotation_pipeline = annotation_pipeline
        annot.orf_process = orf_process
        annot.study = study
        annot.format = format_
        annot.format_doc = format_doc
        annot.private_files = private_files

        annot_json = None

        try:
            annot_json = annot.to_json()
            success = True
        except Exception:
            pass

        self.assertTrue(success, "Able to use 'to_json'.")
        self.assertTrue(annot_json is not None, "to_json() returned data.")

        parse_success = False

        try:
            annot_data = json.loads(annot_json)
            parse_success = True
        except Exception:
            pass

        self.assertTrue(parse_success,
                        "to_json() did not throw an exception.")
        self.assertTrue(annot_data is not None,
                        "to_json() returned parsable JSON.")

        self.assertTrue('meta' in annot_data, "JSON has 'meta' key in it.")

        self.assertEqual(annot_data['meta']['annotation_pipeline'],
                         annotation_pipeline,
                         "'annotation_pipeline' in JSON had expected value."
                        )

        self.assertEqual(annot_data['meta']['orf_process'],
                         orf_process,
                         "'orf_process' in JSON had expected value."
                        )

        self.assertEqual(annot_data['meta']['study'],
                         study,
                         "'study' in JSON had expected value."
                        )

        self.assertEqual(annot_data['meta']['format'],
                         format_,
                         "'format' in JSON had expected value."
                        )

        self.assertEqual(annot_data['meta']['format_doc'],
                         format_doc,
                         "'format_doc' in JSON had expected value."
                        )

        self.assertEqual(annot_data['meta']['private_files'],
                         private_files,
                         "'private_files' in JSON had expected value."
                        )

    def testDataInJson(self):
        """ Test the data resulting from the to_json() method. """
        annot = self.session.create_annotation()
        success = False
        comment = "test_comment"
        annotation_pipeline = "test_annotation_pipeline"
        format_ = "gff3"
        format_doc = "test_format_doc"

        annot.comment = comment
        annot.annotation_pipeline = annotation_pipeline
        annot.format = format_
        annot.format_doc = format_doc

        annot_json = None

        try:
            annot_json = annot.to_json()
            success = True
        except Exception:
            pass

        self.assertTrue(success, "Able to use 'to_json'.")
        self.assertTrue(annot_json is not None, "to_json() returned data.")

        parse_success = False

        try:
            annot_data = json.loads(annot_json)
            parse_success = True
        except Exception:
            pass

        self.assertTrue(parse_success,
                        "to_json() did not throw an exception.")
        self.assertTrue(annot_data is not None,
                        "to_json() returned parsable JSON.")

        self.assertTrue('meta' in annot_data, "JSON has 'meta' key in it.")

        self.assertEqual(annot_data['meta']['annotation_pipeline'],
                         annotation_pipeline,
                         "'annotation_pipeline' in JSON had expected value."
                        )

        self.assertEqual(annot_data['meta']['comment'],
                         comment,
                         "'comment' in JSON had expected value."
                        )

        self.assertEqual(annot_data['meta']['format'],
                         format_,
                         "'format' in JSON had expected value."
                        )

        self.assertEqual(annot_data['meta']['format_doc'],
                         format_doc,
                         "'format_doc' in JSON had expected value."
                        )

    def testId(self):
        """ Test the id property. """
        annot = self.session.create_annotation()

        self.assertTrue(annot.id is None,
                        "New template annotation has no ID.")

        with self.assertRaises(AttributeError):
            annot.id = "test"

    def testVersion(self):
        """ Test the version property. """
        annot = self.session.create_annotation()

        self.assertTrue(annot.version is None,
                        "New template annotation has no version.")

        with self.assertRaises(ValueError):
            annot.version = "test"

    def testTags(self):
        """ Test the tags property. """
        annot = self.session.create_annotation()

        tags = annot.tags
        self.assertTrue(type(tags) == list, "Annotation tags() method returns a list.")
        self.assertEqual(len(tags), 0, "Template annotation tags list is empty.")

        new_tags = ["tagA", "tagB"]

        annot.tags = new_tags
        self.assertEqual(annot.tags, new_tags, "Can set tags on an annotation.")

        json_str = annot.to_json()
        doc = json.loads(json_str)
        self.assertTrue('tags' in doc['meta'],
                        "JSON representation has 'tags' field in 'meta'.")

        self.assertEqual(doc['meta']['tags'], new_tags,
                         "JSON representation had correct tags after setter.")

    def testAddTag(self):
        """ Test the add_tag() method. """
        annot = self.session.create_annotation()

        annot.add_tag("test")
        self.assertEqual(annot.tags, ["test"], "Can add a tag to an annotation.")

        json_str = annot.to_json()
        doc = json.loads(json_str)

        self.assertEqual(doc['meta']['tags'], ["test"],
                         "JSON representation had correct tags after add_tag().")

        # Try adding the same tag yet again, shouldn't get a duplicate
        with self.assertRaises(ValueError):
            annot.add_tag("test")

        json_str = annot.to_json()
        doc2 = json.loads(json_str)

        self.assertEqual(doc2['meta']['tags'], ["test"],
                         "JSON document did not end up with duplicate tags.")

    def testRequiredFields(self):
        """ Test the required_fields() method. """
        required = Annotation.required_fields()

        self.assertEqual(type(required), tuple,
                         "required_fields() returns a tuple.")

        self.assertTrue(len(required) > 0,
                        "required_field() did not return empty value.")

    def testLoadSaveDeleteAnnotation(self):
        """ Extensive test for the load, edit, save and delete functions. """

        temp_file = tempfile.NamedTemporaryFile(delete=False).name

        # Attempt to save at all points before and after adding
        # the required fields
        annot = self.session.create_annotation()
        self.assertFalse(
            annot.save(),
            "Annoatation not saved successfully, no required fields"
        )

        annot.annotation_pipeline = "Test Annotation Pipeline"

        self.assertFalse(
            annot.save(),
            "Annotation not saved successfully, missing some required fields."
        )

        # Annotation nodes are "computed_from" wgs_assembled_seq_set nodes
        annot.links = {"computed_from": ["419d64483ec86c1fb9a94025f3b94551"]}

        annot.checksums = {"md5": "d8e8fca2dc0f896fd7cb4cb0031ba249"}
        annot.format = "gff3"
        annot.format_doc = "Test format_doc"
        annot.orf_process = "Test ORF process"
        annot.study = "prediabetes"
        annot.local_file = temp_file
        annot.size = 131313

        annot.add_tag("test")

        # Make sure annotation does not delete if it does not exist
        with self.assertRaises(Exception):
            annot.delete()

        self.assertTrue(annot.save() is True, "Annotation was saved successfully")

        # Load the annotation that was just saved from the OSDF instance
        annot_loaded = self.session.create_annotation()
        annot_loaded = annot_loaded.load(annot.id)

        # Check all fields were saved and loaded successfully
        self.assertEqual(annot.comment, annot_loaded.comment,
                         "Annotation comment not saved & loaded successfully")
        self.assertEqual(annot.tags[0], annot_loaded.tags[0],
                         "Annotation tags not saved & loaded successfully")

        # Deleted successfully
        self.assertTrue(annot.delete(), "Annotation was deleted successfully")

        # the object of the initial ID should not load successfully
        load_test = self.session.create_annotation()
        with self.assertRaises(Exception):
            load_test = load_test.load(annot.id)

if __name__ == '__main__':
    unittest.main()
