#! /usr/bin/env python

# Copyright (c) 2013 Freescale Semiconductor, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# o Redistributions of source code must retain the above copyright notice, this list
#   of conditions and the following disclaimer.
#
# o Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
# o Neither the name of Freescale Semiconductor, Inc. nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import os
import copy
import array
import json
import time
import pexpect

from fsl import filetools
from memoryrange import MemoryRange
import peripherals
import peripheralspeed
import subprocess
import bootsources

# Allow this import to fail, which it will do on OS X.
try:
    from fsl import debugger_utils
except:
    pass

# Constants for command JSON response dictionary keys.
kCmdResponse_Command = "command"
kCmdResponse_Response = "response"
kCmdResponse_Status = "status"
kCmdResponse_Description = "description"
kCmdResponse_Value = "value"

# Errors returned by the Bootloader command methods.
kBlhostError_NoOutput = -3
kBlhostError_ReturnedError = -4

##
# @brief Factory for creating a bootloader object.
#
# @param target
# @param vectorsDir
# @param peripheral
# @param port
# @param loadTarget
def createBootloader(target, vectorsDir, peripheral=peripherals.kPeripheral_Sim, speed=None, port=None, loadTarget=False, resetTarget=True, usePing=True):
    if peripheral == peripherals.kPeripheral_Sim:
        return BootloaderSimulator(target, vectorsDir)
    elif peripheral.split(',')[0] in peripherals.Peripherals:
        return BootloaderDevice(target, vectorsDir, peripheral, speed, port, loadTarget, resetTarget, usePing)
    elif peripheral.split(',')[0] in peripherals.PeripheralsSDP:
        return BootloaderDeviceSDP(target, vectorsDir, peripheral, speed, port, resetTarget)
    else:
        raise ValueError("Unrecognized peripheral '{}'".format(peripheral.split(',')[0]))


