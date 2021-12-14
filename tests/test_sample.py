import unittest
from copy import deepcopy
from unittest.mock import patch

import pyrefinebio
from pyrefinebio import computed_file as prb_computed_file, original_file as prb_original_file
from tests.custom_assertions import CustomAssertions
from tests.mocks import MockResponse
from tests.test_experiment import experiment_search_result_1, experiment_search_result_2

sample_1 = {
    "id": 1159147,
    "title": "vESRD_CV22",
    "accession_code": "SRR5445147",
    "source_database": "SRA",
    "organism": {"name": "HOMO_SAPIENS", "taxonomy_id": 9606},
    "platform_accession_code": "IonTorrentProton",
    "platform_name": "Ion Torrent Proton",
    "pretty_platform": "Ion Torrent Proton (IonTorrentProton)",
    "technology": "RNA-SEQ",
    "manufacturer": "ION_TORRENT",
    "protocol_info": [
        {
            "Reference": "https://www.ebi.ac.uk/ena/data/view/SRP103842",
            "Description": "EDTA-treated whole blood samples from individual study subjects were centrifuged at 1,600 g for 10 min at 4 °C, transferred to a new centrifuge tube and centrifuged again at 16,000 g for 10 min to remove any residual blood cells. Plasma samples were stored at -80 °C until the step of RNA extraction. Six ml Trizol LS was mixed with 2 ml plasma sample for 5 min at room temperature (RT), followed by mixing with 1 ml 1-bromo-3-chloropropane, vortexed and incubated at 4 °C for 10 min, centrifuged at 6,000 g for 30 min for phase separation. The aqueous phase layer (~ 4 ml) was transferred into a new 50 ml centrifuge tube, mixed with 40 ul glycogen and 5 ml isopropanol, incubated at -20°C for 15 min, centrifuged at 6,000 g for 30 min at 4 °C. After removal of the supernatant, the pellet was lysed with the mixture of Lysis Solution (300 ml) and miRNA Homogenate Additive (30ml) from mirVana (Thermo Fisher, AM1650) kit, vortexed and fully resuspended, followed by addition of 350 ml isopropanol. The mixture was transferred onto an RNAqueous micro filter cartridge and centrifuged at 10,000 g for 15 sec, washed with 700 ml Wash Solution 1 and centrifuged at 10,000 g for 10 sec, washed again with 500 ml Wash Solution 2/3 and centrifuged at 10,000 g for 1 min. Eight ml of Elution Solution (preheated to 65°C) was applied to the filter and centrifuged 10 sec at 10,000 g to obtain RNA samples. The final step was repeated again and the RNA samples were mixed, quantified using Qubit RNA HS assay kit and stored at -80 °C until RNA sequencing. (Exploratory cohort) For the plasma transcriptome RNASeq in the exploratory cohort, 10 ng of total plasma RNA samples from individual study subjects was reversed transcribed to cDNA followed by PCR amplification (16 cycles), digestion with FuPa enzyme, ligation (60 minutes) and Ampure cleanup according to the user guide supplied with the Ion AmpliSeq Transcriptome Human Gene Expression Kit (Thermo Fisher Scientific, PN A26325).  Barcoded libraries were quantitated by Ion Library TaqMan™ Quantitation Kit (Thermo Fisher Scientific, PN4468802) and combined to either 7- or 8- plex pools for sequencing. Sequencing template preparation and Proton P1 chip loading were performed on the Ion Chef™ instrument using the Ion Proton™ Hi-Q ™ Chef kit. (Validation cohort) For the plasma transcriptome RNASeq in the validation cohort, 10 ng of total plasma RNA samples from individual study subjects was reversed transcribed to cDNA followed by PCR amplification (16 cycles) using predesigned primers targeting 8 candidate lncRNAs and 6 control mRNAs, digestion with FuPa enzyme, ligation (60 minutes) and Ampure cleanup.  Barcoded libraries were quantitated by Ion Library TaqMan™ Quantitation Kit (Thermo Fisher Scientific, PN4468802) and pooled for sequencing. Sequencing template preparation and Proton P1 chip loading were performed on the Ion Chef™ instrument using the Ion Proton™ Hi-Q ™ Chef kit.",
        }
    ],
    "annotations": [
        {
            "data": {
                "type": ["RNA"],
                "title": ["sample_150"],
                "status": ["Public on Jan 20 2016"],
            },
            "is_ccdl": False,
            "created_at": "2018-12-19T20:15:49.129080Z",
            "last_modified": "2018-12-19T20:15:49.129080Z",
        }
    ],
    "results": [
        {
            "id": 1339591,
            "processor": {
                "id": 302,
                "name": "Salmon Quant",
                "version": "v1.21.2-hotfix",
                "docker_image": "dr_salmon",
                "environment": {
                    "os_pkg": {"python3": "3.5.1-3", "python3-pip": "8.1.1-2ubuntu0.4"},
                    "python": {"Django": "2.1.8", "data-refinery-common": "=v1.21.2-hotfix"},
                    "cmd_line": {
                        "salmon --version": "salmon 0.13.1",
                        "sra-stat --version": "sra-stat : 2.9.1",
                    },
                    "os_distribution": "Ubuntu 16.04.5 LTS",
                },
            },
            "organism_index": {
                "id": 539,
                "assembly_name": "GRCh38",
                "organism_name": "HOMO_SAPIENS",
                "database_name": "EnsemblMain",
                "release_version": "96",
                "index_type": "TRANSCRIPTOME_LONG",
                "salmon_version": "salmon 0.13.1",
                "download_url": "https://s3.amazonaws.com/data-refinery-s3-transcriptome-index-circleci-prod/HOMO_SAPIENS_TRANSCRIPTOME_LONG_1559763336.tar.gz",
                "result_id": 1242756,
                "last_modified": "2019-06-05T19:36:09.993557Z",
            },
        },
        {
            "id": 1339595,
            "processor": {
                "id": 303,
                "name": "Salmontools",
                "version": "v1.21.2-hotfix",
                "docker_image": "dr_salmon",
                "environment": {
                    "os_pkg": {
                        "g++": "4:5.3.1-1ubuntu1",
                        "cmake": "3.5.1-1ubuntu3",
                        "python3": "3.5.1-3",
                        "python3-pip": "8.1.1-2ubuntu0.4",
                    },
                    "python": {"Django": "2.1.8", "data-refinery-common": "=v1.21.2-hotfix"},
                    "cmd_line": {"salmontools --version": "Salmon Tools 0.1.0"},
                    "os_distribution": "Ubuntu 16.04.5 LTS",
                },
            },
            "organism_index": None,
        },
    ],
    "source_archive_url": "",
    "has_raw": True,
    "sex": "",
    "age": None,
    "specimen_part": "",
    "genotype": "",
    "disease": "",
    "disease_stage": "",
    "cell_line": "",
    "treatment": "",
    "race": "",
    "subject": "human plasma",
    "compound": "",
    "time": "",
    "is_processed": True,
    "created_at": "2019-07-13T14:05:37.129910Z",
    "last_modified": "2019-07-14T16:29:34.433025Z",
    "original_files": [1715994],
    "computed_files": [2425581, 2427322, 2427387],
    "experiment_accession_codes": ["SRP103842"],
}

