"""Unit tests for db_searcher module """
from db_searcher import DbSearcher
from protein_query import ProteinSearcher
import os
import pandas as pd

TEST_FOLDER = os.path.dirname(__file__)
DB_SEARCHER_DATA_FOLDER = os.path.join(TEST_FOLDER,"db_searcher_data")
# DB_SEARCHER_DATA_FOLDER is a folder exclusive for this unit test
# It is expected to contain 2 files (msML and fasta)
# might not work, when more than 2 files are there
fasta_file,mzml_file=([file for file in os.listdir(DB_SEARCHER_DATA_FOLDER)])

# Absolute paths
mzml_file_path = os.path.join(DB_SEARCHER_DATA_FOLDER, mzml_file)
fasta_file_path = os.path.join(DB_SEARCHER_DATA_FOLDER, fasta_file)



class TestDBSearcher:

    def test_parser(self):
        """Checks whether the DbSearcher class correctly extracts the required attributes with correct values"""
        db_instance = DbSearcher(mzml_file=mzml_file_path,fasta_file=fasta_file_path)
        results = db_instance.db_searcher()
        peptide_df = db_instance.peptide_info_df
        assert isinstance(peptide_df, pd.DataFrame)
        assert peptide_df.shape == (3,10) # check for df dimension
        # check  for correctness of values for corresponding columns
        assert [i for i in peptide_df['Peptide ID m/z']] == [520.26,1063.21,775.39]
        assert [i for i in peptide_df['Peptide ID RT']] == [2655.10, 4587.67, 4923.78]
        assert [i for i in peptide_df['Peptide scan index']] == [0,1,2]
        assert [i for i in peptide_df['Peptide ID score type']] == ["hyperscore", "hyperscore", "hyperscore"]
        assert [i for i in peptide_df['Peptide hit rank']] == [1,1,1]
        assert [i for i in peptide_df['Peptide hit charge']] == [3,3,3]
        assert [i for i in peptide_df['Peptide hit monoisotopic m/z']] == [520.26, 1063.21, 775.39]
        assert [i for i in peptide_df['Peptide ppm error']] == [5.42 , 0.15, 3.60]
        assert [i for i in peptide_df['Peptide hit score']] == [16.84 , 42.22, 34.94]