##
# @brief Abstract base class to represent a bootloader.
#
# Use the createBootloader() function to create an instance of the appropriate concrete subclass
# for the desired peripheral. You should never create instances of the Bootloader class hierarchy
# directly.
class Bootloader(object):

    def __init__(self, target, vectorsDir):
        self._commandArgs = []

        ## The bootloader.Target object associated with this instance.
        self.target = target

        ## Path to the directory containing test vectors.
        #
        # This path is also used to find the blhost/blsim tool.
        self.vectorsDir = vectorsDir

        ## The full output of the last execution of blhost/blsim as a string.
        self.commandOutput = ""

        ## Status code returned by the blhost/blsim process the last time it was run.
        self.toolStatus = 0

        ## A dictionary of the response from the bootloader for the last command execution.
        self.commandResults = {}

        ## The status of the most recently executed command returned from the bootloader.
        self.commandStatus = 0

        ## String describing the status of the most recently executed command.
        self.commandStatusDescription = ""

        ## The peripheral this instance will use to communicate with the bootloader.
        #
        # This is a string with one of the peripheral names.
        # @sa Peripherals
        self.peripheral = ''

        ## timeout value for waiting return value from blhost/blsim
        self.timeout = 600

        ## The fileLength will use to calculate timeout value of waiting response of blhost
        self.fileLength  = 0

        ## The eraseLength will use to calculate timeout of waiting response of blhost for executing flash-erase-all/region, etc
        self.eraseLength = 0

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return False # Don't suppress exceptions

    def close(self):
        pass

    ##
    # @brief Print the return value and stdout string from the executable (blsim/blhost).
    def printStatus(self):
        if self.commandStatus is None:
            print '\nstatus: None\nresults:\n%s' % (self.commandOutput)
        else:
            print '\nstatus: %d\nresults:\n%s' % (self.commandStatus, self.commandOutput)

    ##
    # @brief Utility function to return the MemoryRange containing the start address.
    def _getRegion(self, start):
        for range in self.target.memoryRange.values():
            if range.start <= start < range.start + range.length:
                return range

    ##
    # @brief Utility function to return the JSON formatted results.
    def _parseResults(self, output):
        if self.toolStatus == 0:
            jsonResults = output[output.find('{'):output.rfind('}')+1]

            if len(jsonResults):
                actualResults = json.loads(jsonResults)
                return actualResults

            # No json was found, create artificial results.
            actualResults = {
                                kCmdResponse_Status : {
                                            kCmdResponse_Value : kBlhostError_NoOutput,
                                            kCmdResponse_Description : 'The command did not return a status.'
                                        },
                                kCmdResponse_Response : None
                            }
        else:
            # Tool returned error code.
            actualResults = {
                    kCmdResponse_Status : {
                                kCmdResponse_Value : kBlhostError_ReturnedError,
                                kCmdResponse_Description : 'The command returned error %d.' % self.toolStatus
                            },
                    kCmdResponse_Response : None
                }


        return actualResults

    ##
    # @brief Verify a memory range.
    #
    # @param start The absolute memory address to start the comparison.
    # @param arg2 Either a bytearray, integer, or file path.The type of @a arg2 determines what
    #   the memory range will be compared against.<br>If @a arg2 is a bytearray, then it contains
    #   the expected bytes. Length of comparison is determined by the length of the bytearray.<br>
    #   If @a arg2 is an integer, the integer is the number of bytes to verify. In this case,
    #   all bytes in the memory range are expected to be a constant value denoted by arg3.<br>
    #   Finally, if @a arg2 is a valid path to a file in the @c vectors directory, then that file
    #   contains the expected bytes. Length of comparison is determined by the size of the binary file.
    # @param arg3 If arg2 is an integer, then this argument is an integer used as the byte value
    #              for each byte in the expected array.
    # @return True if the actual bytes equal the expected bytes; False otherwise.
    # @throws ValueError In case 2nd parameter does not an expected type.
    def verifyMemory(self, start, arg2, arg3=None):

        # If the second argument is an array of expected bytes.
        if type(arg2) == type(bytearray()):
            expectedBytes = arg2
            bootloaderBytes = self._readMemory(start, len(expectedBytes))
            return bootloaderBytes == expectedBytes

        # If the second argument is an integer representing
        # the number of bytes to verify.
        elif type(arg2) == type(0):
            expectedBytes = array.array('c', [chr(arg3)]) * arg2
            bootloaderBytes = self._readMemory(start, len(expectedBytes))
            return bootloaderBytes == expectedBytes.tostring()

        # If the second argument is the name of a file that contains
        # the bytes to verify.
        elif os.path.isfile(os.path.join(self.vectorsDir, arg2)):
            expectedBytes = open(os.path.join(self.vectorsDir, arg2), 'rb').read()
            bootloaderBytes = self._readMemory(start, len(expectedBytes))
            return bootloaderBytes == expectedBytes

        else:
            raise ValueError('Second argument must be a bytearray, a filename, or an integer length.')

    ##
    # @brief Verify a the results of the last command executed.
    #
    # @param expectedResults A list of the command response words not including the status word.
    # @return True if the actual results equal the expected results; False otherwise.
    def verifyResult(self, expectedResults):
        return self.commandResults[kCmdResponse_Response] == expectedResults

    ##
    # @brief Verify a the status of the last command executed.
    #
    # @param expectedStatus A value of expected status of the last command exectued.
    # @return True if the actual status equal the expected status; False otherwise.
    def verifyStatus(self, expectedStatus):
        return self.commandResults[kCmdResponse_Status][kCmdResponse_Value] == expectedStatus

    ##
    # @brief get peripheral and its speed according to command args
    #
    # @param args     command argument list
    def _getPeripheralAndSpeed(self, args):
        peripheral = peripherals.kPeripheral_Sim
        peripheralSpeed = 0

        if '-u' in self._commandArgs:
            peripheral = peripherals.kPeripheral_USB
            peripheralSpeed = peripheralspeed.kUsbDefaultSpeed

        elif '-b' in self._commandArgs:
            peripheralArgIndex = self._commandArgs.index('-b') + 1
            peripheralArgs = self._commandArgs[peripheralArgIndex].split(',')

            if peripheralArgs[0] == peripherals.kPeripheral_SPI:
                peripheral = peripherals.kPeripheral_SPI
                if len(peripheralArgs) > 1:
                    peripheralSpeed = long(peripheralArgs[1])
                else:
                    peripheralSpeed = peripheralspeed.kSpiDefaultSpeed
            elif peripheralArgs[0] == peripherals.kPeripheral_I2C:
                peripheral = peripherals.kPeripheral_I2C
                if len(peripheralArgs) > 1:
                    peripheralSpeed = long(peripheralArgs[2])
                else:
                    peripheralSpeed = peripheralspeed.kI2cDefaultSpeed
            elif peripheralArgs[0] == peripherals.kPeripheral_CAN:
                peripheral = peripherals.kPeripheral_CAN
                if len(peripheralArgs) > 1:
                    # '0' means 125k, '1' means 250k, '2' means 500k, '4' means 1000k
                    power2 = long(peripheralArgs[1])
                    # '4' is an exception
                    if power2 == 4:
                        power2 = power2 - 1
                    peripheralSpeed = (1 << power2) * 125
                else:
                    peripheralSpeed = peripheralspeed.kCanDefaultSpeed
            else:
                raise ValueError('Invalid peripheral parameter: %s' % peripheralArgs[0])

        elif '-p' in self._commandArgs:
            peripheral = peripherals.kPeripheral_UART
            peripheralArgIndex = self._commandArgs.index('-p') + 1
            peripheralArgs = self._commandArgs[peripheralArgIndex].split(',')
            if len(peripheralArgs) > 1:
                    peripheralSpeed = long(peripheralArgs[1])
            else:
                    peripheralSpeed = peripheralspeed.kUartDefaultSpeed

        else: # peripheral is peripherals.kPeripheral_SIM
            pass

        return peripheral, peripheralSpeed

    ##
    # @brief set timeout for waiting results from blhost
    #
    # @param args    command argument list
    def _setTimeoutAutomatically(self, args):
        peripheral, peripheralSpeed = self._getPeripheralAndSpeed(args)
        fileLength = self.fileLength
        # The max file length should be less than max length of all actual memory
        maxLength = self.target.memoryRange['ram'].length;
        if self.target.memoryRange.has_key('flash'):
            maxLength = max(maxLength, self.target.memoryRange['flash'].length)
        if self.target.memoryRange.has_key('spiFlash'):  
            maxLength = max(maxLength, self.target.memoryRange['spiFlash'].length)
        fileLength = min(fileLength, maxLength)
        
        timeout = 10
        compensateSeconds = 20   # this value is used for compensating deviation
        if 'receive-sb-file' in args:
            timeout = 100 # don't know what is in SB file, so give it a long time
        elif fileLength > 0 and peripheral != peripherals.kPeripheral_Sim :
            actualLength  = long(fileLength) * 1.25 #actual length includes file length and other overhead such as framing header
            baseFileLength = 40960
            multiplicationFactors = actualLength / baseFileLength
            if peripheral == peripherals.kPeripheral_UART:
                fixedProcessSeconds = 7
                basePeripheralSpeed = 115200
                if peripheralSpeed != 9600:# this is an exception
                    timeout = (fixedProcessSeconds + 3.5 * basePeripheralSpeed / peripheralSpeed) * multiplicationFactors + compensateSeconds
                else: # below is a workaround
                    timeout = (fixedProcessSeconds + 3.5 * basePeripheralSpeed / peripheralSpeed) * 1.5 * multiplicationFactors + compensateSeconds

            elif peripheral == peripherals.kPeripheral_SPI:
                fixedProcessSeconds = 50
                basePeripheralSpeed = 250
                timeout = (fixedProcessSeconds + 1.6 * basePeripheralSpeed/peripheralSpeed) * multiplicationFactors + compensateSeconds
            elif peripheral == peripherals.kPeripheral_I2C:
                fixedProcessSeconds = 18
                basePeripheralSpeed = 100
                timeout = (fixedProcessSeconds + 6 * basePeripheralSpeed/peripheralSpeed) * multiplicationFactors + compensateSeconds
            elif peripheral == peripherals.kPeripheral_CAN:
                fixedProcessSeconds = 18
                basePeripheralSpeed = 100
                timeout = (fixedProcessSeconds + 6 * basePeripheralSpeed/peripheralSpeed) * multiplicationFactors + compensateSeconds
            elif peripheral == peripherals.kPeripheral_USB:
                fixedProcessSeconds = 9
                timeout = fixedProcessSeconds *  multiplicationFactors + compensateSeconds
        elif self.eraseLength > 0:
            # assume target takes 20ms to erase one block, typical time is less than this value, according to RM, this value is 14ms
            timeout = 0.1 * self.eraseLength / self.target.memoryRange["flash"].flashSectorSize + compensateSeconds
        else:  # for other commands, 10 seconds timeout is enough
            timeout = 10 # default timeout value : 10 seconds
         
        self.fileLength = 0
        self.eraseLength = 0   

        self.timeout = long(timeout)

    ##
    # @brief Generate computed timeout arguments for the host tool.
    #
    # @param args List of bootloader command arguments.
    # @return List of arguments to set the timeout appropriate for the bootloader command.
    def _getTimeoutArgument(self, args):
        self._setTimeoutAutomatically(args)
        argsList = ['-t', str(int(self.timeout * 1000))]
        return argsList

    ##
    # @brief Utility function to run executable (blsim/blhost) for code reuse.
    # @todo Move the '--' marker from the commands to here after steAutobaud gets reworked.
    # @return A bi-tuple of the command status, and the dictionary of command results.
    def _executeCommand(self, *args):
        # Make a copy of the base args so we don't mess up the original.
        theArgs = copy.copy(self._commandArgs)

        # Modify args with command-specific timeout, and append the command params.
        for i, a in enumerate(self._getTimeoutArgument(args)):
            theArgs.insert(1 + i, a)
        theArgs.extend(args)

        # Convert all args to strings.
        theArgs = [str(x) for x in theArgs]
        print "Executing:", " ".join(theArgs)

        # Execute the command.
        process = subprocess.Popen(theArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.commandOutput = process.communicate()[0]
        self.toolStatus = process.returncode

        print 'toolStatus:', self.toolStatus
        print 'commandOutput:', self.commandOutput

        # Convert command JSON output into a dict.
        self.commandResults = self._parseResults(self.commandOutput);

        # Set some attributes based on results dict.
        self.commandStatus = self.commandResults[kCmdResponse_Status][kCmdResponse_Value]
        self.commandStatusDescription = self.commandResults[kCmdResponse_Status][kCmdResponse_Description]

        return self.commandStatus, self.commandResults[kCmdResponse_Response]

    ## @name Bootloader commands
    ## @{

    ##
    # @brief flash-erase-all command
    def flashEraseAll(self):
        self.eraseLength = self.target.memoryRange["flash"].length
        return self._executeCommand('flash-erase-all')

    ##
    # @brief flash-erase-all-unsecure command
    def flashEraseAllUnsecure(self):
        self.eraseLength = self.target.memoryRange["flash"].length
        return self._executeCommand('flash-erase-all-unsecure')

    ##
    # flash-erase-region command
    def flashEraseRegion(self, address, length):
        self.eraseLength = length + 65536 # it is a approximate value but it is enough for calculation
        return self._executeCommand('flash-erase-region', address, length)

    ##
    # @brief read-memory command
    #
    # response = [ bytes-read ]
    #
    # @todo Default filename to a (new?) temp file rather than reusing the same file.
    def readMemory(self, address, length, filename='readMemory.dat'):
        fullFileName = os.path.join(self.vectorsDir, filename)

        self.fileLength = length
        status = self._executeCommand('read-memory', address, length, fullFileName)

        if status == 0:
            return status, open(fullFileName)
        else:
            return status

    ##
    # @brief write-memory command
    #
    # @param address Data will be written to memory beginning at the address parameter.
    # @param filename If filename is a file in the vectors directory, the file will
    #                 The file data will be written to the memory beginning at the
    #                 address parameter. If filename is not a file in the vectors directory,
    #                 the filename parameter will be used as string data to be written to
    #                 the memory beginning at the address parameter.
    # @returns Status of the
    def writeMemory(self, address, filename):
        createdTempFile = False
        fullFileName = os.path.join(self.vectorsDir, filename)

        if not os.path.isfile(fullFileName):
            fullFileName = os.path.join(self.vectorsDir, 'tmp_writeMemoryData')
            tempFile =  open(fullFileName)
            tempFile.write(str(filename))

            createdTempFile = True
        self.fileLength = os.path.getsize(fullFileName)
        status, results = self._executeCommand('write-memory', address, fullFileName)

        if createdTempFile:
            os.remove(fullFileName)

        return status, results

    ##
    # @brief fill-memory command
    #
    # response = [ bytes-read ]
    #
    def fillMemory(self, address, length, pattern, unit='word'):
        self.fileLength = length
        self.eraseLength = 0
        return self._executeCommand('fill-memory', address, length, pattern, unit)
    
    ##
    # @brief configure-quadspi command
    def configureQuadSpi(self, index, address):
        return self._executeCommand('configure-quadspi', index, address)
    

    ##
    # @brief flash-security-disable command
    def flashSecurityDisable(self, key):
        return self._executeCommand('flash-security-disable', key)

    ##
    # @brief get-property command
    def getProperty(self, tag, externalMemoryId=0):
        return self._executeCommand('get-property', tag, externalMemoryId)

    ##
    # @brief receive-sb-file command
    def receiveSbFile(self, filename):
        fullFileName = os.path.join(self.vectorsDir, filename)
        self.fileLength = os.path.getsize(fullFileName)

        return self._executeCommand('receive-sb-file', fullFileName)

    ##
    # @brief execute command
    def execute(self, address, arg, stackpointer):
        return self._executeCommand('execute', address, arg, stackpointer)

    ##
    # @brief call command
    def call(self, address, arg):
        return self._executeCommand('call', address, arg)

    ##
    # @brief reset command
    def reset(self):
        return self._executeCommand('reset')

    ##
    # @brief set-property command
    def setProperty(self, tag, value):
        return self._executeCommand('set-property', tag, value)

    ##
    # @brief flash-program-once command
    def flashProgramOnce(self, index, byte_count, data):
        return self._executeCommand('flash-program-once', index, byte_count, data)
    
    ##
    # @brief flash-read-once command
    def flashReadOnce(self, index, byte_count):
        return self._executeCommand('flash-read-once', index, byte_count)
    
    ##
    # @brief reliable-update command
    def reliableUpdate(self, address):
        return self._executeCommand('reliable-update', address)    

    ## @}

##
# @brief The bootloader simulator.
class BootloaderSimulator(Bootloader):

    def __init__(self, target, vectorsDir):
        super(BootloaderSimulator, self).__init__(target, vectorsDir)

        self._toolName = os.path.abspath(os.path.join(vectorsDir, '..', 'blsim'))
        self._commandArgs.append(self._toolName)
        self._commandArgs.extend(['-s', vectorsDir])

        self.peripheral = peripherals.kPeripheral_Sim

        # Make the tool executable on OS X. It loses the x bit when Bamboo copies it.
        if sys.platform == 'darwin':
            filetools.makeExecutable(self._toolName)

        self._commandArgs.extend(['-j', '--'])

    ##
    # @brief Read memory from simulator file.
    #
    # Figure out the correct simulator file by looking at the start parameter
    # and read the length of bytes from the file.
    #
    # @param start The beginning address of the memory range to read.
    # @param length The number of bytes to read after the start address.
    # @return A byte_array containing the bytes read from the simulator file.
    def _readMemory(self, start, length):

        returnBytes = bytearray()
        memoryRange = self._getRegion(start)

        # Validate 'start' parameter
        if memoryRange == None:
            raise ValueError('Invalid "start" parameter.')

        # Validate 'length' parameter
        if start + length > memoryRange.start + memoryRange.length:
            raise ValueError('Invalid "length" parameter.')

        # Read simulated memory bytes from appropriate file.
        with open(os.path.join(self.vectorsDir, memoryRange.simulatorFilename), 'rb') as fileObj:
            fileObj.seek(start - memoryRange.start)
            returnBytes = fileObj.read(length)

        return returnBytes

    ##
    # @brief Return empty timeout argument list.
    #
    # blsim doesn't support the timeout argument used by blhost, so this method is overridden
    # to return an empty list.
    def _getTimeoutArgument(self, args):
        return []

    ##
    # @brief set-property command
    # @todo Make it so we don't have to reinit state here when using set-property with blsim.
    def setProperty(self, tag, value):
        # Save current args and insert -i to reinit state.
        savedArgs = copy.copy(self._commandArgs)
        #self._commandArgs.insert(1, '-i')

        # Call to superclass' implementation.
        results = super(BootloaderSimulator, self).setProperty(tag, value)

        # Restore previous args.
        self._commandArgs = savedArgs

        return results

##
# @brief The bootloader running on a real device.
class BootloaderDevice(Bootloader):

    def __init__(self, target, vectorsDir, peripheral, speed, port, loadTarget, resetTarget, usePing):
        super(BootloaderDevice, self).__init__(target, vectorsDir)
        self._speed = speed
        self._port = port     
        self._loadTarget = loadTarget
        self._resetTarget = resetTarget
        self._usePing = usePing
        self._toolName = os.path.abspath(os.path.join(vectorsDir, '..', 'blhost'))
        self._commandArgs.append(self._toolName)

        self.peripheral = peripheral
        peripheralDevice = peripheral.split(',')[0]
        
        self._updatePeripheralSpeed()

        if peripheralDevice == peripherals.kPeripheral_USB:
            self._commandArgs.extend(['-u'])
        else:
            if peripheralDevice == peripherals.kPeripheral_UART:
                self._commandArgs.extend(['-p', self._port + ',' + self._speed])
            else:
                self._commandArgs.extend(['-p', self._port + ',' + str(peripheralspeed.kBuspalUartDefaultSpeed)])

        if peripheralDevice == peripherals.kPeripheral_UART:
            pass
        elif peripheralDevice in [peripherals.kPeripheral_SPI, peripherals.kPeripheral_I2C, peripherals.kPeripheral_CAN]:

            if self.peripheral == peripherals.kPeripheral_SPI:
                peripheralParams = self.peripheral + ',' + self._speed
            elif self.peripheral == peripherals.kPeripheral_I2C:
                kDefaultI2cSlaveAddress = '0x10'
                peripheralParams = self.peripheral + ',' + kDefaultI2cSlaveAddress + ',' + self._speed
            elif self.peripheral == peripherals.kPeripheral_CAN:    
                kDefaultCanSlaveRxTxId = '0x321,0x123'
                peripheralParams = self.peripheral + ',' + self._speed + ',' + kDefaultCanSlaveRxTxId

            self._commandArgs.extend(['-b', peripheralParams])
            if not usePing:
                self._commandArgs.extend(['-n'])
            pass
        elif peripheralDevice == peripherals.kPeripheral_USB:
            pass
        else:
            raise ValueError('Invalid peripheral parameter: %s' % peripheralDevice)

        # Make the tool executable on OS X. It loses the x bit when Bamboo copies it.
        if sys.platform == 'darwin':
            filetools.makeExecutable(self._toolName)

        # Load and start the bootloader firmware.
        if self._loadTarget:
            self.target.flashBinary()
            self.target.reset()
            time.sleep(3)

        # Reset the target running the bootloader firmware.
        if self._resetTarget and not self._loadTarget:
            self.target.reset()
           # if self.peripheral == peripherals.kPeripheral_USB:
            time.sleep(3)

        self._commandArgs.extend(['-j', '--'])


    def close(self):
        self.target.close()

    def __exit__(self, type, value, traceback):
        self.close()
        return False # Don't suppress exceptions
    
    def _getConvertedCanSpeedParam(self, useSelfSpeed, speed):
        if useSelfSpeed == True:
            if self._speed == '':
                unconvertedSpeed = peripheralspeed.kCanDefaultSpeed
            else:
                unconvertedSpeed = self._speed    
        else:
            unconvertedSpeed = speed
        
        convertedSpeed = ''
        if type(unconvertedSpeed) == type(''):
            if unconvertedSpeed.find('k'):
                unconvertedSpeed = long(unconvertedSpeed.split('k')[0])
            elif unconvertedSpeed.find('m'):
                unconvertedSpeed = long(unconvertedSpeed.split('m')[0])*1000
            else:
                unconvertedSpeed = long(unconvertedSpeed)
        
        if unconvertedSpeed == 125:
            convertedSpeed = '0'
        elif unconvertedSpeed == 250:
            convertedSpeed = '1'
        elif unconvertedSpeed == 500:
            convertedSpeed = '2'
        elif unconvertedSpeed == 1000:
            convertedSpeed = '4'
        else:
            raise ValueError('Unsupported can speed parameter')
        
        return convertedSpeed
            

    def _updatePeripheralSpeed(self):
        peripheral = self.peripheral.split(',')[0]
        if peripheral == peripherals.kPeripheral_CAN:
            self._speed = self._getConvertedCanSpeedParam(True, '')
        else:          
            if type(self._speed) == type(''):
                if self._speed == '':
                    if peripheral == peripherals.kPeripheral_UART:
                        self._speed = str(peripheralspeed.kUartDefaultSpeed)
                    elif peripheral == peripherals.kPeripheral_SPI:
                        self._speed = str(peripheralspeed.kSpiDefaultSpeed)
                    elif peripheral == peripherals.kPeripheral_I2C:
                        self._speed = str(peripheralspeed.kI2cDefaultSpeed)
                    else:
                        pass
                elif self._speed.find('k'):
                    self._speed = self._speed.split('k')[0]
                else:
                    pass
            elif type(self._speed) == type(0):
                self._speed = str(self._speed)
            else:
                raise ValueError('Invalid peripheral speed parameter: %s' % self._speed)
        
    def _generateCommandArgs(self):
        self._toolName = os.path.abspath(os.path.join(self.vectorsDir, '..', 'blhost'))
        self._commandArgs = []
        self._commandArgs.append(self._toolName)
        peripheralDevice = self.peripheral.split(',')[0]

        if peripheralDevice == peripherals.kPeripheral_USB:
            self._commandArgs.extend(['-u'])
        else:
            self._commandArgs.extend(['-p', self._port])

        if peripheralDevice == peripherals.kPeripheral_UART:
            pass
        elif peripheralDevice in [peripherals.kPeripheral_SPI, peripherals.kPeripheral_I2C, peripherals.kPeripheral_CAN]:
            self._commandArgs.extend(['-b', self.peripheral])
            if not self._usePing:
                self._commandArgs.extend(['-n'])
            pass
        elif peripheralDevice == peripherals.kPeripheral_USB:
            pass
        else:
            raise ValueError('Invalid peripheral parameter: %s' % peripheralDevice)

        self._commandArgs.extend(['-j', '--'])


    ##
    # @ brief change peripheral
    #
    def setPeripheral(self, peripheral):
        self.peripheral = peripheral
        self._generateCommandArgs()


    ##
    # @ brief change port
    #
    def setPort(self, port):
        self._port = port
        self._generateCommandArgs()


    def setVidPid(self, vid, pid):
        findStatus = False
        for i in range(0, len(self._commandArgs)):
            # if self._commandArgs[i] is not null and contains bootloader.peripherals.kPeripheral_SPI
            if self._commandArgs[i] and self._commandArgs[i].find('-u') > -1:
                findStatus = True
                peripheralArgIndex = i
                break

        if findStatus:
            peripheralString = '-u ' + str(vid) + ',' + str(pid)
            self._commandArgs[peripheralArgIndex] = peripheralString

        else:
            raise ValueError('Requires a USB peripheral')

    ##
    # @brief Set the baud rate of the uart.
    #
    def setBaudRate(self, baudrate):
        if '-p' in self._commandArgs:
            portArgIndex = self._commandArgs.index('-p') + 1
            portArgs = self._commandArgs[portArgIndex].split(',')
            if len(portArgs) > 1:
                portArgs[1] = str(baudrate)
            else:
                portArgs.append(str(baudrate))
            self._commandArgs[portArgIndex] = ','.join(portArgs)
        else:
            raise ValueError('Requires a UART peripheral.')


    ##
    # @brief Set the clock frequency of the spi
    #
    def setSpiFrequency(self, frequency):
        peripheralArgIndex = 0
        findStatus = False

        for i in range(0, len(self._commandArgs)):
            # if self._commandArgs[i] is not null and contains bootloader.peripherals.kPeripheral_SPI
            if self._commandArgs[i] and self._commandArgs[i].find(peripherals.kPeripheral_SPI) > -1:
                findStatus = True
                peripheralArgIndex = i
                break

        if findStatus:
            speedString = str(frequency)
            self._commandArgs[peripheralArgIndex] = peripherals.kPeripheral_SPI + ',' + speedString

        else:
            raise ValueError('Requires a SPI peripheral')


    ##
    # @brief Set the clock frequency and slave address of the i2c
    #
    def setI2cParameters(self, frequency, slaveAddress = 0x10):
        peripheralArgIndex = 0
        findStatus = False

        for i in range(0, len(self._commandArgs)):
            # if self._commandArgs[i] is not null and contains peripherals.kPeripheral_I2C
            if self._commandArgs[i] and self._commandArgs[i].find(peripherals.kPeripheral_I2C) > -1:
                findStatus = True
                peripheralArgIndex = i
                break


        if findStatus:
            speedString = str(frequency)
            self._commandArgs[peripheralArgIndex] = peripherals.kPeripheral_I2C + ',' + hex(slaveAddress) + ',' + speedString

        else:
            raise ValueError('Requires a I2C peripheral')

    ##
    # @brief Set the clock frequency and slave rx/ tx address of the can
    #
    def setCanParameters(self, frequency, slaveRxId = 0x321, slaveTxId = 0x123):
        peripheralArgIndex = 0
        findStatus = False

        for i in range(0, len(self._commandArgs)):
            # if self._commandArgs[i] is not null and contains peripherals.kPeripheral_CAN
            if self._commandArgs[i] and self._commandArgs[i].find(peripherals.kPeripheral_CAN) > -1:
                findStatus = True
                peripheralArgIndex = i
                break

        if findStatus:
            speedString = self._getConvertedCanSpeedParam(False, frequency)
            self._commandArgs[peripheralArgIndex] = peripherals.kPeripheral_CAN + ',' + speedString + ',' + hex(slaveRxId) + ',' + hex(slaveTxId)

        else:
            raise ValueError('Requires a CAN peripheral')

    ##
    # @brief Set the timeout value for waiting return value from blhost/blsim
    #
    def setTimeoutValue(self, timeoutSeconds):
        self.timeout = timeoutSeconds

    ##
    # @brief Read memory from device using a read-memory command.
    #
    # Obviously, this method assumes that the bootloader is running on the target and is in
    # a state where it can process a read-memory command.
    def _readMemory(self, start, length):
        returnBytes = bytearray()
        memoryRange = self._getRegion(start)

        # Validate 'start' parameter
        if memoryRange == None:
            raise ValueError('Invalid "start" parameter.')

        # Validate 'length' parameter
        if start + length > memoryRange.start + memoryRange.length:
            raise ValueError('Invalid "length" parameter.')

        # Read memory from device using a read-memory command.
        self.readMemory(start, length)
        returnBytes = open(os.path.join(self.vectorsDir, 'readMemory.dat'), 'rb').read()

        return returnBytes
        
##
# @brief The bootloader running on a real device, SDP mode.
class BootloaderDeviceSDP(Bootloader):

    def __init__(self, target, vectorsDir, peripheral, speed, port, resetTarget):
        super(BootloaderDeviceSDP, self).__init__(target, vectorsDir)
        self._speed = speed     
        self._port = port     
        self._resetTarget = resetTarget
        self._toolName = os.path.abspath(os.path.join(vectorsDir, '..', 'sdphost'))
        self._commandArgs.append(self._toolName)
        self.peripheral = peripheral
        peripheralDevice = peripheral.split(',')[0]

        self._updatePeripheralSpeed()

        if peripheralDevice == peripherals.kPeripheral_SDP_USB:
            self._commandArgs.extend(['-u'])
        else:
            self._commandArgs.extend(['-p', self._port + ',' + self._speed])
            
        # Make the tool executable on OS X. It loses the x bit when Bamboo copies it.
        if sys.platform == 'darwin':
            filetools.makeExecutable(self._toolName)

        # Reset the target running the bootloader firmware.
        if self._resetTarget:
            self.target.reset()
            time.sleep(3)

        self._commandArgs.extend(['-j', '--'])
        
    def close(self):
        self.target.close()

    def __exit__(self, type, value, traceback):
        self.close()
        return False # Don't suppress exceptions
        
    def _updatePeripheralSpeed(self):
        peripheral = self.peripheral.split(',')[0]
        if type(self._speed) == type(''):
            if self._speed == '':
                self._speed = str(peripheralspeed.kUartDefaultSpeed)
            elif self._speed.find('k'):
                self._speed = self._speed.split('k')[0]
            else:
                pass
        elif type(self._speed) == type(0):
            self._speed = str(self._speed)
        else:
            raise ValueError('Invalid peripheral speed parameter: %s' % self._speed)
            
    ## @name SDP commands
    ## @{

    ##
    # @brief SDP read-register command
    def readRegister(self, address, format, numBytes, filePath):
        return self._executeCommand('read-register', address, format, numBytes, filePath)
        
    ##
    # @brief SDP write-register command
    def writeRegister(self, address, format, value):
        return self._executeCommand('write-register', address, format, value)

    ##
    # @brief SDP write-file command
    def writeFile(self, address, filePath):
        return self._executeCommand('write-file', address, filePath)

    ##
    # @brief SDP error-status command
    def errorStatus(self):
        return self._executeCommand('error-status')

    ##
    # @brief SDP dcd-write command
    def dcdWrite(self, address, filePath):
        return self._executeCommand('dcd-write', address, filePath)

    ##
    # @brief SDP skip-dcd-header command
    def skipDcdHeader(self):
        return self._executeCommand('skip-dcd-header')

    ##
    # @brief SDP jump-address command
    def jumpAddress(self, address):
        return self._executeCommand('jump-address', address)

    ## @}
