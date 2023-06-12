import sys
def trimmed(line,sep = ' '):
    s = [w for w in filter(lambda x: len(x) > 0,line.split(sep))]
    return s

infile = open('notes.txt','r')
for line in infile.readlines():
    instruction = ['x']*32
    trim = trimmed(line)
    for word in trim:
        if '..' in word:
            addrs = trimmed(word,'.')
            start = int(addrs[0])
            end = int(addrs[1][:addrs[1].find('=')])
            value = int(addrs[1][addrs[1].find('=')+1:],0)
            bitcount = start-end+1
            for i in range(end,start+1):
                instruction[i] = str(value & 1)
                value >>= 1
    itype = ''
    try:
        itype = line.split('0=3')[1]
    except:
        continue
    itype = trimmed(itype)[0]
    
    sys.stderr.write(itype+'\n')
    name = trim[0]
    while len(name) < 6:
        name += ' '
    print(name + ' '+''.join(reversed(instruction)))
