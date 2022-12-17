55df87b23ed27f40b90001e5


def calc_special(d, b):
    rep = {10:'d', 8:'o', 16:'x'}[b]
    n = format(d, rep)
    while True:
        prod = format(d * int(n, b), rep)
        if n[-1:]+n[:-1] == prod: return n
        n = prod[-len(n):]+n[-1:]
____________________________
def calc_special(d,base):
    src,carry = [d],0
    while src[-1]!=1 or carry:
        res = d*src[-1] + carry
        carry,n = divmod(res,base)
        src.append(n)
    return ''.join(hex(v)[2:] for v in src[::-1])
____________________________
def calc_special(n, base):
    d = {8: {1: '1', 2: '1042', 3: '10262054413', 4: '10204', 5: '1015', 6: '10127114202562304053446', 7: '10112362022474404517'},16: {1: '1', 2: '10842', 3: '10572620ae4c415c9882b93', 4: '104', 5: '1033d91d2a2067b23a5440cf6474a8819ec8e95', 6: '102b1da46', 7: '1024e6a17', 8: '1020408', 9: '101ca4b3055ee19', 10: '1019c2d14ee4a', 11: '101767dce434a9b', 12: '101571ed3c506b39a22d9218202ae3da78a0d673445b24304055c7b4f141ace688b6486080ab8f69e28359cd116c90c', 13: '1013c995a47babe74404f265691eeaf9d', 14: '10125e22708092f113840497889c2024bc44e', 15: '10112358e75d30336a0ab617909a3e202246b1ceba6066d4156c2f21347c40448d639d74c0cda82ad85e4268f880891ac73ae9819b5055b0bc84d1f'}, 10: {1: '1', 2: '105263157894736842', 3: '1034482758620689655172413793', 4: '102564', 5: '102040816326530612244897959183673469387755', 6: '1016949152542372881355932203389830508474576271186440677966', 7: '1014492753623188405797', 8: '1012658227848', 9: '10112359550561797752808988764044943820224719'}}
    return d[base][n]
____________________________
num_dict = {x: str(x) for x in range(10)}
num_dict.update({10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'})

def find_cycle_base(n1, n2, base=10):
    if n1 >= n2: return # not support
    quotient, remainder = [], [n1]
    
    while True:
        quotient.append(num_dict[(remainder[-1] * base) // n2 ])
        r = (remainder[-1] * base) % n2
        if r not in remainder:
            remainder.append(r)
        else: break
    return "".join([str(x) for x in quotient])

def calc_special( lastDigit,base ):
    return find_cycle_base(
        lastDigit, lastDigit * base - 1, base)
____________________________
dic = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'A',11:'B',12:'C',13:'D',14:'E',15:'F'}
def calc_special( lastDigit,base ):
    carry = 0
    num = [lastDigit]
    while True:
        num.append((lastDigit*num[-1]+carry)%base)
        carry = (lastDigit*num[-2]+carry)//base        
        if num[-1] == lastDigit and carry == 0:
            break
    for i in range(len(num)):
        num[i] = dic[num[i]]
    return ''.join(num[::-1][1:])
____________________________
from numpy import base_repr as to_base

def calc_special(t, i):
    l,n,o = 0,t,to_base(t,i)
    while True:
        l = n*t+l//i
        n = l%i
        o = to_base(n,i)+o
        if l==t: break
    return o[1:]
