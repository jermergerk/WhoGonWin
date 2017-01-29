#!/usr/bin/env python
import time
import datetime
from datetime import timedelta, date
import json
import billboard

start_date = date(2015, 12, 13)
end_date = date(2017, 12, 29)

d = start_date
delta = datetime.timedelta(days=1)
while d <= end_date:
	print(d.strftime("%Y-%m-%d"))
	filename = d.strftime("%Y-%m-%d") + ".txt"
	chart = billboard.ChartData("hot-100", d)
	print (len(chart.entries))
	if (len(chart.entries) > 0):
		chartStr = "[\n"
		for entry in chart.entries:
			chartStr += entry.to_JSON() + ",\n"
		chartStr = chartStr[:-2]
		chartStr += "]"
		f = open(filename, 'w')
		f.write(chartStr)
		f.close()
		# print d.strftime("%Y-%m-%d")
	d += delta
