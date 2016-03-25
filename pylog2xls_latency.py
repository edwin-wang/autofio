#! /usr/bin/env python

'''

Convert fio_perf.py result to Excel file

                        Yangming Wang 
                        wym@marvell.com

'''

import os, sys, xlwt, re

baseDir = 'log'

devList = []
ResList = []


# filter char
def filterCh(inputVal) :
  return filter(lambda ch: ch in '0123456789. MKB/s', inputVal)

# convert K to 1000 for iops
def to1k(inputVal) :
  inputVal = filterCh(inputVal)
  # print inputVal
  if inputVal[-1:] == 'K' :
    # print int(inputVal[0:-1]) * 1000
    return int(inputVal[0:-1]) * 1000
  else :
    return int(inputVal)
  
# convert KB/s or B/s to MB/s
def toMB(inputVal) :
  inputVal = filterCh(inputVal)
  # print inputVal
  if inputVal[-4:] == 'KB/s' :
    return float(inputVal[0:-4]) / 1024
  elif inputVal[-4:] == ' B/s' :
    return float(inputVal[0:-4]) / 1024 / 1024
  elif inputVal[-3:0] == 'B/s' :
    return float(inputVal[0:-3]) / 1024 / 1024
  elif inputVal[-4:] == 'MB/s' :
    return float(inputVal[0:-4])
  else :
    return float(inputVal)

def touSec(inputVal, inputUnit) :
  if inputUnit == 'usec' :
    lat = inputVal
  elif inputUnit == 'msec' :
    lat = inputVal * 1000
  elif inputUnit == 'sec' :
    lat = inputVal * 1000 * 1000
  else :
    lat = 'n/a'
  return lat


if __name__ == "__main__" :
  
  logFiles = os.listdir(baseDir)
  logFiles = sorted(logFiles)
  # print logFiles
  
  # get dev, r'^.*?:'
  fl = open(os.path.join(baseDir, logFiles[0]), 'r').readlines()
  for line in fl :
    dev = re.findall(r'^(/.*?):', line.strip(), re.M)
    if len(dev) == 0 :
      break
    else :
      devList.append(dev[0])
      
  # print devList
  
  for f in logFiles :
  
    # read log file
    # print f
    fl = open(os.path.join(baseDir, f), 'r').readlines()

    devResult = []
    
    # get spec string
    specRW = re.findall(r'^.*?_(.*?)_', f, re.M)
    specBlock = re.findall(r'^.*?_.*?_(.*?)_', f, re.M)
    # print specRW, specBlock
    devResult.append(specRW[0])
    devResult.append(specBlock[0])
    
    # get score for each dev
    for item in devList :
    
      catchStr = item + ': (groupid='
      
      for idx, val in enumerate(fl) :
        if val.find(catchStr) == 0 :
          bw = re.findall(r'^.*?bw=(.*?), ', fl[idx + 1], re.M)
          iops = re.findall(r'^.*?iops=(.*?), ', fl[idx + 1], re.M)
          
          unitTitle = re.findall(r'^.*?slat \((.*?)\):', fl[idx + 2], re.M)[0]
          unitVal = float(re.findall(r'^.*?slat.*?, avg=(.*?), ', fl[idx + 2], re.M)[0])
          slat = touSec(unitVal, unitTitle)

          unitTitle = re.findall(r'^.*?clat \((.*?)\):', fl[idx + 3], re.M)[0]
          unitVal = float(re.findall(r'^.*?clat.*?, avg=(.*?), ', fl[idx + 3], re.M)[0])
          clat = touSec(unitVal, unitTitle)
          
          unitTitle = re.findall(r'^.*?lat \((.*?)\):', fl[idx + 4], re.M)[0]
          unitVal = float(re.findall(r'^.*?lat.*?, avg=(.*?), ', fl[idx + 4], re.M)[0])
          lat = touSec(unitVal, unitTitle)
          
          # print iops[0], bw[0]
          devResult.append(to1k(iops[0].strip()))
          devResult.append(toMB(bw[0]))
          devResult.append(slat)
          devResult.append(clat)
          devResult.append(lat)
          break
          
    # get score for all dev
    catchStr = '(all jobs):'
    for idx, val in enumerate(fl) :
      # print val.find(catchStr)
      if val.find(catchStr) != -1 :
        aggrb = re.findall(r'^.*?aggrb=(.*?), ', fl[idx + 1], re.M)
        # print aggrb[0]
        devResult.append(toMB(aggrb[0]))
        break
    
    # print devResult
    ResList.append(devResult)
  
  # print ResList
  
  wkb = xlwt.Workbook(encoding='utf-8')
  sheet = wkb.add_sheet('perf_result', cell_overwrite_ok=True)
  
  # print len(devList)
  devVolCount = 5 #2
  for idx in range(0, len(devList)) :
    vol = idx * devVolCount + 2
    sheet.write(0, vol, devList[idx])
    sheet.write(1, vol, 'iops')
    sheet.write(1, vol + 1, 'bw (MB/s)')
    sheet.write(1, vol + 2, 'slat (us)')
    sheet.write(1, vol + 3, 'clat (us)')
    sheet.write(1, vol + 4, 'lat (us)')
    
    sheet.write(0, len(devList) * devVolCount + 2, 'all')
    sheet.write(1, len(devList) * devVolCount + 2, 'bw (MB/s)')
  
  # print ResList

  for wline in range(0, len(ResList)) :
    for idx in range(0, len(devList) * 5 + 3) :
      sheet.write(wline + 2, idx, ResList[wline][idx])
      
  wkb.save('result.xls')
  print 'result.xls is saved.'
  sys.exit(0)
  
