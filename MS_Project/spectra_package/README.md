# Package Readme


## Peptide Atlas API - protein_query.py


### Documentation: 

http://www.peptideatlas.org/api/promast/v1/map

### Parameters:

* peptide :    peptide sequence to search
* proteome :   name of the reference proteome to search
* fuzzy :      number of wildcards to consider (0-3)
* tolerance :  mass tolerance for matching wildcards
* output : json or tsv

Example: http://www.peptideatlas.org/api/promast/v1/map?proteome=Human&peptide=ALFLETEQLK&fuzzy=3&tolerance=0.0001

### Alternative APIs

#### UniProt EBI
UniProt 'Peptide Search' is a separate tool, apparently not accessible by the UniProt REST API. http://insideuniprot.blogspot.com/2016/09/a-new-peptide-search-tool-now-in-uniprot.html
EBI Proteins API: http://www.ebi.ac.uk/proteins/api/doc
API Citation: Andrew Nightingale, Ricardo Antunes, Emanuele Alpi, Borisas Bursteinas, Leonardo Gonzales, Wudong Liu, Jie Luo, Guoying Qi, Edd Turner, Maria Martin, The Proteins API: accessing key integrated protein and genome information, Nucleic Acids Research, Volume 45, Issue W1, 3 July 2017, Pages W539–W544, https://doi.org/10.1093/nar/gkx237
API Publication: https://academic.oup.com/nar/article/45/W1/W539/3106040#90592569
=> Peptide Atlas query is included

#### Protein Information Resource
Searches UniProt and others. Uses a custom OpenAPI called Peptide Match API. Is available as python scripts for download for integration.
https://research.bioinformatics.udel.edu/peptidematch/api/v2/

#### Nextprot (not further investigated)
https://www.nextprot.org/

