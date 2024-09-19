from ipaddress import ip_address

def ips_between(start, end):
    return int(ip_address(end)) - int(ip_address(start))
_________________________
def ips_between(start, end):
    ip_end = list(map(int, end.split('.')))
    ip_start = list(map(int, start.split('.')))
    return sum(((ip_end[i] - ip_start[i])*(256**(3 - i)) for i in range(4)))
_______________________
def ips_between(start, end):
    count = 0
    for i in range(0,4):
        count += ((int(end.split(sep='.')[i])) - (int(start.split(sep='.')[i])))*256**(3-i)
    return count
________________________
def ips_between(start, end):
    start_ = [int(i) for i in start.split('.')] 
    a1 = ((int(start_[0]) << 24) + (int(start_[1]) << 16) + (int(start_[2]) << 8) + int(start_[3]))
    end_ = [int(i) for i in end.split('.')] 
    a2 = ((int(end_[0]) << 24) + (int(end_[1]) << 16) + (int(end_[2]) << 8) + int(end_[3]))
    return a2-a1
