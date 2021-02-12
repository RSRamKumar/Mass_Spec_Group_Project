"""Unit tests for protein_query module"""
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

class TestProteinSearcher:
    """Unit tests for the ProteinSearcher class"""
    def test_protein_query(self):
        """unit tests to ensure the correct mapping of peptides to proteins"""
        db_instance = DbSearcher(mzml_file=mzml_file_path, fasta_file=fasta_file_path)
        results = db_instance.db_searcher()
        peptide_df = db_instance.peptide_info_df

        protein_instance = ProteinSearcher(peptide_list=peptide_df)
        protein_instance.download_protein_info()

        protein_atlas_results = protein_instance.protein_matches
        assert isinstance(protein_atlas_results, dict)
        # print([i for i in protein_atlas_results.keys()])
        assert [i for i in protein_atlas_results.keys()] == ["DFASSGGYVLHLHR", "IALSRPNVEVVALNDPFITNDYAAYMFK",
                                                             "RPGADSDIGGFGGLFDLAQAGFR"]
        assert protein_atlas_results["DFASSGGYVLHLHR"] == []
        assert protein_atlas_results["RPGADSDIGGFGGLFDLAQAGFR"] == []
        assert protein_atlas_results["IALSRPNVEVVALNDPFITNDYAAYMFK"] == [{'location': '19',
                                                                          'peptide': 'LALSRPNVEVVALNDPFLTNDYAAYMFK',
                                                                          'protein': 'Microbe_sp|P00359|G3P3_YEAST'}]
