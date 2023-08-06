# Traffic Monitoring Detection Roadway Sensing key Value data
# ver:0.1.0
# date: 2021/04/21
# parsing Roadway Traffic Monitoring Detect
# hardware:(BM-201 TRS): ISK IWR6843 ES2.0
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: objPoint: ['flow','fn','indexMax','index','x','y','range','doppler','area','ptsNum','cid']
# v0.1.0 : 2021/04/21 release
 

import serial
import time
import struct
import pandas as pd
import numpy as np
from dataclasses import dataclass

@dataclass
class header:
	version = 'v0.1.0'
	frameNumber = 0


class roadwayTmdISK_kv:
	#				{        }        ,      ;
	#magicWord =  [b'\x7B',b'\x7D',b'\x3C',b'\x3E']
	magicWord =  [b'{',b'}',b'J',b'B']
	hdr = header
	
	port = ""
	v21_col_names_rt = ['flow','fn','indexMax','index','x','y','range','doppler','area','ptsNum','cid']
	
	def __init__(self,port):
		self.port = port
		print("(jb)Traffic Monitoring Detection Roadway Sensing lib initial")
		print("(jb)For Hardware: Batman-201(ISK)")
		print("(jb)Hardware: IWR-6843 ES2.0")
		print("(jb)Firmware: TRS_kv")
		print("(jb)UART Baud Rate:921600")

		print("(jb)Data type: kv (DataFrame)")
		print("==============Info=================")
		print("Output Data Type: DataFrame")
		print("Output: ['flow','fn','indexMax','index','x','y','range','doppler','area','ptsNum','cid']")
		print("===================================")
	
	def list2df(self,dck,l21):
		ld21 = pd.DataFrame(l21,columns=self.v21_col_names_rt)
		return (dck,ld21)
	
	def getHeader(self):
		return self.hdr
	
	def trsRead(self,disp):
		
		frameNum = 0
		idx = 0
		lstate = 'idle'
		sbuf = b""
		v21df = ([])
		while True:
			try:
				ch = self.port.read()
			except:
				print("(TRS)---port.read() Exception---")
				return self.list2df(False,v21df)
			#print(str(ch))
			if lstate == 'idle':
				#print(self.magicWord)
				if ch == self.magicWord[0]:
					#if disp:
					#print("*** magicWord:"+ "{:02x}".format(ord(ch)) + ":" + str(idx))
					idx = 0
					sbuf = b""
					lstate = 'iData'
					v21df = ([])
					sbuf = ch
					#if disp:
					#	print("-----------------------")
					#	print("(jb) idle-> idata")
					
				else:
					idx = 0
					sbuf = b""
					v21df = ([])
					return self.list2df(False,v21df)
					
			elif lstate == 'iNext':
				sbuf += ch
				idx += 1
				#print(":".join("{:02x}".format(c) for c in sbuf))  
				if self.magicWord[0] == ch:
					#print(":".join("{:02x}".format(c) for c in sbuf))   
					#print("(jb)iTarget_end state:")
					lstate = 'iData'
				
				elif idx > 44:
					lstate = 'idle'
					sbuf = b""
					print("*********  data over(iNext) *********")
					print("Please close the other process in use")
		
			elif lstate == 'iData':
				sbuf += ch
				#print(":".join("{:02x}".format(c) for c in sbuf))  
				idx += 1
				if  self.magicWord[1] == ch and len(sbuf) > 44: # } 
					#print(":".join("{:02x}".format(c) for c in sbuf))
					if disp:
						print("------rx data(iData)-----")
						print(":".join("{:02x}".format(c) for c in sbuf)) 
						
					try:
						 
						(h,j,b,flow,fn,indexMax,index,x,y,ran,doppler,area,ptsNum,cid,t) = struct.unpack('3cBI9fc',sbuf[0:45])
						
						v21df.append((flow,fn,indexMax,index,x,y,ran,doppler,area,ptsNum,cid))
						self.hdr.frameNumber = fn
						
						compIdx = 0 if (indexMax - 1) < 0 else indexMax - 1
						if index == compIdx:
							lstate = 'idle'
							v21pd = self.list2df(True,v21df) 
							v21df =([]) 
							return v21pd
						else:
							lstate = 'iNext'
							
						sbuf = b""
						idx = 0
						
						if disp:
							print("(jb)iData(1) -> idle state")
			
					except:
						lstate = 'idle'
						
						print("(jb)---iData Exception---:{:}".format())
						if disp:
							print("(jb)---iData Exception---")
					
				elif idx > 45:
					lstate = 'idle'
					sbuf = b""
					print("*********data over(iData)*********")
					if disp:
						print("data over {:d} back to idle state".format(idx))
					
					v21df = ([])
					idx = 0
					
					return self.list2df(False,v21df) 
					
			