sample_2 = {
    "id": 840023,
    "title": "sample_150",
    "accession_code": "GSM1562009",
    "source_database": "GEO",
    "organism": {"name": "HOMO_SAPIENS", "taxonomy_id": 9606},
    "platform_accession_code": "hgu133a2",
    "platform_name": "[HG-U133A_2] Affymetrix Human Genome U133A 2.0 Array",
    "pretty_platform": "Affymetrix Human Genome U133A 2.0 Array (hgu133a2)",
    "technology": "MICROARRAY",
    "manufacturer": "AFFYMETRIX",
    "protocol_info": {
        "Reference": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM1562009",
        "Scan protocol": ["Affymetrix GeneChip Scanner"],
        "Label protocol": [
            "Total RNA is converted into double stranded cDNA via reverse transcription (RT) using an oligo-d(T) primer-adaptor. During this RT step, four peptide nucleic acid (PNA) oligomers that bind portions of the alpha and beta hemoglobin transcripts are added to prevent transcription of globin mRNAs.  The cDNA is then converted to dsDNA using T4 DNA polymerase.  The resulting dsDNA is purified to remove unincorporated nucleotides, salts, enzymes and inorganic phosphates.  This is used as a template for in vitro transcription using T7 RNA polymerase and biotinylated ribonucleotides. The resulting cRNA is purified and quantitated using spectrophotometry.  Globin reduction in the cRNA is verified using an Agilent Bioanalyzer."
        ],
        "Data processing": ["Expression Console"],
        "Extraction protocol": [
            "RNA isolation was performed from blood collected in PAXgene Blood RNA Tubes using the PAXgene 96 Blood RNA Kit (QIAgen).  Briefly, blood was pelleted, washed, resuspended, and incubated in optimized buffers with Proteinase K.  The lysate was applied to a filter plate and centrifuged to remove any residual cell debris.  Ethanol was added to the flow-through to provide appropriate binding conditions for the RNA.  The lysate was then applied to an RNA plate where the RNA selectively binds to membrane.  Residual DNA was removed through a DNase digestion on the membrane and any remaining contaminants were washed away.  High-quality RNA was then eluted in nuclease-free water."
        ],
        "Hybridization protocol": [
            "Next, 11ug of purified cRNA is fragmented using a 5X fragmentation buffer, then a hybridization cocktail is prepared and added to the fragmentation product using the Hybridization, Wash and Stain kit (Affymetrix), applied to arrays, and incubated at 45C for 16 hours."
        ],
    },
    "annotations": [
        {
            "data": {
                "type": ["RNA"],
                "title": ["sample_150"],
                "status": ["Public on Jan 20 2016"],
                "label_ch1": ["biotin"],
            },
            "is_ccdl": False,
            "created_at": "2018-12-19T20:15:49.129080Z",
            "last_modified": "2018-12-19T20:15:49.129080Z",
        }
    ],
    "results": [
        {
            "id": 1339595,
            "processor": {
                "id": 303,
                "name": "Salmontools",
                "version": "v1.21.2-hotfix",
                "docker_image": "dr_salmon",
                "environment": {
                    "os_pkg": {
                        "g++": "4:5.3.1-1ubuntu1",
                        "cmake": "3.5.1-1ubuntu3",
                        "python3": "3.5.1-3",
                        "python3-pip": "8.1.1-2ubuntu0.4",
                    },
                    "python": {"Django": "2.1.8", "data-refinery-common": "=v1.21.2-hotfix"},
                    "cmd_line": {"salmontools --version": "Salmon Tools 0.1.0"},
                    "os_distribution": "Ubuntu 16.04.5 LTS",
                },
            },
            "organism_index": None,
        }
    ],
    "source_archive_url": "",
    "has_raw": True,
    "sex": "",
    "age": None,
    "specimen_part": "",
    "genotype": "",
    "disease": "",
    "disease_stage": "",
    "cell_line": "",
    "treatment": "",
    "race": "",
    "subject": "",
    "compound": "",
    "time": "",
    "is_processed": True,
    "created_at": "2018-12-19T20:15:46.399775Z",
    "last_modified": "2019-08-09T20:44:29.963746Z",
    "original_files": [1920272, 1208147],
    "computed_files": [2679162],
    "experiment_accession_codes": ["GSE63990"],
}

