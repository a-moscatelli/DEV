import csv
import sys
import hashlib

#print(sys.version)	# 3.8.10 (...)

assert sys.version[0]=='3'

class OCSVC:

	def __init__(self):
		self.filename = None
		self.withmd5 = False
		self.hasheaders = False
		self.header = []
		self.body = []
		#return None # mandatory

	def loadcsv(self,filename):
		assert len(self.header)==0
		assert len(self.body)==0
		self.filename = filename
		print(self.filename); 
		with open(self.filename, mode ='r') as file:
			self.csvFile = csv.reader(file)
			suspend_on_empty_line = True
			for lines in self.csvFile:
				if suspend_on_empty_line and len(lines)==0:
					break
				self.body.append(lines)
		self.__check_fieldno_consistency()
		return self

	def __check_fieldno_consistency(self):
		assert len(set([len(line) for line in self.body]))==1, 'lines have different number of fields'

	def hasHeaders(self):
		assert len(self.body)>0, 'no data'
		self.hasheaders = True
		self.header = self.body.pop(0)
		return self
		
	def printlines(self):
		hr = "="*64
		print(hr); print(self.header); print(hr)
		[ print(line) for line in self.body ]
		print(hr);
		return None
	
	def __getmd5(self,fields):
		# private
		sep = '#'
		str2hash = sep.join(fields)
		#print(str2hash)
		# header included
		result = hashlib.md5(str2hash.encode())
		linemd5 = result.hexdigest()
		return linemd5
		
	def withmd5s(self):
		assert not self.withmd5
		body2 = [ line + [ self.__getmd5(line)] for line in self.body ]
		self.body = body2
		self.withmd5 = True
		if self.hasheaders:
			header2 = self.header + [ self.__getmd5(self.header)]
		self.header = header2
		return self

	def withpkcheck(self,header):
		assert self.hasheaders
		#print(self.header)
		try:
			hd = self.header.index(header)
		except ValueError:
			print(header); print(self.header)
			raise Exception("no header is found")
		pkvalues = [ line[hd] for line in self.body ]
		assert len(pkvalues) == len(set(pkvalues)), header + ' is NOT a valid PK'
		print(header,'is a valid PK')
		return self

# main

o1 = OCSVC()
o1.loadcsv("test1.csv").hasHeaders().withmd5s().withpkcheck("header3n").printlines()
o2 = OCSVC()
o2.loadcsv("test2.csv").hasHeaders().withmd5s().withpkcheck("header3n").printlines()

