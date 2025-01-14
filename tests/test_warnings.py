import VariantValidator
from VariantValidator import Validator
from VariantFormatter import simpleVariantFormatter
from unittest import TestCase
vfo = VariantValidator.Validator()


class TestWarnings(TestCase):

    @classmethod
    def setup_class(cls):
        cls.vv = Validator()
        cls.vv.testing = True

    def test_t_in_rna_string(self):
        variant = 'NM_007075.3:r.235_236insGCCCACCCACCTGCCAG'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'The IUPAC RNA alphabet dictates that RNA variants must use the character u in place of t' in \
               results['validation_warning_1']['validation_warnings']

    def test_issue_169(self):
        variant = 'NC_000017.10(NM_007294.3):c.4421-63A>G'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'ExonBoundaryError: Position c.4421-63 does not correspond with an exon boundary for transcript NM_007294.3' in \
               results['validation_warning_1']['validation_warnings']

    def test_issue_176(self):
        variant = 'NC_000023.10(NM_004006.2):c.8810A>G'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'NC_000023.10:g.31496350T>C: Variant reference (T) does not agree with reference sequence (C)' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_180a(self):
        variant = 'NC_000017.10:g.41232400_41236235del383'
        results = self.vv.validate(variant, 'hg19', 'all').format_as_dict(test=True)
        print(results)
        assert 'Length implied by coordinates must equal sequence deletion length' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_180b(self):
        variant = 'NC_000017.10(NM_007300.3):c.4186-1642_4358-983del10'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'Length implied by coordinates must equal sequence deletion length' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_180c(self):
        variant = 'NC_000017.10(NM_000088.3):c.589-1del2'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'Length implied by coordinates must equal sequence deletion length' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_195a(self):
        variant = 'NM_000088.3(COL1A1):c.590delG'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'Removing redundant gene symbol COL1A1 from variant description' in \
               results['NM_000088.3:c.590del']['validation_warnings'][0]
        assert 'Removing redundant reference bases from variant description' in \
               results['NM_000088.3:c.590del']['validation_warnings'][1]

    def test_issue_216a(self):
        variant = 'NM_006941.3:c.850_877dup27'
        results = self.vv.validate(variant, 'hg19', 'all').format_as_dict(test=True)
        print(results)
        assert 'Length implied by coordinates must equal sequence duplication length' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_216b(self):
        variant = 'NM_006941.3:c.850_877dup28'
        results = self.vv.validate(variant, 'hg19', 'all').format_as_dict(test=True)
        print(results)
        assert 'Trailing digits are not permitted in HGVS variant descriptions' in \
               results['NM_006941.3:c.850_877dup']['validation_warnings'][0]

    def test_issue_239(self):
        variant = 'NM_006941.3:c.1047dupT'
        results = self.vv.validate(variant, 'hg19', 'all').format_as_dict(test=True)
        print(results)
        assert 'Removing redundant reference bases from variant description' in \
               results['NM_006941.3:c.1047dup']['validation_warnings'][0]

    def test_issue_338(self):
        # Also issue 357
        variant = 'NM_000088.3:C.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'NM_000088.3:C.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'nm_000088.3:c.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'lrg_1t1:c.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'lrg_1T1:c.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'LRG_1T1:c.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'chr17:50198002C>A'
        results = self.vv.validate(variant, 'GRCh38', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'because no reference sequence ID has been provided' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

    def test_issue_359(self):
        variant = 'NM_001371623.1:c.483ins'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'The inserted sequence must be provided for insertions or deletion-insertions' in \
               results['validation_warning_1']['validation_warnings'][0]
        assert 'An insertion must be provided with the two positions between which the insertion has taken place' in \
               results['validation_warning_1']['validation_warnings'][1]

        variant = 'NM_001371623.1:c.483ins(10)'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'The length of the variant is not formatted following the HGVS guidelines. Please rewrite e.g. (10) ' \
               'to N[10]' in \
               results['validation_warning_1']['validation_warnings'][0]
        assert 'An insertion must be provided with the two positions between which the insertion has taken place' in \
               results['validation_warning_1']['validation_warnings'][1]

        variant = 'NM_001371623.1:c.483ins10'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'The length of the variant is not formatted following the HGVS guidelines. Please rewrite e.g. 10 ' \
               'to N[10]' in \
               results['validation_warning_1']['validation_warnings'][0]
        assert 'An insertion must be provided with the two positions between which the insertion has taken place' in \
               results['validation_warning_1']['validation_warnings'][1]

        variant = 'NM_001371623.1:c.483insA[10]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'NM_001371623.1:c.483insA[10] is better written as NM_001371623.1:c.483insAAAAAAAAAA' in \
               results['validation_warning_1']['validation_warnings'][0]
        assert 'An insertion must be provided with the two positions between which the insertion has taken place' in \
               results['validation_warning_1']['validation_warnings'][1]
        assert 'insertion length must be 1' in \
               results['validation_warning_1']['validation_warnings'][2]

        variant = 'NM_001371623.1:c.483delinsA[10]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'NM_001371623.1:c.483delinsA[10] is better written as NM_001371623.1:c.483delinsAAAAAAAAAA' in \
               results['NM_001371623.1:c.483_484insAAAAAAAAA']['validation_warnings'][0]

        variant = 'NM_001371623.1:c.483_484insA[10]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'NM_001371623.1:c.483_484insA[10] is better written as NM_001371623.1:c.483_484insAAAAAAAAAA' in \
               results['NM_001371623.1:c.483_484insAAAAAAAAAA']['validation_warnings'][0]

        variant = 'NM_001371623.1:c.483_484ins[A[10];T]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'NM_001371623.1:c.483_484ins[A[10];T] is better written as NM_001371623.1:c.483_484insAAAAAAAAAAT' in \
               results['NM_001371623.1:c.483_484insAAAAAAAAAAT']['validation_warnings'][0]

        variant = 'NM_001371623.1:c.483_484delins[A[10];T]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'NM_001371623.1:c.483_484delins[A[10];T] is better written as ' \
               'NM_001371623.1:c.483_484delinsAAAAAAAAAAT' in \
               results['NM_001371623.1:c.484delinsAAAAAAAAAT']['validation_warnings'][0]

        variant = 'NM_001371623.1:c.483ins(10_20)'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'The length of the variant is not formatted following the HGVS guidelines. Please rewrite e.g. (10_20) '\
               'to N[(10_20)](where N is an unknown nucleotide and [(10_20)] is an uncertain number of N nucleotides ' \
               'ranging from 10 to 20)' in \
               results['validation_warning_1']['validation_warnings'][0]

        variant = 'NM_001371623.1:c.483ins[(20_10)]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'The length of the variant is not formatted following the HGVS guidelines. Please rewrite (20_10) to ' \
               'N[(10_20)]' in \
               results['validation_warning_1']['validation_warnings'][0]
        assert 'An insertion must be provided with the two positions between which the insertion has taken place' in \
               results['validation_warning_1']['validation_warnings'][1]

        variant = 'NM_001371623.1:c.483ins[(20_20)]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'The length of the variant is not formatted following the HGVS guidelines. Please rewrite ' \
               '(20_20) to N[(20)]' in \
               results['validation_warning_1']['validation_warnings'][0]
        assert 'An insertion must be provided with the two positions between which the insertion has taken place' in \
               results['validation_warning_1']['validation_warnings'][1]

        variant = 'NM_001371623.1:c.483_484ins[(10_20)]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'The variant description is syntactically correct but no further validation is possible because the ' \
               'description contains uncertainty' in \
               results['validation_warning_1']['validation_warnings'][0]

        variant = 'NM_001371623.1:c.483ins[(10_20)]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'An insertion must be provided with the two positions between which the insertion has taken place' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_360(self):
        result = simpleVariantFormatter.format('NC_012920.1:g.100del', 'GRCh37', 'refseq', None, False, True)
        assert "The given reference sequence (NC_012920.1) does not match the DNA type (g). For NC_012920.1, " \
               "please use (m). For g. variants, please use a linear genomic reference sequence" in \
               result["NC_012920.1:g.100del"]["NC_012920.1:g.100del"]["genomic_variant_error"]

        result = simpleVariantFormatter.format('NC_012920.1:g.100del', 'hg19', 'refseq', None, False, True)
        assert "NC_012920.1 is not associated with genome build hg19, instead use genome build GRCh37" in \
               result["NC_012920.1:g.100del"]["NC_012920.1:g.100del"]["genomic_variant_error"]

        result = simpleVariantFormatter.format('NC_012920.1:m.1011C>T', 'GRCh37', 'refseq', None, False, True)
        assert "grch37" in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()
        assert "grch38" in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()
        assert "hg38" in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()
        assert "hg19" not in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()

        result = simpleVariantFormatter.format('NC_012920.1:m.1011C>T', 'GRCh38', 'refseq', None, False, True)
        assert "grch37" in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()
        assert "grch38" in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()
        assert "hg38" in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()
        assert "hg19" not in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()

        result = simpleVariantFormatter.format('NC_012920.1:m.1011C>T', 'hg38', 'refseq', None, False, True)
        assert "grch37" in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()
        assert "grch38" in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()
        assert "hg38" in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()
        assert "hg19" not in result["NC_012920.1:m.1011C>T"]["NC_012920.1:m.1011C>T"]["hgvs_t_and_p"][
            "intergenic"]["primary_assembly_loci"].keys()

    def test_issue_360(self):
        variant = 'NC_012920.1:g.100del'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert "The given reference sequence (NC_012920.1) does not match the DNA type (g). For NC_012920.1, " \
               "please use (m). For g. variants, please use a linear genomic reference sequence" in \
               results['mitochondrial_variant_1']['validation_warnings'][0]

    def test_issue_360a(self):
        variant = 'NC_012920.1:g.100del'
        results = self.vv.validate(variant, 'hg19', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert "NC_012920.1 is not associated with genome build hg19, instead use genome build GRCh37" in \
               results['mitochondrial_variant_1']['validation_warnings'][0]

    def test_issue_360b(self):
        variant = 'NC_001807.4:g.100del'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert "NC_001807.4 is not associated with genome build GRCh37, instead use genome build hg19" in \
               results['mitochondrial_variant_1']['validation_warnings'][0]

    def test_issue_351(self):
        variant = 'M:m.1000_100del'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'This is not a valid HGVS variant description, because no reference sequence ID has been provided, ' \
               'instead use NC_012920.1:m.1000_100del' in \
               results['validation_warning_1']['validation_warnings'][0]
        assert 'The variant positions are valid but we cannot normalize variants spanning the origin of ' \
               'circular reference sequences' in \
               results['validation_warning_1']['validation_warnings'][1]

        variant = 'chr1:g.100000del'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'This is not a valid HGVS variant description, because no reference sequence ID has been provided' in \
               results['intergenic_variant_1']['validation_warnings'][0]

    def test_issue_352(self):
        variant = 'NC_000001.10:o.100_1000del'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'Reference sequence type o. should only be used for circular reference sequences that are ' \
               'not mitochondrial. Instead use m.' in \
               results['validation_warning_1']['validation_warnings'][0]

        variant = 'NC_012920.1:o.100_1000del'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'Reference sequence type o. should only be used for circular reference sequences that are not ' \
               'mitochondrial. Instead use m.' in \
               results['mitochondrial_variant_1']['validation_warnings'][0]

    def test_issue_365(self):
        variant = 'NM_000277.3:c.1315+5_1315+6insGTGTAACAG'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert results['NM_000277.3:c.1315+5_1315+6insGTGTAACAG']['validation_warnings'] == []

    def test_issue_46(self):
        variant = 'NP_001119590.1:p.R175_H178delinsX'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert results['validation_warning_1']['validation_warnings'] == [
            "The amino acid at position 175 of NP_001119590.1 is H not R",
            "The amino acid at position 178 of NP_001119590.1 is V not H"
        ]

        variant = 'NP_001119590.1:p.R175delinsX'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert results['validation_warning_1']['validation_warnings'] == [
            "The amino acid at position 175 of NP_001119590.1 is H not R"
        ]

        variant = 'NP_001119590.1:p.H175_V178delinsX'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert results['validation_warning_1']['validation_warnings'] == [
            "Protein level variant descriptions are not fully supported due to redundancy in the genetic code",
            "NP_001119590.1:p.His175_Val178delinsTer is HGVS compliant and contains a valid reference amino acid "
            "description"
        ]
        assert results['validation_warning_1'][

                   'hgvs_predicted_protein_consequence']["tlr"] == "NP_001119590.1:p.His175_Val178delinsXaa"

        variant = 'NP_001119590.1:p.H175delinsX'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert results['validation_warning_1']['validation_warnings'] == [
            "Protein level variant descriptions are not fully supported due to redundancy in the genetic code",
            "NP_001119590.1:p.His175delinsTer is HGVS compliant and contains a valid reference amino acid description"
        ]
        assert results['validation_warning_1'][
                   'hgvs_predicted_protein_consequence']["tlr"] == "NP_001119590.1:p.His175delinsXaa"

    def test_issue_322b(self):
        results = simpleVariantFormatter.format('NC_000017.10:g.48275363CG>A',
                                                'GRCh37', 'refseq', None, False, True)

        print(results)
        assert 'NC_000017.10:g.48275363CG>A' in results.keys()
        assert "Variant reference (CG) does not agree with reference sequence (CC)" in results[
            'NC_000017.10:g.48275363CG>A']['NC_000017.10:g.48275363CG>A']['genomic_variant_error']

    def test_issue_432(self):
        variant = 'NM_024649.4:c.1779+7A>G'
        results = self.vv.validate(variant, 'GRCh38', 'all').format_as_dict(test=True)

        print(results)
        assert results['validation_warning_1']['validation_warnings'] == [
            "NM_024649.4:c.1779+7A>G auto-mapped to NM_024649.4:c.*4A>G",
            "NM_024649.4:c.*4A>G: Variant reference (A) does not agree with reference sequence (C)"
        ]

    def test_issue_455(self):
        variant = 'NP_000483.3:p.?'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)

        print(results)
        assert results['validation_warning_1']['validation_warnings'] == [
            "Protein level variant descriptions are not fully supported due to redundancy in the genetic code",
            "NP_000483.3:p.? is HGVS compliant and contains a valid reference amino acid description"
        ]


class TestVFGapWarnings(TestCase):

    def test_vf_series_1(self):
        results = simpleVariantFormatter.format('NC_000004.11:g.140811117C>A', 'GRCh37', 'refseq', None, False, True,
                                                testing=True)
        print(results)
        assert 'NC_000004.11:g.140811117C>A' in results.keys()
        assert 'NM_018717.4 contains 3 fewer bases between c.2276_2277, and 12 fewer bases between c.1467_1468 ' \
               'than NC_000004.11' in results['NC_000004.11:g.140811117C>A'][
            'NC_000004.11:g.140811117C>A']['hgvs_t_and_p']['NM_018717.4']['gap_statement']

    def test_vf_series_2(self):
        results = simpleVariantFormatter.format('NC_000008.10:g.24811072C>T',
                                                                 'GRCh37', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NC_000008.10:g.24811072C>T' in results.keys()
        assert 'NM_006158.3 contains 1 fewer bases between c.1407_1408 than NC_000008.10' in results[
            'NC_000008.10:g.24811072C>T']['NC_000008.10:g.24811072C>T']['hgvs_t_and_p'][
            'NM_006158.3']['gap_statement']
        assert 'NM_006158.4 contains 1 fewer bases between c.1407_1408 than NC_000008.10' in results[
            'NC_000008.10:g.24811072C>T']['NC_000008.10:g.24811072C>T']['hgvs_t_and_p'][
            'NM_006158.4']['gap_statement']
        assert 'NM_006158.5 contains 1 fewer bases between c.1413_1414 than NC_000008.10' in results[
            'NC_000008.10:g.24811072C>T']['NC_000008.10:g.24811072C>T']['hgvs_t_and_p'][
            'NM_006158.5']['gap_statement']

    def test_vf_series_3(self):
        results = simpleVariantFormatter.format('NC_000015.9:g.72105933del',
                                                                 'GRCh37', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NC_000015.9:g.72105933del' in results.keys()
        assert 'NM_014249.2 contains 1 fewer bases between c.947_948 than NC_000015.9' in results[
            'NC_000015.9:g.72105933del']['NC_000015.9:g.72105933del']['hgvs_t_and_p'][
            'NM_014249.2']['gap_statement']
        assert 'NM_014249.3 contains 1 fewer bases between c.947_948 than NC_000015.9' in results[
            'NC_000015.9:g.72105933del']['NC_000015.9:g.72105933del']['hgvs_t_and_p'][
            'NM_014249.3']['gap_statement']
        assert 'NM_014249.4 contains 1 fewer bases between c.951_952 than NC_000015.9' in results[
            'NC_000015.9:g.72105933del']['NC_000015.9:g.72105933del']['hgvs_t_and_p'][
            'NM_014249.4']['gap_statement']
        assert 'NM_016346.2 contains 1 fewer bases between c.947_948 than NC_000015.9' in results[
            'NC_000015.9:g.72105933del']['NC_000015.9:g.72105933del']['hgvs_t_and_p'][
            'NM_016346.2']['gap_statement']
        assert 'NM_016346.3 contains 1 fewer bases between c.947_948 than NC_000015.9' in results[
            'NC_000015.9:g.72105933del']['NC_000015.9:g.72105933del']['hgvs_t_and_p'][
            'NM_016346.3']['gap_statement']
        assert 'NM_016346.4 contains 1 fewer bases between c.951_952 than NC_000015.9' in results[
            'NC_000015.9:g.72105933del']['NC_000015.9:g.72105933del']['hgvs_t_and_p'][
            'NM_016346.4']['gap_statement']

    def test_vf_series_4(self):
        results = simpleVariantFormatter.format('NC_000019.9:g.41123095dup',
                                                                 'GRCh37', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NC_000019.9:g.41123095dup' in results.keys()
        assert 'NM_001042544.1 contains 1 extra bases between c.3233_3235 than NC_000019.9' in results[
            'NC_000019.9:g.41123095dup']['NC_000019.9:g.41123095dup']['hgvs_t_and_p'][
            'NM_001042544.1']['gap_statement']
        assert 'NM_001042545.1 contains 1 extra bases between c.3032_3034 than NC_000019.9' in results[
            'NC_000019.9:g.41123095dup']['NC_000019.9:g.41123095dup']['hgvs_t_and_p'][
            'NM_001042545.1']['gap_statement']
        assert 'NM_001042545.2 contains 1 extra bases between c.3034_3036 than NC_000019.9' in results[
            'NC_000019.9:g.41123095dup']['NC_000019.9:g.41123095dup']['hgvs_t_and_p'][
            'NM_001042545.2']['gap_statement']
        assert 'NM_003573.2 contains 1 extra bases between c.3122_3124 than NC_000019.9' in results[
            'NC_000019.9:g.41123095dup']['NC_000019.9:g.41123095dup']['hgvs_t_and_p'][
            'NM_003573.2']['gap_statement']

    def test_vf_series_5(self):
        results = simpleVariantFormatter.format('NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=',
                                                                 'GRCh37', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=' in results.keys()
        assert 'NM_001083585.1 contains 25 fewer bases between c.*344_*345 than NC_000017.10' in results[
            'NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['hgvs_t_and_p'][
            'NM_001083585.1']['gap_statement']
        assert 'NM_001083585.2 contains 25 fewer bases between c.*344_*345 than NC_000017.10' in results[
            'NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['hgvs_t_and_p'][
            'NM_001083585.2']['gap_statement']
        assert 'NM_001083585.3 contains 25 fewer bases between c.*369_*370 than NC_000017.10' in results[
            'NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['hgvs_t_and_p'][
            'NM_001083585.3']['gap_statement']
        assert 'NM_001291581.1 contains 25 fewer bases between c.*344_*345 than NC_000017.10' in results[
            'NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['hgvs_t_and_p'][
            'NM_001291581.1']['gap_statement']
        assert 'NM_001291581.2 contains 25 fewer bases between c.*369_*370 than NC_000017.10' in results[
            'NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['hgvs_t_and_p'][
            'NM_001291581.2']['gap_statement']
        assert 'NM_004703.4 contains 25 fewer bases between c.*344_*345 than NC_000017.10' in results[
            'NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['hgvs_t_and_p'][
            'NM_004703.4']['gap_statement']
        assert 'NM_004703.5 contains 25 fewer bases between c.*344_*345 than NC_000017.10' in results[
            'NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['hgvs_t_and_p'][
            'NM_004703.5']['gap_statement']
        assert 'NM_004703.6 contains 25 fewer bases between c.*369_*370 than NC_000017.10' in results[
            'NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG=']['hgvs_t_and_p'][
            'NM_004703.6']['gap_statement']

    def test_vf_series_6(self):
        results = simpleVariantFormatter.format('NC_000012.11:g.122064777C>A',
                                                                 'GRCh37', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NC_000012.11:g.122064777C>A' in results.keys()
        assert 'NM_032790.3 contains 6 fewer bases between c.126_127 than NC_000012.11' in results[
            'NC_000012.11:g.122064777C>A']['NC_000012.11:g.122064777C>A']['hgvs_t_and_p'][
            'NM_032790.3']['gap_statement']

    def test_vf_series_7(self):
        results = simpleVariantFormatter.format('NC_000002.11:g.95847041_95847043GCG=',
                                                                 'GRCh37', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NC_000002.11:g.95847041_95847043GCG=' in results.keys()
        assert 'NM_001017396.1 contains 3 fewer bases between c.341_342 than NC_000002.11' in results[
            'NC_000002.11:g.95847041_95847043GCG=']['NC_000002.11:g.95847041_95847043GCG=']['hgvs_t_and_p'][
            'NM_001017396.1']['gap_statement']
        assert 'NM_001017396.2 contains 3 fewer bases between c.341_342 than NC_000002.11' in results[
            'NC_000002.11:g.95847041_95847043GCG=']['NC_000002.11:g.95847041_95847043GCG=']['hgvs_t_and_p'][
            'NM_001017396.2']['gap_statement']
        assert 'NM_001282398.1 contains 3 fewer bases between c.353_354 than NC_000002.11' in results[
            'NC_000002.11:g.95847041_95847043GCG=']['NC_000002.11:g.95847041_95847043GCG=']['hgvs_t_and_p'][
            'NM_001282398.1']['gap_statement']
        assert 'NM_001291604.1 contains 3 fewer bases between c.227_228 than NC_000002.11' in results[
            'NC_000002.11:g.95847041_95847043GCG=']['NC_000002.11:g.95847041_95847043GCG=']['hgvs_t_and_p'][
            'NM_001291604.1']['gap_statement']
        assert 'NM_001291605.1 contains 3 fewer bases between c.506_507 than NC_000002.11' in results[
            'NC_000002.11:g.95847041_95847043GCG=']['NC_000002.11:g.95847041_95847043GCG=']['hgvs_t_and_p'][
            'NM_001291605.1']['gap_statement']
        assert 'NM_021088.2 contains 3 fewer bases between c.467_468 than NC_000002.11' in results[
            'NC_000002.11:g.95847041_95847043GCG=']['NC_000002.11:g.95847041_95847043GCG=']['hgvs_t_and_p'][
            'NM_021088.2']['gap_statement']
        assert 'NM_021088.3 contains 3 fewer bases between c.467_468 than NC_000002.11' in results[
            'NC_000002.11:g.95847041_95847043GCG=']['NC_000002.11:g.95847041_95847043GCG=']['hgvs_t_and_p'][
            'NM_021088.3']['gap_statement']

    def test_vf_series_8(self):
        results = simpleVariantFormatter.format('NC_000003.11:g.14561629_14561630insG',
                                                'GRCh37', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NM_001080423.2 contains 1 extra bases between c.1308_1310 than NC_000003.11' in results[
            'NC_000003.11:g.14561629_14561630insG']['NC_000003.11:g.14561629_14561630insG']['hgvs_t_and_p'][
            'NM_001080423.2']['gap_statement']
        assert 'NM_001080423.3 contains 1 extra bases between c.1017_1019 than NC_000003.11' in results[
            'NC_000003.11:g.14561629_14561630insG']['NC_000003.11:g.14561629_14561630insG']['hgvs_t_and_p'][
            'NM_001080423.3']['gap_statement']
        assert 'NM_001080423.4 contains 1 extra bases between c.1019_1021 than NC_000003.11' in results[
            'NC_000003.11:g.14561629_14561630insG']['NC_000003.11:g.14561629_14561630insG']['hgvs_t_and_p'][
            'NM_001080423.4']['gap_statement']

    def test_vf_series_9(self):
        results = simpleVariantFormatter.format('NC_000004.11:g.140811117C>A',
                                                'GRCh37', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NC_000004.11:g.140811117C>A' in results.keys()
        assert 'NM_018717.4 contains 3 fewer bases between c.2276_2277, and 12 fewer bases between c.1467_1468 ' \
               'than NC_000004.11' in results[
            'NC_000004.11:g.140811117C>A']['NC_000004.11:g.140811117C>A']['hgvs_t_and_p'][
            'NM_018717.4']['gap_statement']

    def test_vf_series_10(self):
        results = simpleVariantFormatter.format('NC_000009.11:g.136132908_136132909TA=',
                                                'GRCh37', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NC_000009.11:g.136132908_136132909TA=' in results.keys()
        assert 'NM_020469.2 contains 1 extra bases between c.260_262 than NC_000009.11' in results[
            'NC_000009.11:g.136132908_136132909TA=']['NC_000009.11:g.136132908_136132909TA=']['hgvs_t_and_p'][
            'NM_020469.2']['gap_statement']
        assert 'NM_020469.3 contains 22 extra bases between c.*756_*757, and 2 extra bases between c.*797_*798, ' \
               'and 110 extra bases between c.*840_*841, and 2 extra bases between c.*4648_*4649, and 1 extra ' \
               'bases between c.260_262 than NC_000009.11' in results[
            'NC_000009.11:g.136132908_136132909TA=']['NC_000009.11:g.136132908_136132909TA=']['hgvs_t_and_p'][
            'NM_020469.3']['gap_statement']

    def test_vf_series_11(self):
        results = simpleVariantFormatter.format('NC_000019.10:g.50378563_50378564insTAC',
                                                'GRCh38', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NC_000019.10:g.50378563_50378564insTAC' in results.keys()
        assert 'NM_001256647.1 contains 3 extra bases between c.223_227 than NC_000019.10' in results[
            'NC_000019.10:g.50378563_50378564insTAC']['NC_000019.10:g.50378563_50378564insTAC']['hgvs_t_and_p'][
            'NM_001256647.1']['gap_statement']
        assert 'NM_007121.5 contains 3 extra bases between c.514_518 than NC_000019.10' in results[
            'NC_000019.10:g.50378563_50378564insTAC']['NC_000019.10:g.50378563_50378564insTAC']['hgvs_t_and_p'][
            'NM_007121.5']['gap_statement']

    def test_vf_series_12(self):
        results = simpleVariantFormatter.format('NC_000007.13:g.149476664_149476666delinsTC',
                                                'GRCh37', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NC_000007.13:g.149476664_149476666delinsTC' in results.keys()
        assert 'NR_163594.1 contains 1 extra bases between n.1129_1131, and 1 fewer bases between n.11675_11676 ' \
               'than NC_000007.13' in results[
            'NC_000007.13:g.149476664_149476666delinsTC']['NC_000007.13:g.149476664_149476666delinsTC'][
            'hgvs_t_and_p']['NR_163594.1']['gap_statement']

    def test_vf_series_13(self):
        results = simpleVariantFormatter.format('NC_000004.12:g.139889957_139889968del',
                                                'GRCh38', 'refseq', None, False, True, testing=True)
        print(results)
        assert 'NC_000004.12:g.139889957_139889968del' in results.keys()
        assert 'NM_018717.4 contains 3 fewer bases between c.2276_2277, and 12 fewer bases between c.1467_1468 ' \
               'than NC_000004.12' in results[
            'NC_000004.12:g.139889957_139889968del']['NC_000004.12:g.139889957_139889968del']['hgvs_t_and_p'][
            'NM_018717.4']['gap_statement']


class TestVVGapWarnings(TestCase):

    @classmethod
    def setup_class(cls):
        cls.vv = Validator()
        cls.vv.testing = True

    def test_vv_series_1(self):
        variant = 'NC_000004.11:g.140811117C>A'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_018717.4 contains 3 fewer bases between c.2276_2277, and 12 fewer bases between c.1467_1468 than NC_000004.11" in \
               results['NM_018717.4:c.1472_1473insTCAGCAGCAGCA']['validation_warnings']

    def test_vv_series_2(self):
        variant = 'NC_000008.10:g.24811072C>T'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_006158.5 contains 1 fewer bases between c.1413_1414 than NC_000008.10" in \
               results['NM_006158.5:c.1407delinsAC']['validation_warnings']
        assert "NM_006158.4 contains 1 fewer bases between c.1407_1408 than NC_000008.10" in \
               results['NM_006158.4:c.1407delinsAC']['validation_warnings']
        assert "NM_006158.3 contains 1 fewer bases between c.1407_1408 than NC_000008.10" in \
               results['NM_006158.3:c.1407delinsAC']['validation_warnings']

    def test_vv_series_3(self):
        variant = 'NC_000015.9:g.72105933del'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_016346.4 contains 1 fewer bases between c.951_952 than NC_000015.9" in \
               results['NM_016346.4:c.951_952=']['validation_warnings']
        assert "NM_016346.3 contains 1 fewer bases between c.947_948 than NC_000015.9" in \
               results['NM_016346.3:c.947_948=']['validation_warnings']
        assert "NM_016346.2 contains 1 fewer bases between c.947_948 than NC_000015.9" in \
               results['NM_016346.2:c.947_948=']['validation_warnings']
        assert "NM_014249.4 contains 1 fewer bases between c.951_952 than NC_000015.9" in \
               results['NM_014249.4:c.951_952=']['validation_warnings']
        assert "NM_014249.3 contains 1 fewer bases between c.947_948 than NC_000015.9" in \
               results['NM_014249.3:c.947_948=']['validation_warnings']
        assert "NM_014249.2 contains 1 fewer bases between c.947_948 than NC_000015.9" in \
               results['NM_014249.2:c.947_948=']['validation_warnings']

    def test_vv_series_4(self):
        variant = 'NC_000019.9:g.41123095dup'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_003573.2 contains 1 extra bases between c.3122_3124 than NC_000019.9" in \
               results['NM_003573.2:c.3122_3124=']['validation_warnings']
        assert "NM_001042545.2 contains 1 extra bases between c.3034_3036 than NC_000019.9" in \
               results['NM_001042545.2:c.3033_3036=']['validation_warnings']
        assert "NM_001042545.1 contains 1 extra bases between c.3032_3034 than NC_000019.9" in \
               results['NM_001042545.1:c.3032_3034=']['validation_warnings']
        assert "NM_001042544.1 contains 1 extra bases between c.3233_3235 than NC_000019.9" in \
               results['NM_001042544.1:c.3233_3235=']['validation_warnings']

    def test_vv_series_5(self):
        variant = 'NC_000017.10:g.5286863_5286889AGTGTTTGGAATTTTCTGTTCATATAG='
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_004703.6 contains 25 fewer bases between c.*369_*370 than NC_000017.10" in \
               results['NM_004703.6:c.*344_*368dup']['validation_warnings']
        assert "NM_004703.5 contains 25 fewer bases between c.*344_*345 than NC_000017.10" in \
               results['NM_004703.5:c.*344_*368dup']['validation_warnings']
        assert "NM_004703.4 contains 25 fewer bases between c.*344_*345 than NC_000017.10" in \
               results['NM_004703.4:c.*344_*368dup']['validation_warnings']
        assert "NM_001291581.2 contains 25 fewer bases between c.*369_*370 than NC_000017.10" in \
               results['NM_001291581.2:c.*344_*368dup']['validation_warnings']
        assert "NM_001291581.1 contains 25 fewer bases between c.*344_*345 than NC_000017.10" in \
               results['NM_001291581.1:c.*344_*368dup']['validation_warnings']
        assert "NM_001083585.3 contains 25 fewer bases between c.*369_*370 than NC_000017.10" in \
               results['NM_001083585.3:c.*344_*368dup']['validation_warnings']
        assert "NM_001083585.2 contains 25 fewer bases between c.*344_*345 than NC_000017.10" in \
               results['NM_001083585.2:c.*344_*368dup']['validation_warnings']
        assert "NM_001083585.1 contains 25 fewer bases between c.*344_*345 than NC_000017.10" in \
               results['NM_001083585.1:c.*344_*368dup']['validation_warnings']

    def test_vv_series_6(self):
        variant = 'NC_000012.11:g.122064777C>A'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_032790.3 contains 6 fewer bases between c.126_127 than NC_000012.11" in \
               results['NM_032790.3:c.129_130insACACCG']['validation_warnings']

    def test_vv_series_7(self):
        variant = 'NC_000002.11:g.95847041_95847043GCG='
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_021088.3 contains 3 fewer bases between c.467_468 than NC_000002.11" in \
               results['NM_021088.3:c.471_473dup']['validation_warnings']
        assert "NM_021088.2 contains 3 fewer bases between c.467_468 than NC_000002.11" in \
               results['NM_021088.2:c.471_473dup']['validation_warnings']
        assert "NM_001291605.1 contains 3 fewer bases between c.506_507 than NC_000002.11" in \
               results['NM_001291605.1:c.510_512dup']['validation_warnings']
        assert "NM_001291604.1 contains 3 fewer bases between c.227_228 than NC_000002.11" in \
               results['NM_001291604.1:c.231_233dup']['validation_warnings']
        assert "NM_001282398.1 contains 3 fewer bases between c.353_354 than NC_000002.11" in \
               results['NM_001282398.1:c.357_359dup']['validation_warnings']
        assert "NM_001017396.2 contains 3 fewer bases between c.341_342 than NC_000002.11" in \
               results['NM_001017396.2:c.345_347dup']['validation_warnings']
        assert "NM_001017396.1 contains 3 fewer bases between c.341_342 than NC_000002.11" in \
               results['NM_001017396.1:c.345_347dup']['validation_warnings']

    def test_vv_series_8(self):
        variant = 'NC_000003.11:g.14561629_14561630insG'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_001080423.4 contains 1 extra bases between c.1019_1021 than NC_000003.11" in \
               results['NM_001080423.4:c.1019_1021=']['validation_warnings']
        assert "NM_001080423.3 contains 1 extra bases between c.1017_1019 than NC_000003.11" in \
               results['NM_001080423.3:c.1017_1020=']['validation_warnings']
        assert "NM_001080423.2 contains 1 extra bases between c.1308_1310 than NC_000003.11" in \
               results['NM_001080423.2:c.1308_1311=']['validation_warnings']

    def test_vv_series_9(self):
        variant = 'NC_000004.11:g.140811117C>A'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_018717.4 contains 3 fewer bases between c.2276_2277, and 12 fewer bases between c.1467_1468 than NC_000004.11" in \
               results['NM_018717.4:c.1472_1473insTCAGCAGCAGCA']['validation_warnings']

    def test_vv_series_10(self):
        variant = 'NC_000009.11:g.136132908_136132909TA='
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_020469.3 contains 22 extra bases between c.*756_*757, and 2 extra bases between c.*797_*798, and 110 extra bases between c.*840_*841, and 2 extra bases between c.*4648_*4649, and 1 extra bases between c.260_262 than NC_000009.11" in \
               results['NM_020469.3:c.261del']['validation_warnings']
        assert "NM_020469.2 contains 1 extra bases between c.260_262 than NC_000009.11" in \
               results['NM_020469.2:c.261del']['validation_warnings']

    def test_vv_series_11(self):
        variant = 'NC_000019.10:g.50378563_50378564insTAC'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_007121.5 contains 3 extra bases between c.514_518 than NC_000019.10" in \
               results['NM_007121.5:c.515A>T']['validation_warnings']
        assert "NM_001256647.1 contains 3 extra bases between c.223_227 than NC_000019.10" in \
               results['NM_001256647.1:c.224A>T']['validation_warnings']

    def test_vv_series_12(self):
        variant = 'NC_000007.13:g.149476664_149476666delinsTC'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NR_163594.1 contains 1 extra bases between n.1129_1131, and 1 fewer bases between n.11675_11676 than NC_000007.13" in \
               results['NR_163594.1:n.1122_1124delinsT']['validation_warnings']

    def test_vv_series_13(self):
        variant = 'NC_000004.12:g.139889957_139889968del'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "NM_018717.4 contains 3 fewer bases between c.2276_2277, and 12 fewer bases between c.1467_1468 than NC_000004.12" in \
               results['NM_018717.4:c.1466_1468=']['validation_warnings']

    def test_vv_series_14(self):
        variant = 'NM_000516.7:c.2780+73C>T'
        results = self.vv.validate(variant, 'GRCh38', 'all').format_as_dict(test=True)
        print(results)
        assert "CDSError: Variant start position and/or end position are beyond the CDS end position and likely also beyond the end of the selected reference sequence" in \
               results['validation_warning_1']['validation_warnings']

    def test_vv_series_15(self):
        variant = 'NM_000518.5:c.89+25del'
        results = self.vv.validate(variant, 'GRCh38', 'all').format_as_dict(test=True)
        print(results)
        assert "ExonBoundaryError: Position c.89+25 does not correspond with an exon boundary for transcript NM_000518.5" in \
               results['validation_warning_1']['validation_warnings']

    def test_vv_series_16(self):
        variant = 'NM_207122.2:c.1174_1174+1insAT'
        results = self.vv.validate(variant, 'GRCh38', 'all').format_as_dict(test=True)
        print(results)
        assert "ExonBoundaryError: Position c.1174+1 does not correspond with an exon boundary for transcript NM_207122.2" in \
               results['validation_warning_1']['validation_warnings']

    def test_vv_series_17(self):
        variant = 'chr17:g.7578554_7578555delinsCC'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert "This is not a valid HGVS variant description, because no reference sequence ID has been provided" in \
               results['NM_001276761.3:c.259T>G']['validation_warnings']


# <LICENSE>
# Copyright (C) 2016-2023 VariantValidator Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# </LICENSE>