sample_1_object_dict = deepcopy(sample_1)

sample_1_object_dict["original_files"] = [
    prb_original_file.OriginalFile(file_id) for file_id in sample_1["original_files"]
]
sample_1_object_dict["computed_files"] = [
    prb_computed_file.ComputedFile(file_id) for file_id in sample_1["computed_files"]
]

sample_2_object_dict = deepcopy(sample_2)

sample_2_object_dict["original_files"] = [
    prb_original_file.OriginalFile(file_id) for file_id in sample_2["original_files"]
]
sample_2_object_dict["computed_files"] = [
    prb_computed_file.ComputedFile(file_id) for file_id in sample_2["computed_files"]
]

result = {
    "id": 1339595,
    "commands": [
        "salmontools extract-unmapped -u /home/user/data_store/processor_job_2893940/SRR5445147_output/aux_info/unmapped_names.txt -o /home/user/data_store/processor_job_2893940/salmontools/unmapped_by_salmon -r /home/user/data_store/processor_job_2893940/SRR5445147"
    ],
    "processor": {
        "id": 303,
        "name": "Salmontools",
        "version": "v1.21.2-hotfix",
        "docker_image": "dr_salmon",
        "environment": {
            "os_pkg": {
                "g++": "4:5.3.1-1ubuntu1",
                "cmake": "3.5.1-1ubuntu3",
                "python3": "3.5.1-3",
                "python3-pip": "8.1.1-2ubuntu0.4",
            },
            "python": {"Django": "2.1.8", "data-refinery-common": "=v1.21.2-hotfix"},
            "cmd_line": {"salmontools --version": "Salmon Tools 0.1.0"},
            "os_distribution": "Ubuntu 16.04.5 LTS",
        },
    },
    "is_ccdl": True,
    "annotations": [],
    "files": [
        {
            "id": 2425581,
            "filename": "salmontools-result.tar.gz",
            "size_in_bytes": 190,
            "is_smashable": False,
            "is_qc": True,
            "sha1": "9d3396dffe4617f6d2d8414ebb2a9f132a0f3c24",
            "s3_bucket": "data-refinery-s3-circleci-prod",
            "s3_key": "ysccy3qawpt2awi1hm4alaz6_salmontools-result.tar.gz",
            "created_at": "2019-07-14T14:49:50.224352Z",
            "last_modified": "2019-07-14T14:49:50.493387Z",
        }
    ],
    "organism_index": None,
    "time_start": "2019-07-14T14:49:47.567197Z",
    "time_end": "2019-07-14T14:49:49.418108Z",
    "created_at": "2019-07-14T14:49:50.210938Z",
    "last_modified": "2019-07-14T14:49:50.210938Z",
}

