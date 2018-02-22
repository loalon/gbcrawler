from GBcrawler import GBcrawler

geneInfo = GBcrawler("1.gb")
print("------LOADING EXAMPLE------")
print ("file name:" + geneInfo.filename + "\n")
print ("sequence: " + geneInfo.sequenceID)
print ("lenght:" + geneInfo.sequenceLength)
print ("molecule: " + geneInfo.strand+geneInfo.moleculeType)
print ("division: "+geneInfo.division)
print ("moification date: "+ geneInfo.modDate)
print("------DEFINITION------")
print (geneInfo.definition)
print("------ACCESSION------")
print (geneInfo.accession)
print("------VERSION------")
print (geneInfo.version)
print("------KEYWORDS------")
print (geneInfo.keywords)
print("------Comment------")
print (geneInfo.comment)
print("------SEQUENCE------")
#print (''.join(geneInfo.sequence))
#print (len(geneInfo.sequenceList))
print (geneInfo.baseCount)
print (geneInfo)
#print (geneInfo.featureList)
contador=0

for i in geneInfo.featureList:
	if i.type == 'gene':
		#print(i.qualifierDict.get('locus_tag'))
		contador+=1
print (len(geneInfo.featureList))
print(contador)

#print (geneInfo.featureList[0].name)
#print (geneInfo.featureList[0].begin)
#print (geneInfo.featureList[0].end)
#print (geneInfo.referenceList)