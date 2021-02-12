
import numpy
import pandas as pd
from pyopenms import *
import sys
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DbSearcher:
    """
        Class that compares mzML file and fasta file to obtain peptide properties

        :parameter:
            mzml_file: mzML file containing Mass Spectrum data
            fasta_file: fasta file to be compared with mzML file

        :return:
            Creates a data frame containing information about peptides contained in the mzML file
    """

    def __init__(self, mzml_file: str, fasta_file: str):
        self.fasta_file = fasta_file
        self.mzml_file = mzml_file

    def db_searcher(self) ->pd.DataFrame:
        """
        db_searcher method uses SimpleSearchEngineAlgorithm that searches mzML file against fasta database of protein sequences
        :return: Dataframe containing peptide information

        """

        # OpenMS Peptide Query
        protein_ids = []
        peptide_ids = []

        #SimpleSearchEngineAlgorithm compares mzML file against fasta file, and it gives an output that contains the number of peptides and the proteins in the database and how many spectra were matched to peptides and proteins
        if self.mzml_file and self.fasta_file:
            SimpleSearchEngineAlgorithm().search(self.mzml_file, self.fasta_file, protein_ids, peptide_ids)
            logger.info("MS file and fasta file were accepted as input files")
        else:
            logger.error("Please enter appropriate input files ")


        # Results Preprocessing
        mz_lst_1 = []
        mz_lst_2 = []

        MZ = int()
        RT = int()
        meta_val = int()
        score_type = int()
        hit_rank = int()
        hit_charge = int()
        hit_seq = str()
        hit_monoisotopic = int()
        ppm_error = int()
        hit_score = int()

        if peptide_ids != []:
            logger.info("Peptides have successfully been identified by SimpleSearchEngineAlgorithm")
            #Exploring the individual hits, and gathering the peptide information
            for peptides in peptide_ids:
                MZ = round(peptides.getMZ(), 2)
                RT = round(peptides.getRT(), 2)
                meta_val = peptides.getMetaValue("scan_index")
                score_type = peptides.getScoreType()
                mz_lst_1.append([MZ, RT, meta_val, score_type])

                for hit in peptides.getHits():
                    hit_rank = round(hit.getRank(), 2)
                    hit_charge = round(hit.getCharge(), 2)
                    hit_seq = hit.getSequence()
                    hit_monoisotopic = round(
                        hit.getSequence().getMonoWeight(Residue.ResidueType.Full, hit.getCharge()) / hit.getCharge(), 2)
                    ppm_error = round(abs(hit_monoisotopic - peptides.getMZ()) / hit_monoisotopic * 10 ** 6, 2)
                    hit_score = round(hit.getScore(), 2)

                mz_lst_2.append([hit_rank, hit_charge, str(hit_seq), hit_monoisotopic, ppm_error, hit_score])

            final_lst = list()
            for i in range(len(mz_lst_2)):
                final_lst.append(mz_lst_1[i] + mz_lst_2[i])

            #Generating a dataframe that contains the peptide information
            if final_lst != []:
                self.peptide_info_df = pd.DataFrame(final_lst)
                self.peptide_info_df.columns = ["Peptide ID m/z", "Peptide ID RT", "Peptide scan index", "Peptide ID score type",
                              "Peptide hit rank", "Peptide hit charge", "Peptide hit sequence", "Peptide hit monoisotopic m/z",
                              "Peptide ppm error", "Peptide hit score"]
                logging.info("A dataframe containing the properties of peptides was generated")

            else:
                logging.error("A dataframe containing the properties of peptides was not generated. Please check the inputs")

            # For depicting entire columns in the dataframe, pd.option_context was used
            with pd.option_context('display.max_rows', None, 'display.max_columns',
                                   None):  # more options can be specified also
                print(self.peptide_info_df)
                return self.peptide_info_df


        else:
            print("No Peptide Data found! Please try a different reference Fasta file or MS spectrum file!")
            logger.warning("Peptides have not been identified by SimpleSearchEngineAlgorithm. Please try a different reference fasta file or MS file")


if __name__ == "__main__":
    mzml_input = sys.argv[1]
    fasta_input = sys.argv[2]
    searcher = DbSearcher(mzml_file=mzml_input, fasta_file=fasta_input)
    result = searcher.db_searcher()