search_1 = {"count": 2, "next": "search_2", "previous": None, "results": [sample_1]}

search_2 = {"count": 2, "next": None, "previous": "search_1", "results": [sample_2]}

e_search_1 = {
    "count": 2,
    "next": "e_search_2",
    "previous": None,
    "results": [experiment_search_result_1],
}

e_search_2 = {
    "count": 2,
    "next": None,
    "previous": "e_search_1",
    "results": [experiment_search_result_2],
}


def mock_request(method, url, **kwargs):

    if url == "https://api.refine.bio/v1/samples/SRR5445147/":
        return MockResponse(sample_1, url)

    if url == "https://api.refine.bio/v1/samples/GSM1562009/":
        return MockResponse(sample_2, url)

    # this request needs to exist because the result's organism index is None for both test samples
    # so a request will be made to make sure that that value should actually be None
    if url == "https://api.refine.bio/v1/computational_results/1339595/":
        return MockResponse(result, url)

    if url == "https://api.refine.bio/v1/samples/0/":
        return MockResponse(None, url, status=404)

    if url == "https://api.refine.bio/v1/samples/500/":
        return MockResponse(None, url, status=500)

    if url == "https://api.refine.bio/v1/samples/":
        return MockResponse(search_1, "search_2")

    if url == "search_2":
        return MockResponse(search_2, url)

    if url == "https://api.refine.bio/v1/search/":
        return MockResponse(e_search_1, "e_search_2")

    if url == "e_search_2":
        return MockResponse(e_search_2, url)


class SampleTests(unittest.TestCase, CustomAssertions):
    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_sample_get(self, mock_request):
        result = pyrefinebio.Sample.get("SRR5445147")
        self.assertObject(result, sample_1_object_dict)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_sample_500(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.Sample.get(500)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_sample_404(self, mock_request):
        with self.assertRaises(Exception):
            pyrefinebio.Sample.get(0)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_sample_result_is_fully_populated(self, mock_request):
        result = pyrefinebio.Sample.get("SRR5445147")
        self.assertIsNotNone(result.results[1].is_ccdl)
        self.assertIsNotNone(result.results[1].commands)

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_sample_search_no_filters(self, mock_request):
        results = pyrefinebio.Sample.search()

        self.assertObject(results[0], sample_1_object_dict)
        self.assertObject(results[1], sample_2_object_dict)

    def test_sample_search_with_filters(self):
        filtered_results = pyrefinebio.Sample.search(
            limit=1, organism=258, has_raw=True, is_processed=False
        )

        self.assertGreater(len(filtered_results), 0)
        for result in filtered_results:
            self.assertEqual(result.organism.name, "MUS")
            self.assertTrue(result.has_raw)
            self.assertFalse(result.is_processed)

    def test_sample_search_with_invalid_filters(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilters):
            pyrefinebio.Sample.search(foo="bar")

    def test_sample_search_with_invalid_filter_type(self):
        with self.assertRaises(pyrefinebio.exceptions.InvalidFilterType):
            pyrefinebio.Sample.search(age="foo")

    def test_sample_search_with_multiple_invalid_filter_types(self):
        with self.assertRaises(pyrefinebio.exceptions.MultipleErrors):
            pyrefinebio.Sample.search(age="foo", organism="bar")

    @patch("pyrefinebio.api_interface.requests.request", side_effect=mock_request)
    def test_sample_get_experiments(self, mock_request):
        result = pyrefinebio.Sample.get("SRR5445147")
        experiments = list(result.experiments)

        self.assertObject(experiments[0], experiment_search_result_1)
        self.assertObject(experiments[1], experiment_search_result_2)
