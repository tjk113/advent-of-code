#!/usr/bin/python
import os
dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
last = sorted(dirs, key=lambda d: int(d.split("day")[1]))[-1][-1]
cur = str(int(last) + 1)
os.system("&&".join([
          f"cd {os.getcwd()}",
          f"cp -r day{last} day{cur}",
          f"cd day{cur}",
          f"rm day{last}",
          f"rename {last} {cur} day*",
          f"> input.txt",
          f"> test.txt"]))
