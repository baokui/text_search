#!/usr/bin/python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
for data in sys.stdin:
    data = data.strip()
    #fields = data.split('\t')
    sys.stdout.write("%s\n" % data)