#title           :GBcrawler.py
import re
import collections

"""GBcrawler GenBank reader and parser"""

class GBfeature:
	
	def __init__(self, begin, end, type):

		self.begin = begin
		self.end = end
		self.type = type
		self.complementary=False
		self.beginIsBeyond=False
		self.endIsBeyond=False
		self.betweenBases=False
		self.qualifierDict={}
		self.pseudo=False

	def __repr__(self):
		return ("Type: "+self.type + "; Start: "+self.begin+"; End: " +self.end)


class GBreference:
	def __init__(self, refString):
	
		#referenceID=0
		self.authors=""
		self.consortium=""
		self.title=""
		self.journal="" #mandatory journal name, volume, year and page numbers
		#medline="" obsolete
		self.pubmed=""
		self.remark=""
		lines=refString.split('\n')
		self.reference=lines[0]
		searchState=""
		for line in lines:
			print(line)
			if line.startswith("  AUTHORS"):
				searchState="AUTHORS"
				self.authors+=line[12:]
			elif line.startswith("  CONSRTM"):
				searchState="CONSRTM"
				self.consortium+=line[12:]
			elif line.startswith("  TITLE"):
				searchState="TITLE"
				self.title+=line[12:]
			elif line.startswith("  JOURNAL"):
				searchState="JOURNAL"
				self.journal+=line[12:]
			elif line.startswith("  PUBMED"):
				searchState="PUBMED"
				self.pubmed+=line[12:]
			elif line.startswith("  REMARK"):
				searchState="REMARK"
				self.remark+=line[12:]
			elif line.startswith("  MEDLINE"):
				searchState="MEDLINE"
				print("MEDLINE was removed")
			elif line.startswith("            "):
				if searchState=="AUTHORS":
					self.authors+=line[12:]
				elif searchState=="CONSRTM":
					self.consortium+=line[12:]
				elif searchState=="TITLE":
					self.title+=line[12:]
				elif searchState=="JOURNAL":
					self.journal+=line[12:]
				elif searchState=="PUBMED":
					self.pubmed+=line[12:]
				elif searchState=="REMARK":
					self.remark+=line[12:]
				else:
					continue
		#TODO posprocessing each reference string to a list, dict or somethign
		#p.e. separate authors,journals, etc

	def __repr__(self):
		return ("Type: ")

class GBcrawler:

	def __init__(self, filename):
		self.sequenceID=""
		self.sequenceLength=0
		self.strand=""
		self.moleculeType=""
		self.division=""
		self.modDate=""
		self.definition=""
		self.accession=""
		self.version=""
		self.keywords=[]
		self.comment=""
		self.referenceList=[]
		self.featureList=[]  #stores feature objects
		#self.baseCount = {'a': 0, 'c': 0, 'g': 0, 't': 0, 'n':0}
		self.baseCount = collections.Counter()
		self.sequenceList=[]
		self.filename = filename
		
		
		#input = open(filename, 'r')
		

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
			"assembly_gap","centromere","gap","J_segment","mobile_element","ncRNA",
			"operon","oriT","propeptide","regulatory","telomere","tmRNA","V_segment"
		]
		divisionTypes=["PRI","ROD","MAM","VRT","INV","PLN","BCT","VRL","PHG","SYN",
			"UNA","EST","PAT","STS","GSS","HTG","HTC","ENV","CON","TSA","   "]
		
		monoQualifiers = ['environmental_sample','focus','germline','macronuclear',
		'partial','proviral','pseudo','rearranged','ribosomal_slippage',
		'transgenic','trans_splicing']
		
		searchState="LOCUS" #initial state
		tempFeature=None
		tempQualifierKey=""
		tempQualifierValue=None
		tempReference=""
		lineCounter = 0
		
		with open(filename, 'r') as f:
			for line in f:
				
				lineCounter+=1
				#1. check the line and change searchState if needed
				# the most common situation is having a line starting with whitespaces
				# in that case it should skip the checks and depend only on the seachState
				if line.startswith(" "):
					pass
				elif line.startswith("LOCUS"):
					pass
				elif line.startswith("DEFINITION"):
					searchState="DEFINITION"
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
						#self.referenceList.append(tempReference)
						self.referenceList.append(GBreference(tempReference))
						tempReference=""
					tempReference+=line[12:]
					continue
				elif line.startswith("COMMENT"):
					self.referenceList.append(GBreference(tempReference))
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
					
				#print(searchState)
			# 2nd according to the search state, decide action
			# order matters, most used search state should be first,features then sequence
				if searchState == "FEATURES":
					#print(line)
					if not line.startswith("                     "): #22
						if tempFeature is not None:
							tempFeature.qualifierDict[tempQualifierKey]=tempQualifierValue
							self.featureList.append(tempFeature) #store previous
							#print (tempQualifierKey)
							#print (tempQualifierValue)
						featType=re.findall(r"(\S+)\s+" , line)
						if featType[0] not in keyNames:
							print (featType[0]+" is not a valid type. Check line "+ str(lineCounter))
						positions=re.findall("([0-9]+)" , line)
						tempFeature=GBfeature(positions[0],positions[1], featType[0])
						if "complement" in line:
							tempFeature.complementary=True

					elif line.startswith("                     /"): 
						#tempQualifierValue=""
						#simplify with default dict value
						if tempQualifierKey is not None:
							tempFeature.qualifierDict[tempQualifierKey]=tempQualifierValue
						qualifierType=re.findall("/(.+)" , line)
						if qualifierType[0] in monoQualifiers:
							print(qualifierType[0]) #TODO
							# again simply with default dict value = true
							tempQualifierKey=qualifierType[0]
							tempQualifierValue=True
						#elif line.startswith("                     /"):
						else:
							qualifierType=re.findall(r"/(\S+)=(.+)" , line)
							#qualifierType=re.findall("/(\S+)=(\S+)" , line)
							tempQualifierKey=qualifierType[0][0]
							tempQualifierValue=qualifierType[0][1]
					
					else: #manage multiline values
						qt=re.findall(r"(\S+)" , line)
						tempQualifierValue += qt[0]
						
						
				elif searchState == "ORIGIN":
					for i in line:
						if i.isalpha():
							self.sequenceList.append(i.upper())	
						"""
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
						"""
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
				elif searchState == "DEFINITION":
					if line.startswith("            "):
						self.definition+=" "+line.lstrip()
				elif searchState == "LOCUS":
					print("elif")
					print(searchState)
					print(line)
					self.sequenceID = line[12:28].strip()
					self.sequenceLength = line[29:40].strip()
					self.strand = line[44:47].strip()
					self.moleculeType = line[47:53].strip()
					self.division = line[64:67]
					if self.division not in divisionTypes:
						print ("Division type: "+self.division+" is not valid. Valid divisions are: ")
						#print (*divisionTypes, sep='\t')
						print ("Exit program")
						exit()
					self.modDate=line[68:79].strip()
				else:
					continue
		#input.close()
		
		# update the baseCount
		self.baseCount.update(''.join(self.sequenceList))
		
		#self.baseCount.update(self.sequenceList)
	def __str__(self):
		return ("Genbank file for " + self.sequenceID)
		
	def getSequence(self):
		return (''.join(self.sequenceList))
		
	def saveAsFasta(self, filename):
		outFile = open(filename, 'w')
		outFile.write('>')
		outFile.write('\n')
		nCounter=0
		
		for n in self.sequenceList:
			outFile.write(str(n))
			nCounter+=1
			if nCounter==70:
				outFile.write('\n')
				nCounter=0
			
		#outFile.write()
		outFile.close()
		#70 nucleotides per line

