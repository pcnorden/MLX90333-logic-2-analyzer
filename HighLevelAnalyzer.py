# BSD 3-Clause License
#
# Copyright (c) 2021, pcnorden
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

class Hla(HighLevelAnalyzer):

	# Settings:
	#join_frames = ChoicesSetting(['Yes', 'No'], label="Join frames together")
	# Join frames won't be available until Saleae releases more documents on the internals of the python
	# SDK, due to Logic 2 wanting time deltas, but when calculating the objects becoming "saleae.data.timing.GraphTime"
	# when apparently Logic 2 wants "saleae.data.timing.GraphTimeDelta" and poking around on the API documentation,
	# I just don't find I have the time really do dig into it since I already have a full-time job and stuff to do instead
	# of digging around in a companies badly-documented python library.
	# And I am very sorry for being so harsh, Saleae is a awesome company, but the lack of python documentation is quite severe.
	# I really love Logic 2 along with my Logic Pro 16 but it still needs a bit of way to come.
	xyz_mode = ChoicesSetting(['0', '1'], label="XYZ Mode bit")

	result_types = {
		'start':{
			'format':'Start'
		},
		'reportX':{
			'format': 'X: {{data.input_data}}'
		},
		'reportY':{
			'format': 'Y: {{data.input_data}}'
		},
		'reportZ':{
			'format': 'Z: {{data.input_data}}'
		},
		'reportAlpha':{
			'format': 'Alpha: {{data.input_data}}'
		},
		'reportBeta':{
			'format': 'Beta: {{data.input_data}}'
		},
		'reportError':{
			'format': 'Error: {{data.input_data}}'
		},
		'sum':{
			'format': 'SUM: {{data.input_data}}'
		}
	}

	def __init__(self):
		'''
		Initialize HLA.

		Settings can be accessed using the same name used above.
		'''
		self.resetValues()

	def resetValues(self):
		'''
		Resets all the values that are needed for the internal processing

		of the SPI packets from the sensor
		'''
		self.last_value = None # A buffer so we can reconstruct the value from the packets
		self.last_value_start_time = None # Startpoint of the packet that we are capturing
		self.start_packet = [None, None] # Start, End
		self.pack1 = [None, None, None] # Start, End, Value
		self.pack2 = [None, None, None] # Start, End, Value
		self.pack3 = [None, None, None] # Start, End, Value
		self.sumpack = [None, None, None] # Start, End, Value
		self.match_len = 0 # Counter to keep track of where we are

	def decode(self, frame: AnalyzerFrame):
		'''
		Process a frame from the input analyzer, and optionally return a single `AnalyzerFrame` or a list of `AnalyzerFrame`s.

		The type and data values in `frame` will depend on the input analyzer.
		'''
		# Start of stream is indicated for MOSI=0xFF and MISO=0xFF
		if frame.data["miso"] == b'\xff' and frame.data["mosi"] == b'\xff' and self.match_len == 0:
			self.start_packet = [frame.start_time, frame.end_time] # Mark the start packet
			self.match_len += 1 # Increment the counter so we can figure out that we need to capture and parse bytes
		elif self.match_len > 0 and frame.data["mosi"] == b'\xff':
			if self.match_len == 7: # The SPI packet should be 8 bytes long including start and end packets.
				self.sumpack = [frame.start_time, frame.end_time, frame.data["miso"]]
				#TODO: Create the AnazlyerFrames here after the rest is made!
				frames = [] # Small buffer to keep all the created frames into before we commit them
				#if self.join_frames == "Yes":
				#	frames.append(AnalyzerFrame('start', self.start_packet[0], (self.start_packet[1]+self.pack1[0])/2, {}))
				#	frames.append(AnalyzerFrame('reportX', (self.start_packet[1]+self.pack1[0])/2, (self.pack1[1]+self.pack2[0])/2, {'input_data':self.pack1[2]}))
				#	frames.append(AnalyzerFrame('reportY', (self.pack1[1]+self.pack2[0])/2, (self.pack2[1]+self.pack3[0])/2, {'input_data':self.pack2[2]}))
				#	frames.append(AnalyzerFrame('reportZ', (self.pack2[1]+self.pack3[0])/2, (self.pack3[1]+self.sumpack[0])/2, {'input_data':self.pack3[2]}))
				#	frames.append(AnalyzerFrame('sum', (self.pack3[1]+self.sumpack[0])/2, self.sumpack[1], {'input_data':self.sumpack[2]}))
				#else:
				if self.xyz_mode == "1":
					frames.append(AnalyzerFrame('start', self.start_packet[0], self.start_packet[1], {}))
					frames.append(AnalyzerFrame('reportX', self.pack1[0], self.pack1[1], {'input_data':self.pack1[2]}))
					frames.append(AnalyzerFrame('reportY', self.pack2[0], self.pack2[1], {'input_data':self.pack2[2]}))
					frames.append(AnalyzerFrame('reportZ', self.pack3[0], self.pack3[1], {'input_data':self.pack3[2]}))
					frames.append(AnalyzerFrame('sum', self.sumpack[0], self.sumpack[1], {'input_data':self.sumpack[2]}))
				else:
					frames.append(AnalyzerFrame('start', self.start_packet[0], self.start_packet[1], {}))
					frames.append(AnalyzerFrame('reportAlpha', self.pack1[0], self.pack1[1], {'input_data':self.pack1[2]}))
					frames.append(AnalyzerFrame('reportBeta', self.pack2[0], self.pack2[1], {'input_data':self.pack2[2]}))
					frames.append(AnalyzerFrame('reportError', self.pack3[0], self.pack3[1], {'input_data':self.pack3[2]}))
					frames.append(AnalyzerFrame('sum', self.sumpack[0], self.sumpack[1], {'input_data':bin(int.from_bytes(self.sumpack[2], 'little'))}))
				self.resetValues()
				return frames
			elif self.match_len == 1: # Capture first byte of X report
				self.last_value = frame.data["miso"]
				self.last_value_start_time = frame.start_time # Store the start time of the packet value that we want to capture
				self.match_len += 1 # Increase the counter so we know where we are

			elif self.match_len == 2: # Capture second byte of X report
				self.pack1 = [self.last_value_start_time, frame.end_time, int.from_bytes(self.last_value+frame.data["miso"], byteorder='little')]
				self.match_len += 1 # Increase the counter so we know which packet we are capturing
			
			elif self.match_len == 3: # Capture first byte of Y report
				self.last_value = frame.data["miso"]
				self.last_value_start_time = frame.start_time # Store the start time of the packet value that we want to capture
				self.match_len += 1 # Increase the counter so we know where we are

			elif self.match_len == 4: # Capture the second byte of the Y report
				self.pack2 = [self.last_value_start_time, frame.end_time, int.from_bytes(self.last_value+frame.data["miso"], byteorder='little')]
				self.match_len += 1
			
			elif self.match_len == 5: # Capture the first byte of the Z report
				self.last_value = frame.data["miso"]
				self.last_value_start_time = frame.start_time
				self.match_len += 1

			elif self.match_len == 6: # Capture the second byte of the Z report
				self.pack3 = [self.last_value_start_time, frame.end_time, int.from_bytes(self.last_value+frame.data["miso"], byteorder='little')]
				self.match_len += 1
		else:
			self.resetValues()