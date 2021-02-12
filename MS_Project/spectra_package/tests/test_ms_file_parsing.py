"""MS file parsing tests
The Dataframe returned after the parsing is huge and hence it is
cumbersome to check for the correctness of each and every value.
Therefore, a check is made only on the object type and its dimensionality
"""

from ms_file_parsing import MSFileParser
import os
import pandas as pd
TEST_FOLDER = os.path.dirname(__file__)
MS_FILE_PATH_mzML = os.path.join(TEST_FOLDER, "data/tiny.pwiz.1.1.mzML")
MS_FILE_PATH_mzXML = os.path.join(TEST_FOLDER, "data/raftflow10.mzXML")

class TestMSFileParser:
    """Unit tests for the MSFileParser class."""

    def test_parser(self):
        """Checks whether the MSFileParser class correctly extracts the required attributes"""

        # test for mzML file
        parsing_instance_mzML = MSFileParser(ms_file_input=MS_FILE_PATH_mzML)
        output_mzML = parsing_instance_mzML.parser()
        output_mzML_shape = output_mzML.shape
        assert isinstance(output_mzML,pd.DataFrame)  # check for returned output is a dataframe
        assert output_mzML_shape == (3,5)            # check for correct dimension

        # test for mzXML file
        parsing_instance_mzXML = MSFileParser(ms_file_input=MS_FILE_PATH_mzXML)
        output_mzXML = parsing_instance_mzXML.parser()
        output_mzXML_shape = output_mzXML.shape
        assert isinstance(output_mzXML, pd.DataFrame)  # check for returned output is a dataframe
        assert output_mzXML_shape == (4064, 5)         # check for correct dimension


