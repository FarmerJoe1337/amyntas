# NOTE!
Results may vary when attacking! It might peak at 40k rq/s and drop down to 2k rq/s, just so you know!

# about
This version is v3, because v1 and v2 are just too shitty to upload. I made this script to flex on my friends, thats it.
This script is for volumetric layer 7 attacks, not for stealthy and powerfull attacks!

# features
1. Cache bypassing
2. Randomized user agents
3. Randomized referers
4. Rotating proxy support
5. Option to choose custom user agents list
6. Option to choose custom referer list
7. Randomized POST payloads

# known bugs/problems
1. Timing is a bit egh, because thread 1 is already busy attacking when thread 70 just started (for example)
2. Proxies get obliterated when attacking (need to fix)
3. POST and HEAD are not as fast as GET
4. Sometimes script gives "Fatal Python" errors, just ignore them and restart the tool if neccesary

# to do list
1. Implement more methods (Slowloris, CONNECT, PATCH, PUT etc)
2. Better exception handling
3. Animations?
4. ....

# usage
All options:
```
python3 amyntas.py -h
```

Basic usage:
```
python3 amyntas.py -t https://target.com
```

Brute power, 700 threads hammering for 40 seconds:
```
python3 amyntas.py -t https://target.com -w 700 -d 40
```

POST flood, 700 threads and 40 seconds:
```
python3 amyntas.py -t https://target.com -w 700 -d 40 -m POST
```

# images
Note, these are a bit old because i am too lazy to make new screenshots lmao

23k requests per second
![23k](https://github.com/Switch1024/amyntas/blob/main/images/23k_dstat.png?raw=true)

30k requests per second
![30k](https://github.com/Switch1024/amyntas/blob/main/images/30k_dstat.png?raw=true)

507k requests per second
![507k](https://github.com/Switch1024/amyntas/blob/main/images/507k_dstat.png?raw=true)


btw, Toshiro is a skid
