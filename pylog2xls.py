#! /usr/bin/env python

import os, sys, xlwt, re

baseDir = 'log'

devList = []
ResList = []


# filter char
def filterCh(input) :
  return filter(lambda ch: ch in '0123456789. MKB/s', input)

# convert K to 1000 for iops
def to1k(input) :
  input = filterCh(input)
  # print input
  if input[-1:] == 'K' :
    # print int(input[0:-1]) * 1000
    return int(input[0:-1]) * 1000
  else :
    return int(input)

# convert KB/s or B/s to MB/s
def toMB(input) :
  input = filterCh(input)
  # print input
  if input[-4:] == 'MB/s' :
    return float(input[0:-4])
  elif input[-4:] == 'KB/s' :
    return float(input[0:-4]) / 1024
  elif input[-4:] == ' B/s' :
    return float(input[0:-4]) / 1024 / 1024
  elif input[-3:] == 'B/s' :
    return float(input[0:-3]) / 1024 / 1024
  else :
    return float(input)


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
          # print iops[0], bw[0]
          devResult.append(to1k(iops[0].strip()))
          devResult.append(toMB(bw[0]))
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
  for idx in range(0, len(devList)) :
    vol = idx * 2 + 2
    sheet.write(0, vol, devList[idx])
    sheet.write(1, vol, 'iops')
    sheet.write(1, vol + 1, 'bw (MB/s)')

    sheet.write(0, len(devList) * 2 + 2, 'all')
    sheet.write(1, len(devList) * 2 + 2, 'bw (MB/s)')

  for wline in range(0, len(ResList)) :
    for idx in range(0, len(devList) * 2 + 3) :
      sheet.write(wline + 2, idx, ResList[wline][idx])

  wkb.save('result.xls')
  print 'result.xls is saved.'
  sys.exit(0)










