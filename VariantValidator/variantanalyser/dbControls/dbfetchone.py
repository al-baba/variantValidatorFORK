# -*- coding: utf-8 -*-

"""
dbfetchone.py

Functions which make MySQL fetchone queries
"""

import dbConnection

def execute(query):	
	conn = dbConnection.get_connection().get_connection()
	cursor = conn.cursor(buffered=True)
	cursor.execute(query)

	row = []
	row = cursor.fetchone()

	if row is not None:
		pass
	else:
		# print('No Data...')
		row = ['none', 'No data']
	cursor.close()
	conn.close()
	return row

# Methods
def get_utaSymbol(gene_symbol):
	query = "SELECT utaSymbol FROM transcript_info WHERE hgncSymbol = '%s'" %(gene_symbol)
	row = execute(query)
	return row
	
def get_hgncSymbol(gene_symbol):
	query = "SELECT hgncSymbol FROM transcript_info WHERE utaSymbol = '%s'" %(gene_symbol)
	row = execute(query)
	return row

def get_transcript_description(transcript_id):
	transcript_id = transcript_id
	query = "SELECT description FROM transcript_info WHERE refSeqID = '%s'" %(transcript_id)
	tx_description = str(execute(query)[0])
	return tx_description	

def get_gene_symbol_from_transcriptID(transcript_id):
	transcript_id = transcript_id
	query = "SELECT hgncSymbol FROM transcript_info WHERE refSeqID = '%s'" %(transcript_id)
	gene_symbol = str(execute(query)[0])
	return gene_symbol

def get_refSeqGene_data_by_refSeqGeneID(refSeqGeneID, genomeBuild):
	query = "SELECT refSeqGeneID, refSeqChromosomeID, genomeBuild, startPos, endPos, orientation, totalLength, chrPos, rsgPos, entrezID, hgncSymbol FROM refSeqGene_loci WHERE refSeqGeneID = '%s' AND genomeBuild = '%s'" %(refSeqGeneID, genomeBuild)
	refSeqGene_data = execute(query)
	return refSeqGene_data

def get_gene_symbol_from_refSeqGeneID(refSeqGeneID):
	refseqgene_id = refSeqGeneID
	query = "SELECT hgncSymbol FROM refSeqGene_loci WHERE refSeqGeneID = '%s'" %(refseqgene_id)
	gene_symbol = str(execute(query)[0])
	return gene_symbol	
	
def get_RefSeqGeneID_from_lrgID(lrgID):
	query = "SELECT RefSeqGeneID FROM LRG_RSG_lookup WHERE lrgID = '%s'" %(lrgID)
	rsgID = execute(query)
	rsgID = rsgID[0]
	return rsgID 
	
def get_RefSeqTranscriptID_from_lrgTranscriptID(lrgtxID):
	query = "SELECT RefSeqTranscriptID FROM LRG_transcripts WHERE LRGtranscriptID = '%s'" %(lrgtxID)
	rstID = execute(query)
	rstID = rstID[0]
	return rstID
	
def	get_lrgTranscriptID_from_RefSeqTranscriptID(rstID):		
	query = "SELECT LRGtranscriptID FROM LRG_transcripts WHERE RefSeqTranscriptID = '%s'" %(rstID)
	lrg_tx = execute(query)
	lrg_tx = lrg_tx[0]
	return lrg_tx

def get_lrgID_from_RefSeqGeneID(rsgID):
	query = "SELECT lrgID, status FROM LRG_RSG_lookup WHERE RefSeqGeneID = '%s'" %(rsgID)	
	lrgID = execute(query)
	lrgID = lrgID
	return lrgID
	
def get_refseqgene_info(refseqgene_id, primary_assembly):
	query = "SELECT refSeqGeneID, refSeqChromosomeID, genomeBuild, startPos, endPos FROM refSeqGene_loci WHERE refSeqGeneID = '%s' AND genomeBuild = '%s'" %(refseqgene_id, primary_assembly)	
	refseqgene_info = execute(query)
	return refseqgene_info	
	
def get_RefSeqProteinID_from_lrgProteinID(lrg_p):
	query = "SELECT RefSeqProteinID FROM LRG_proteins WHERE LRGproteinID = '%s'" %(lrg_p)
	rspID = execute(query)
	rspID = rspID[0]
	return rspID

def get_lrgProteinID_from_RefSeqProteinID(rs_p):
	query = "SELECT LRGproteinID FROM LRG_proteins WHERE  RefSeqProteinID = '%s'" %(rs_p)
	lrpID = execute(query)
	lrpID = lrpID[0]
	return lrpID

def get_LRG_data_from_LRGid(lrg_id):
    query = "SELECT * FROM LRG_RSG_lookup WHERE lrgID = '%s'" %(lrg_id)
    lrg_data = execute(query)
    lrg_data = lrg_data
    return lrg_data
	
if __name__ == '__main__':
	query_with_fetchone()
	
# <LICENSE>
# Copyright (C) 2018  Peter Causey-Freeman, University of Leicester
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