#title           :GBcrawler.py
import re

"""GBcrawler GenBank reader and parser"""

class GBfeature:
	begin=0
	end=0
	type=""
	complementary=False
	beginIsBeyond=False
	endIsBeyond=False
	betweenBases=False
	qualifierDict={}
	pseudo=False

	def __init__(self, begin, end, type):
		self.begin = begin
		self.end = end
		self.type = type

	def __repr__(self):
		return ("Type: "+self.type + "; Start: "+self.begin+"; End: " +self.end)

''' For future uses
class GBreference:
	referenceID=0
	authors=[]
	consortiums=[]
	title=[]
	journal="" #mandatory journal name, volume, year and page numbers
	 medline="" obsolete
	pubmed=""
	remark=[]
'''

class GBcrawler:
	sequenceID=""
	sequenceLength=0
	strand=""	
	moleculeType=""
	division=""
	modDate=""
	definition=""
	accession=""
	version=""
	keywords=[]
	comment=""
	referenceList=[]
	featureList=[]  #stores feature objects
	sequenceList=[]
	baseCount = {'a': 0, 'c': 0, 'g': 0, 't': 0, 'n':0}
	
	
	def __init__(self, filename):
		self.filename = filename
		input = open(filename, 'r')
		searchState="" 
		tempFeature=None
		tempQualifierKey=""
		tempQualifierValue=None
		tempReference=""
		lineCounter=0
		keyNames=[
			#both sets
			"C_region","CDS","D-loop","D_segment","exon","gene","iDNA",
			"intron","mat_peptide","misc_binding","misc_difference",
			"misc_feature","misc_recomb","misc_RNA","misc_structure",
			"modified_base","mRNA","N_region","old_sequence","polyA_site",
			"precursor_RNA","prim_transcript","primer_bind","protein_bind",
			"repeat_region","rep_origin","rRNA","S_region","sig_peptide",
			"source","stem_loop","STS","transit_peptide","tRNA","unsure",
			"V_region","variation","3'UTR","5'UTR",
			
			#exclusive from NCBI-GenBank Flat File Release 220.0
			"attenuator","CAAT_signal","conflict",
			"enhancer","GC_signal","J_region","LTR",
			"misc_signal","mutation",
			"polyA_signal","primer","promoter",
			"RBS","repeat_unit","satellite","scRNA","snRNA",
			"TATA_signal","terminator","transposon",
			"-","-10_signal","-35_signal","3'clip","5'clip",
			
			#exclusive from insdc.org
			"assembly_gap","centromere","gap","J_segment","mobile_element","ncRNA","operon","oriT",
			"propeptide","regulatory","telomere","tmRNA","V_segment"
		]
		divisionTypes=[
			"PRI","ROD","MAM","VRT","INV","PLN","BCT","VRL","PHG","SYN",
			"UNA","EST","PAT","STS","GSS","HTG","HTC","ENV","CON","TSA","   "
		]
		
		for line in input:
			lineCounter+=1
			#1. check the line and change searchState if needed
		
			if line.startswith("LOCUS"):
			#LOCUS       NC_005835            1894877 bp    DNA     circular     12-SEP-2016
				self.sequenceID=line[12:28].strip()
				self.sequenceLength=line[29:40].strip()
				self.strand=line[44:47].strip()
				self.moleculeType=line[47:53].strip()
				self.division=line[64:67]
				if self.division not in divisionTypes:
					print ("Division type: "+self.division+" is not valid. Valid division are: ")
					print(*divisionTypes, sep='\t')
					print ("Exit program")
					exit()
				self.modDate=line[68:79].strip()
			elif line.startswith("DEFINITION"):
				self.definition=line[12:].strip()
			elif line.startswith("ACCESSION"):
				self.accession=line[12:].strip()
			elif line.startswith("VERSION"):
				self.version=line[12:].strip()			#DBlink ????
			elif line.startswith("KEYWORDS"):	
				searchState="KEYWORDS"
				data3=re.findall("([^,]*)[,|\.|\s+]" , line[12:])
				self.keywords+=data3
				continue
			elif line.startswith("SOURCE"):	
				searchState="SOURCE"
				continue
			elif line.startswith("REFERENCE"):
				searchState="REFERENCE"
				if tempReference:
					self.referenceList.append(tempReference)
					tempReference=""
				tempReference+=line[12:]
				continue
			elif line.startswith("COMMENT"):
				self.referenceList.append(tempReference)
				searchState="COMMENT"
				self.comment+=line[12:]
				continue
			elif line.startswith("FEATURES"):
				searchState="FEATURES"
				continue
			elif line.startswith("BASE COUNT"):
				#OBSOLETE
				searchState="OBSOLETE"
				continue
			elif line.startswith("ORIGIN"):
				searchState="ORIGIN"
				#need to append last feature
				self.featureList.append(tempFeature)
				continue

		# 2nd according to the search state, decide action
		# order matters, most used search state should be first,features then sequence
			if searchState == "FEATURES":
				if not line.startswith("                     "): #22
					if tempFeature is not None:
						self.featureList.append(tempFeature) #store previous
					featType=re.findall("(\S+)\s+" , line)
					if featType[0] not in keyNames:
						print (featType[0]+" is not a valid type. Check line "+ str(lineCounter))
					positions=re.findall("([0-9]+)" , line)
					tempFeature=GBfeature(positions[0],positions[1], featType[0])
					if "complement" in line:
						tempFeature.complementary=True
				elif line.startswith("                     /pseudo"): 
					if tempQualifierKey is not None:
						tempFeature.qualifierDict[tempQualifierKey]=tempQualifierValue
					qualifierType=re.findall("/(\S+)=(\S+)" , line)
					tempQualifierKey="pseudo"
					tempQualifierValue=""
				elif line.startswith("                     /"): 
					if tempQualifierKey is not None:
						tempFeature.qualifierDict[tempQualifierKey]=tempQualifierValue
					qualifierType=re.findall("/(\S+)=(\S+)" , line)
					tempQualifierKey=qualifierType[0][0]
					tempQualifierValue=qualifierType[0][1]
				else: 
					qt=re.findall("(\S+)" , line)
					tempQualifierValue += qt[0]
			elif searchState == "ORIGIN":
				for i in line:
					if i.isalpha():
						self.sequenceList.append(i.upper())	
					
						if i == 'a':
							self.baseCount['a'] += 1
						elif i == 'c':
							self.baseCount['c'] += 1
						elif i == 'g':
							self.baseCount['g'] += 1
						elif i == 't':
							self.baseCount['t'] += 1
						else:
							self.baseCount['n'] += 1
			elif searchState=="REFERENCE":
				if tempReference:
					tempReference+=line
					continue
			elif searchState == "KEYWORDS":
				data3=re.findall("([^,]*)[,|\.]" , line.lstrip())
				#[([^,]*)\.|\s+]
				self.keywords+=data3
			elif searchState == "COMMENT":
				self.comment+=line.lstrip()
			else:
				continue

	def __str__(self):
		return ("Genbank file for "+self.sequenceID)
		
	def getSequence(self):
		return (''.join(self.sequenceList))

