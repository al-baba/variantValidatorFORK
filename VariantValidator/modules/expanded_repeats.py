"""
NAME:          modules/expanded_repeats.py
AUTHORS:       Rebecca Locke (@rklocke) & Robert Wilson (@RSWilson1)
DATE:          18/02/22
INSTITUTION:   University of Manchester/Cambridge University Hospitals

DESCRIPTION:   This script contains the TandemRepeats class and methods,
               aiming to check the syntax and
               reformat tandem repeat variants for VariantValidator.
"""

# Importing Modules
import re
import logging
import copy
from vvhgvs.assemblymapper import AssemblyMapper

# Set up logger
logger = logging.getLogger(__name__)


class RepeatSyntaxError(Exception):
    """Raised when the syntax of the expanded repeat is incorrect"""
    pass

# Established class for Tandem repeats
class TandemRepeats:
    """
    Class used for create instances of
    expanded repeat variants.
    ----------
    reference : str
        reference sequence name
    prefix : str
        reference sequence type used
    variant_position : str
        nucleotide position(s)
    repeat_sequence : str
        sequence repeat unit
    copy_number : str
        number of repeat units
    after_the_bracket: str
        anything after the last square bracket
    """

    def __init__(
        self,
        reference,
        prefix,
        variant_position,
        repeat_sequence,
        copy_number,
        after_the_bracket,
        build,
        select_transcripts,
        variant_str,
        ref_type,
    ):
        """
        This initialised an instance of the class with set class vars.

        Parameters
        ----------
        variant_str : str
            (Variant string i.e. LRG_199:g.1ACT[20])
        build : str
            Which genome reference the variant_string refers to e.g. GRCh37
        select_transcripts : str
            Return all possible transcripts or only select ones e.g. "all"
        Returns
        -------
        None. But a class instance of variant is created.
        """
        self.reference = reference
        self.intronic_g_reference = False
        self.prefix = prefix
        self.variant_position = variant_position
        self.repeat_sequence = repeat_sequence
        self.copy_number = copy_number
        self.after_the_bracket = after_the_bracket
        self.build = build
        self.select_transcripts = select_transcripts
        self.variant_str = variant_str
        self.cds_start = None # only valid for C type tx
        self.g_strand = 1 # only valid for intronic +/-1
        self.evm = False
        self.no_norm_evm = False
        self.genomic_conversion = None
        self.original_position = None
        self.is_reverse_complement = False

    @classmethod
    def parse_repeat_variant(cls, variant_str, build, select_transcripts, validator):
        """
        Summary
        -------
        Takes a variant string and breaks it into its constituent parts
        with regex to be processed in downstream functions,
        assigns them to class variables.
        Parameters
        ----------
            variant_str : str
                variant string e.g. "LRG_199:g.1ACT[20]A"
        Returns
        -------
            Updates each class attribute:
            reference : str
                Transcript or gene; everything before the first colon, e.g. "LRG_199"
            prefix : str
                The variant genomic or coding type e.g. "g"
            variant_position : str
                Position of the variant, e.g. "1" or "1_12"
            repeat_sequence : str
                The repeated sequence e.g. "ACT"
            copy_number : str
                The number of repeat units e.g. "20"
            after_the_bracket : str
                Captures anything after the number of repeats bracket e.g. "A"

        Example 1:
            >>>parse_repeat_variant("LRG_199:g.1ACT[20]A")
                "LRG_199", "g", "1", "ACT", "20", "A"
        Example 2:
            >>>parse_repeat_variant("NM_024312.4:c.1_10A[10]")
                "NM_024312.4", "c", "1_10" "A", "10", ""
        """
        logger.info(f"Parsing variant: parse_repeat_variant({variant_str})")
        # Strip any whitespace
        variant_str = variant_str.strip()

        # Check if square brackets included which indicate tandem repeat
        # variant

        if '[' in variant_str or ']' in variant_str:
            reference, suffix = variant_str.split(":")

            # Find reference sequence used (g or c)
            var_type = re.search("^.*?(.*?)\\.", suffix)
            prefix = var_type.group(1).lower()
            # Get g or c position(s)
            # Extract bit between . and [ e.g. 1ACT
            pos_and_seq = suffix.split(".")[1].split("[")[0]
            try:
                assert re.search(
                "[gatcu]+$", pos_and_seq, re.IGNORECASE), \
                "Please ensure that the repeated sequence is included between "\
                "the position and number of repeat units, e.g. g.1ACT[20]"
            except AssertionError:
                raise RepeatSyntaxError("RepeatSyntaxError: Ensure that the repeated sequence is included between "\
                "the variant position and the number of repeat units, e.g. g.1_3ACT[20]")
            else:
                rep_seq = re.search("[ACTG]+", pos_and_seq, re.IGNORECASE)
                repeat_sequence = rep_seq.group()
            variant_position = re.sub(r"[A-Za-z]", "", pos_and_seq)

            # Get number of unit repeats
            repeat_no = re.search("\\[(.*?)\\]", variant_str)
            copy_number = repeat_no.group(1)
            # Save anything after bracket so that mixed repeats are supported in future
            if re.search("\\](.*)", variant_str):
                after_brac = re.search("\\](.*)", variant_str)
                after_the_bracket = after_brac.group(1)
            else:
                after_the_bracket = ""

            ref_type = ""
        else:
            logger.info(
                "Unable to identify a tandem repeat. Ending program."
                "Check Format matches HGVS: "
                "(https://varnomen.hgvs.org/recommendations/DNA/variant/repeated/)"
            )
            return False
            #  This returns False to VV to indicate no tandem repeats present.

        if "LRG" in reference:
            ref_type = "LRG"
            if "t" in reference:
                reference = validator.db.get_refseq_transcript_id_from_lrg_transcript_id(reference)
            else:
                reference = validator.db.get_refseq_id_from_lrg_id(reference)

        return cls(
            reference,
            prefix,
            variant_position,
            repeat_sequence,
            copy_number,
            after_the_bracket,
            build,
            select_transcripts,
            variant_str,
            ref_type,
        )

    def reformat_reference(self):
        """Reformats the reference sequence name"""
        logger.info(f"Reformatting reference: reformat_reference({self.reference})")
        if re.match(r"^ENS", self.reference) or re.match(r"^N", self.reference):
            assert (
                "." in self.reference
            ), """Please ensure the transcript or gene version is included
                  following a '.' after the transcript 
                  or gene name e.g. ENST00000357033.8"""
        return self.reference

    def check_genomic_or_coding(self):
        """Takes reference and works out what prefix type should be used
        Raises:
            AssertionError if wrong prefix type is used
        """
        logger.info(
            f"Checking prefix is consistent with reference: "\
            f"check_genomic_or_coding({self.reference},{self.prefix})"
        )
        if re.match(r"^ENST", self.reference):
            assert (
                self.prefix == "c"
            ), """Please ensure variant type is coding 
                if an Ensembl transcript is provided"""
        elif re.match(r"^NM", self.reference):
            assert (
                self.prefix == "c"
            ), """Please ensure variant type is coding 
                  if a RefSeq transcript is provided"""
        elif re.match(r"^NC", self.reference):
            assert (
                self.prefix == "g"
            ), "Please ensure variant type is genomic if RefSeq chromosome is used"
        elif re.match(r"^NG", self.reference):
            assert (
                self.prefix == "g"
            ), "Please ensure variant type is genomic if RefSeq gene is used"
        elif re.match(r"^NR", self.reference):
            assert (
                self.prefix == "n"
            ), "Please ensure variant type is non-coding if NR transcript is used"

    def check_positions_given(self, validator):
        """
        Checks the position range matches the genome reference
        """
        logger.info(
            f"Checking range given: "\
            f"check_positions_given({self.repeat_sequence}, "\
            f"{self.variant_position},{self.copy_number})"
        )
        start,end = self.variant_position.split("_")
        reference_repeat_sequence = validator.sf.fetch_seq(self.reference, int(start)-1, int(end))

        # Check if the length of reference_repeat_sequence is a multiple of the length of query_str
        if len(reference_repeat_sequence) % len(self.repeat_sequence) != 0:
            raise RepeatSyntaxError(f"RepeatSyntaxError: The stated range {self.variant_position} is not a multiple of "
                                    f"the length of the "
                                    f"provided repeat sequence {self.repeat_sequence}")

        # Create a new string by repeating query_str enough times
        repeated_str = self.repeat_sequence * (len(reference_repeat_sequence) // len(self.repeat_sequence))

        if repeated_str != reference_repeat_sequence:
            raise RepeatSyntaxError(f"RepeatSyntaxError: The repeat sequence does not match the reference sequence at "
                                    f"the given position {self.variant_position}, expected {repeated_str} but the "
                                    f"reference is {reference_repeat_sequence} at the specified position")

        return

    def get_range_from_single_pos(self, validator):
        """
        Gets full range of the variant if this is needed
        when a single start position is supplied
        """
        logger.info(
            f"Fetching the range from a given single position: "
            f"get_range_from_single_pos({self.repeat_sequence},"
            f"{self.copy_number},{self.variant_position}"
        )

        # Get the full reference sequence range of the variant
        # the within_ref_pos here is the start position in 0 based coordinates
        try:
            within_ref_pos = int(self.variant_position) - 1
        except ValueError:
            if not self.no_norm_evm:
                # if we normalise at the wrong points we get the wrong ref seq back
                self.no_norm_evm = AssemblyMapper(
                        validator.hdp,
                        assembly_name=self.build,
                        alt_aln_method=validator.alt_aln_method,
                        normalize=False,
                        replace_reference=True
                        )
            if re.search(r"[0-9]+[+-][0-9]+", self.variant_position):
                # Handle a range variant input, given current function's purpose we
                # just dump range and re-build from the first base

                if "_" in self.variant_position:
                    seq_check = validator.hp.parse(f"{self.reference}:{self.prefix}."
                                                   f"{self.variant_position}"
                                                   f"{self.repeat_sequence * int(self.copy_number)}=")

                    self.original_position = copy.copy(self.variant_position)
                    intronic_genomic_variant = self.no_norm_evm.t_to_g(seq_check)
                    self.genomic_conversion = intronic_genomic_variant

                    # Check the exon boundaries
                    self.check_exon_boundaries(validator)
                    seq_check = self.evm.g_to_t(intronic_genomic_variant, self.reference)

                    if seq_check.posedit.edit.ref != self.repeat_sequence * int(self.copy_number):
                        raise RepeatSyntaxError(f"RepeatSyntaxError: The repeat sequence does not match the reference "
                                                f"sequence at the given position {self.variant_position}, "
                                                f"expected {self.repeat_sequence * int(self.copy_number)} but the "
                                                f"reference is "
                                                f"{seq_check.posedit.edit.ref} at the specified position")
                    start, _sep, end =  self.variant_position.partition('_')
                    self.g_strand = validator.hdp.get_tx_exons(self.reference, intronic_genomic_variant.ac,
                                                               validator.alt_aln_method)[0][3]
                    self.original_position = copy.copy(self.variant_position)
                    if  self.g_strand == -1:
                        self.variant_position = end
                    else:
                        self.variant_position = start
                else:
                    # Create a variant for mapping to the genome containing the whole repeat, we used
                    # to use only the first base of the repeat but this breaks on -1 mapping transcripts
                    # with multi-base repeats
                    map_var = f"{self.reference}:{self.prefix}."
                    length = len(self.repeat_sequence)
                    if length == 1:
                        map_var = map_var +f"{self.variant_position}{self.repeat_sequence}="
                    elif '+' in self.variant_position:
                        tx_pos,_sep,intron_offset = self.variant_position.partition('+')
                        intron_offset = int(intron_offset)
                        map_var = map_var +f"{tx_pos}+{intron_offset}_{tx_pos}+{str(intron_offset+length-1)}"+\
                                f"{self.repeat_sequence}="
                    elif '-' in self.variant_position:
                        tx_pos,_sep,intron_offset = self.variant_position.partition('-')
                        intron_offset = int(intron_offset)
                        map_var = map_var +f"{tx_pos}-{intron_offset}_{tx_pos}-{str(intron_offset-length+1)}"+\
                                f"{self.repeat_sequence}="
                    intronic_variant = validator.hp.parse(map_var)
                    intronic_genomic_variant = self.no_norm_evm.t_to_g(intronic_variant)
                    self.g_strand = validator.hdp.get_tx_exons(intronic_variant.ac, intronic_genomic_variant.ac,
                                                               validator.alt_aln_method)[0][3]
                    self.original_position = copy.copy(self.variant_position)
                    self.variant_position = intronic_genomic_variant.posedit.pos.start.base

                self.intronic_g_reference = intronic_genomic_variant.ac
                self.genomic_conversion = intronic_genomic_variant

                # Check exon boundaries
                self.check_exon_boundaries(validator)

                if self.repeat_sequence[0] == intronic_genomic_variant.posedit.edit.ref:
                    within_ref_pos = intronic_genomic_variant.posedit.pos.start.base - 1
                    if self.g_strand == -1:
                        self.reverse_complement(self.repeat_sequence)
                        self.is_reverse_complement = True
                else:
                    within_ref_pos = intronic_genomic_variant.posedit.pos.start.base - 1
                    if self.g_strand == -1:
                        self.reverse_complement(self.repeat_sequence)
                        self.is_reverse_complement = True
            else:
                raise RepeatSyntaxError(
                    f"RepeatSyntaxError: The provided start coordinate {self.variant_position}"
                    "does not appear to be a simple transcript coordinate, or an intronic "
                    "location ")

        if self.prefix == "c" and not self.intronic_g_reference:
            if self.cds_start is None:
                transcript_info = validator.hdp.get_tx_identity_info(self.reference)
                self.cds_start = int(transcript_info[3])
            if  "-" in self.variant_position:
                within_ref_pos = self.cds_start + within_ref_pos + 1
            else:
                within_ref_pos = self.cds_start + within_ref_pos

        self.check_reference_sequence(validator, within_ref_pos)
        ref_start_position, ref_end_position = self.get_reference_range(validator, within_ref_pos)
        ref_start_position = ref_start_position + 1
        full_range = f"{ref_start_position}_{ref_end_position}"

        # Map the full genomic range in the description
        if self.genomic_conversion is not None:
            self.genomic_conversion.posedit.edit.ref = ""
            self.genomic_conversion.posedit.edit.alt = ""
            self.genomic_conversion.posedit.pos.start.base = ref_start_position
            self.genomic_conversion.posedit.pos.end.base = ref_end_position
        return full_range

    def check_reference_sequence(self, validator, within_ref_pos):
        start = within_ref_pos
        end = within_ref_pos + len(self.repeat_sequence)
        ref = self.reference
        if self.intronic_g_reference:
            ref = self.intronic_g_reference
        requested_sequence = validator.sf.fetch_seq(ref, start, end)
        if requested_sequence != self.repeat_sequence:
            raise RepeatSyntaxError(f"RepeatSyntaxError: The provided repeat sequence {self.repeat_sequence } does not "
                                    f"match the reference sequence {requested_sequence} at the given position "
                                    f"{within_ref_pos+1}_{within_ref_pos + len(self.repeat_sequence)} of "
                                    f"reference sequence {ref}")

        else:
            return

    def get_reference_range(self, validator, within_ref_pos):
        """
        Get the full range of the variant
        """
        # get sequence ref
        ref = self.reference
        if self.intronic_g_reference:
            ref = self.intronic_g_reference
        logger.info(
            f"Getting the full range of the variant: "
            f"get_reference_range({ref}, {self.variant_position})"
        )

        # Get the full range of the reference repeat sequence
        start_position = None
        end_position = None
        current_position = None
        while start_position is None:
            if current_position is None:
                current_position = within_ref_pos
            last_position = copy.copy(current_position)
            current_position -= len(self.repeat_sequence)
            requested_sequence = validator.sf.fetch_seq(ref, current_position,
                                                        current_position + len(self.repeat_sequence))
            if requested_sequence != self.repeat_sequence:
                start_position = last_position

        current_position = None
        while end_position is None:
            if current_position is None:
                current_position = within_ref_pos
            last_position = copy.copy(current_position)
            current_position += len(self.repeat_sequence)
            requested_sequence = validator.sf.fetch_seq(ref, current_position,
                                                        current_position + len(self.repeat_sequence))
            if requested_sequence != self.repeat_sequence:
                end_position = last_position + len(self.repeat_sequence)

        return start_position, end_position

    def reformat(self, validator):
        """Reformats and returns final formatted variant as a string"""
        logger.info(
            f"Reformatting variant: reformat({self.repeat_sequence}, "\
            f"{self.after_the_bracket}, "\
            f"{self.prefix}, {self.variant_position}, {self.copy_number})"
        )

        if not self.copy_number.isdecimal():
            raise RepeatSyntaxError("RepeatSyntaxError: The number of repeat units included between square brackets "
                                    "must be numeric")

        # Update the repeated sequence to be upper case
        self.repeat_sequence = self.repeat_sequence.upper()
        # test for non matching chars
        if re.search("[^ACTGU]", self.repeat_sequence):
            raise RepeatSyntaxError(
                "RepeatSyntaxError: Please ensure the repeated sequence"
                "includes only Aa, Cc, Tt, Gg, or Uu")

        if self.after_the_bracket != "":
            raise RepeatSyntaxError(
                f"No information should be included after "
                f"the number of repeat units. "
                f"Currently '{self.after_the_bracket}'' is included. "
            )

        if re.search(r"[+-]", self.variant_position):

            # Create easy variant mapper (over variant mapper) and splign locked evm
            self.evm = AssemblyMapper(validator.hdp,
                                      assembly_name=self.build,
                                      alt_aln_method=validator.alt_aln_method,
                                      normalize=True,
                                      replace_reference=True
                                      )

        # Add coordinates for single position variants
        if "_" not in self.variant_position:
            self.variant_position = self.get_range_from_single_pos(validator)
        elif ("-" in self.variant_position or "+" in self.variant_position) and "_" in self.variant_position:
            if (not re.search(r"\d+\+\d+", self.variant_position) and
                    not re.search(r"\d+-\d+", self.variant_position)):
                self.variant_position = self.variant_position.split("_")[0]
            self.variant_position = self.get_range_from_single_pos(validator)
        else:
            self.variant_position = self.variant_position.split("_")[0]
            self.variant_position = self.get_range_from_single_pos(validator)

        self.check_positions_given(validator)
        self.variant_position = self.convert_n_to_c_coordinates()

        # Map back to transcript if intronic
        if self.genomic_conversion is not None:
            transcript_variant = self.evm.g_to_t(self.genomic_conversion, self.reference)
            self.reference = transcript_variant.ac
            self.variant_position = str(transcript_variant.posedit.pos)
            if self.is_reverse_complement is True:
                self.reverse_complement(self.repeat_sequence)

        final_format = f"{self.reference}:{self.prefix}." \
                       f"{self.variant_position}{self.repeat_sequence}" \
                       f"[{self.copy_number}]"

        return final_format

    def simple_split_string(self):
        """
        Splits the string into two parts divided by the colon (:).
        Useful for segregating the two distict elements of the variant string
        And for troubleshooting.
        Parameters
        ----------
        self.variant_str:str
                (Variant string i.e. LRG_199:g.1ACT[20])

        Returns
        -------
        self.prefix:str
            String for the transcript of the variant. I.e. NM_40091.5
        self.suffix:str
            String for the remaining variant string for further processing.
        """
        self.begining = self.variant_str.split(":")[0]
        self.end = ":" + self.variant_str.split(":")[1]
        return self.begining, self.end

    def convert_n_to_c_coordinates(self):
        """
        Applies CDS based c type offset to a n type variant position
        used for c transcripts only!
        """
        logger.info(
            "Applying c type offset to n type coordinates: " +
            f"convert_n_to_c_coordinates({self.variant_position})"
        )
        if not self.prefix == 'c' or not self.cds_start:
            return self.variant_position
        start, _sep, end = self.variant_position.partition("_")
        start = self._add_offset_to_n(start)
        end = self._add_offset_to_n(end)
        return f"{start}_{end}"

    def _add_offset_to_n(self,coridinate):
        "Add c type offset to a single n type hgvs coordinate"
        # CDS is 0 based, as such for CDS start 0 would be first base pre CDS
        coridinate = int(coridinate) - self.cds_start
        if coridinate <= 0:
            coridinate = coridinate - 1
        return coridinate

    def reverse_complement(self, dna_seq):
        """
        Reverse complement a DNA string using the
        :param dna_seq:
        :return: (str)
        """
        reverse_seq = dna_seq[::-1]
        self.repeat_sequence = "".join([{"G": "C", "T": "A", "A": "T", "C": "G",
                                         "g": "c", "t": "a", "a": "t", "c": "g"}[base]
                                        for base in list(reverse_seq)])
        return

    def check_exon_boundaries(self,validator):
        """
        Check the boundaries of intronic variants are correctly stated
        """
        logger.info(
            f"Checking intronic variant boundaries: check_exon_boundaries({self.variant_position})"
        )
        # Return without error if no boundaries used
        if not '+' in self.original_position and not (
            '-' in self.original_position and # only bother to check with regex if relevant
            re.search('[0-9]-',self.original_position)):
            return

        exon_data = validator.hdp.get_tx_exons(self.reference,
                                               self.genomic_conversion.ac,
                                               validator.alt_aln_method)
        transcript_exon_pos = []
        if  self.prefix == 'c' and self.cds_start is None:
            transcript_info = validator.hdp.get_tx_identity_info(self.reference)
            self.cds_start = int(transcript_info[3])
        elif self.cds_start is None:
            self.cds_start = 0

        for exon in exon_data:
            transcript_exon_pos.append(exon['tx_end_i'])
        start, _sep, end = self.original_position.partition('_')
        def check_exon_pos(exon_pos):
            bad_exon = False
            if exon_pos.startswith('-') and ('+' in exon_pos or '-' in start[1:]):
                pos, _sep, offset = start[1:].partition('-')
                if not self.cds_start - int(pos) -1 in transcript_exon_pos:
                    bad_exon = True
            elif '-' in exon_pos:
                pos, _sep, offset = exon_pos.partition('-')
                if not int(pos) + self.cds_start -1 in transcript_exon_pos:
                    bad_exon = True
            elif '+' in exon_pos:
                pos, _sep, offset = exon_pos.partition('+')
                if pos.startswith('-'):
                    pos = self.cds_start - int(pos)
                else:
                    pos = self.cds_start + int(pos)
                if not pos in transcript_exon_pos:
                    bad_exon = True
            if bad_exon:
                raise RepeatSyntaxError(
                    f"ExonBoundaryError: Position {self.original_position} " +
                    "does not correspond with an exon boundary for transcript "
                    + self.reference)
            return True
        check_exon_pos(start)
        # skip "end" if we don't have a range
        if not end:
            return
        check_exon_pos(end)
        return

def convert_tandem(variant, validator, build, my_all):
    expanded_variant = TandemRepeats.parse_repeat_variant(variant.quibble, build, my_all, validator)

    if expanded_variant is False:
        return False
    else:
        expanded_variant_string = expanded_variant.reformat(validator)
        variant.expanded_repeat = {"variant": expanded_variant_string,
                                   "position": expanded_variant.variant_position,
                                   "copy_number": expanded_variant.copy_number,
                                   "repeat_sequence": expanded_variant.repeat_sequence,
                                   "reference": expanded_variant.reference,
                                   "prefix": expanded_variant.prefix}
        return True


# <LICENSE>
# Copyright (C) 2016-2024 VariantValidator Contributors
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
