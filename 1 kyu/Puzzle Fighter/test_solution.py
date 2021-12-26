import codewars_test as test
from solution import puzzle_fighter

from random import shuffle, randrange as rand, randint
from itertools import *
import re


#solution verification
def ver_funk(s,es):
    top_border = ' ___ __ '
    bot_border = ' ------ '
    def frame_gen(r):
        field = [top_border]
        field.extend(['|{}|'.format(v) for v in r])
        field.append(bot_border)
        return '\n'.join(['{0:>2}'.format(i-1)+x if i%13 else '  '+x for i,x in enumerate(field)])
    if type(es) == list:
        sol,states = es
    else:
        sol,states = es,None
    if type(s) != str:
        return test.expect(False,'Invalid return type - Must return a string.',allow_raise=True)
    rform = None
    if '\n' in s:
        rform = s.split('\n')
        if len(rform) != 12 or not all([len(v) == 6 for v in rform]):
            rform = None
    if rform == None: return test.expect(False,'Invalid structure: {}'.format(s),allow_raise=True)
    rform = frame_gen(rform)
    if s == sol: print('Correct!\nYour result:\n{}'.format(rform))
    else:
        print('Incorrect result. Your result:\n{}\nExpected:\n{}'.format(rform,frame_gen(sol.split('\n'))))
        if see_states and states:
            print('Game States for each Gem pair:')
            for i,v in enumerate(states):
                print('PAIR {}: {} | MOVE:{}\n{}\n'.format(i,v[0][0],v[0][1],frame_gen(v[1].split('\n'))))
    return test.expect(s == sol,allow_raise=True)



@test.describe('Full Test Suite')
def _():

    # 10 FIXED TESTS
    @test.it('10 FIXED TESTS')
    def _():
        fixed_tests = [
            [['BR','LLL'],['BY','LL'],['BG','ALL'],['BY','BRR'],['RR','AR'],['GY','A'],['BB','AALLL'],['GR','A'],['RY','LL'],['GG','L'],['GY','BB'],['bR','ALLL'],['gy','AAL']],
            [['GR','ALLL'],['GG','ALLL'],['RG','AAL'],['RB','BLL'],['RG','ALL'],['BB','RR'],['BR','BB'],['BR','ALLL'],['YB','R'],['BG','BBRR'],['YR','AAR'],['RR','L'],['RR','ABLL'],['GY','BRR'],['BB','R'],['gB','RR'],['BR','ALL'],['Gr','BB'],['Rb','R'],['GG','B'],['bB','LL']],
            [['RR','LLL'],['GG','LL'],['RG','BBL'],['GY','AR'],['RR','BBLLL'],['RB','AALL'],['GR','B'],['GB','AR'],['RR',''],['GG','R'],['YR','BR'],['RR','LLL'],['BR','AALL'],['Bg',''],['RR','BBBBLLL'],['GR','ALLL'],['bR','L'],['YG','BBBALL'],['RR','L'],['YB','AL']],
            [['YY','BALLL'],['RR','AALL'],['RG','BR'],['YG','ALLR'],['BG','BRR'],['YR','BBLLLL'],['GR','BL'],['GG','ALB'],['GY',''],['yB','RR'],['GG','R'],['RB','LLLAAAB'],['Ry','LL'],['BG','BR'],['RB','BBRRR'],['Rg','R'],['bR','L'],['YR','BLLL'],['RR','LLLLLLLL'],['Yg','AALL'],['Br','LLL']],
            [['BB','LLLL'],['BB','LL'],['BB','L'],['BB','LLL'],['BB','LL'],['BG','L'],['BB',''],['BB','R'],['RB','BBRRR'],['RR','LLL'],['RR','BALL'],['RR',''],['RR','R'],['RR','L'],['RR','B'],['RR','LLL'],['RR','LL'],['RR','BLLL'],['RR','B'],['YR','ALL'],['GR','AL'],['Rb','RRRR']],
            [['RY','ALLL'],['YY','L'],['RG','BBR'],['YR','BLL'],['RR','ALLLL'],['GY','B'],['RR','RRRRRRR'],['RY','ALLL'],['BY','BBBBLL'],['BY','L'],['BG','BBBL'],['BB','LLL'],['BY','BBLL'],['BR','AL'],['RB','AR'],['BB','RR'],['GG','R'],['YB','LLLRR'],['GG',''],['rb','RR'],['bY','ABLL'],['GY','L'],['GR','BRR'],['RR','LLL'],['yy','LLLB'],['RY','BB']],
            [['YR','LLL'],['GY','LLLRL'],['RY','BBLL'],['RB','AAL'],['GR','BR'],['GG','A'],['YY','LL'],['GG','BLLL'],['YY','ALLL'],['BY','BL'],['YB','ALLLR'],['RY','LLLB'],['GG','BBBBB'],['GB','A'],['GR','AA'],['gB','AALAB'],['YR','RRAAA'],['BB',''],['RG','AL'],['GG','L'],['RG','RRBL'],['Gb','A'],['rB','R'],['GG','RR'],['RB','AARR'],['GG','BR'],['bR','AARR']],
            [['BB','AALLL'],['GR','RR'],['RR','R'],['RG','A'],['YY','BBBL'],['BG','RR'],['BY',''],['Rg','RR'],['YB','A'],['BY','RRAA'],['BY','L'],['yB','LLLBB'],['YR','A'],['Yy','BBB'],['rY','BR'],['Rb','BRR'],['gR','ARR'],['BB','B'],['BG','B'],['RG','BBLL'],['YG','LLLA'],['GG','L'],['RY','BRR'],['bB','']],
            [['GY','LL'],['BG','R'],['BB','BR'],['GG','BR'],['RG','AAL'],['GB','BBRR'],['YG','RR'],['YG','BRR'],['BG','LL'],['GB',''],['RR','R'],['YR','AAAA'],['RB','RRA'],['YB','BB'],['BY','LLLB'],['bY','R'],['GB','L'],['RR','L'],['0G','AARR'],['RB','AAL'],['GB','ALL'],['yB','R'],['Br','LLLA'],['BY','L'],['GR','ALL'],['B0','L'],['rY','ALL'],['RB','ALLL'],['BR','ALL'],['RR','LLLLR'],['GY','ALLL'],['BB','LL'],['0G','RRA'],['yr','AALL']],
            [['RR','LLL'],['RR','LLL'],['GG','LLL'],['RR','LLL'],['YY','LL'],['YY','LL'],['BY','LL'],['BG','L'],['YY','L'],['RR','LL'],['BR','L'],['Yb','AAL'],['GG',''],['BB','R'],['GG','R'],['GG',''],['GB','BBRR'],['BR',''],['BY','RBR'],['BB','RRRR'],['BB','AARR'],['yB','R'],['Bg','A'],['RR',''],['Br','']]
        ]
        fixed_test_states = [
            [
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nB     \nR     ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nBB    \nRY    ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n B    \nBB    \nRYG   ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n B    \nBB    \nRYG YB',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n B    \nBB  RR\nRYG YB',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n B  Y \nBB  RR\nRYGGYB',
                '      \n      \n      \n      \n      \n      \n      \n      \nB     \nBB  Y \nBB  RR\nRYGGYB',
                '      \n      \n      \n      \n      \n      \n      \n      \nB   R \nBB  Y \nBB GRR\nRYGGYB',
                '      \n      \n      \n      \n      \n      \n      \n R    \nBY  R \nBB  Y \nBB GRR\nRYGGYB',
                '      \n      \n      \n      \n      \n      \n      \n R    \nBY  R \nBBG Y \nBBGGRR\nRYGGYB',
                '      \n      \n      \n      \n      \n      \n      \n R    \nBY YR \nBBGGY \nBBGGRR\nRYGGYB',
                '      \n      \n      \n      \n      \n      \n      \n      \n R YR \n RGGY \n YGGRR\nRYGGYB',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n    R \n R  YR\nRR  RB'],
            [
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nGR    ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nGG    \nGR    ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nGGG   \nGRR   ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \nBR    \nGGG   \nGRR   ',
                '      \n      \n      \n      \n      \n      \n      \n      \n R    \nBRG   \nGGG   \nGRR   ',
                '      \n      \n      \n      \n      \n      \n      \n      \n R    \nBRG   \nGGG  B\nGRR  B',
                '      \n      \n      \n      \n      \n      \n      \n      \n R    \nBRG   \nGGGR B\nGRRB B',
                '      \n      \n      \n      \n      \n      \n      \n R    \nBR    \nBRG   \nGGGR B\nGRRB B',
                '      \n      \n      \n      \n      \n      \n      \n R    \nBR    \nBRG   \nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n      \n      \n      \n R    \nBR   G\nBRG  B\nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n      \n      \n      \n R    \nBR  RG\nBRG YB\nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n      \n      \n      \n RR   \nBRR RG\nBRG YB\nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n      \n R    \n R    \n RR   \nBRR RG\nBRG YB\nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n      \n R    \n R    \n RR YG\nBRR RG\nBRG YB\nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n      \n R  B \n R  B \n RR YG\nBRR RG\nBRG YB\nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n      \n R  Bg\n R  BB\n RR YG\nBRR RG\nBRG YB\nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n B    \n R  Bg\n RR BB\n RR YG\nBRR RG\nBRG YB\nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n      \n     g\n    BB\n    BG\nB   YG\nBBGGYB\nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n      \n      \n      \n    R \nB   Y \nBBGGYB\nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n      \n      \n      \n    R \nB GGY \nBBGGYB\nGGGRYB\nGRRBBB',
                '      \n      \n      \n      \n      \n      \n      \n    R \n  GGY \n  GGYB\nGGGRYB\nGRRBBB'],
            [
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nR     \nR     ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nRG    \nRG    ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nRGG   \nRGR   ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nRGG   \nRGR GY',
                '      \n      \n      \n      \n      \n      \n      \n      \nR     \nR     \nRGG   \nRGR GY',
                '      \n      \n      \n      \n      \n      \n      \n      \nRB    \nRR    \nRGG   \nRGR GY',
                '      \n      \n      \n      \n      \n      \n      \n      \nRB    \nRRR   \nRGG   \nRGRGGY',
                '      \n      \n      \n      \n      \n      \n      \n      \nRB    \nRRR   \nRGG GB\nRGRGGY',
                '      \n      \n      \n      \n      \n      \n      \n      \nRB    \nRRRR  \nRGGRGB\nRGRGGY',
                '      \n      \n      \n      \n      \n      \n      \n      \nRB  G \nRRRRG \nRGGRGB\nRGRGGY',
                '      \n      \n      \n      \n      \n      \n      \n    Y \nRB RG \nRRRRG \nRGGRGB\nRGRGGY',
                '      \n      \n      \n      \n      \n      \nR     \nR   Y \nRB RG \nRRRRG \nRGGRGB\nRGRGGY',
                '      \n      \n      \n      \n      \n      \nRR    \nRB  Y \nRB RG \nRRRRG \nRGGRGB\nRGRGGY',
                '      \n      \n      \n      \n      \n      \nRR B  \nRB gY \nRB RG \nRRRRG \nRGGRGB\nRGRGGY',
                '      \n      \n      \n      \nR     \nR     \nRR B  \nRB gY \nRB RG \nRRRRG \nRGGRGB\nRGRGGY',
                '      \n      \n      \nG     \nR     \nRR    \nRR B  \nRB gY \nRB RG \nRRRRG \nRGGRGB\nRGRGGY',
                '      \n      \n      \nG     \nR     \nRR    \nRR B  \nR  gY \nR RRG \nRRRRG \nRGGRGB\nRGRGGY',
                '      \n      \n      \nGG    \nRY    \nRR    \nRR B  \nR  gY \nR RRG \nRRRRG \nRGGRGB\nRGRGGY',
                '      \n      \n      \nGG    \nRY    \nRR    \nRRRB  \nR RgY \nR RRG \nRRRRG \nRGGRGB\nRGRGGY',
                '      \n      \n      \nGG    \nRY    \nRRYB  \nRRRB  \nR RgY \nR RRG \nRRRRG \nRGGRGB\nRGRGGY'],
            [
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nY     \nY     ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nYR    \nYR    ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nYR    \nYR GR ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nYR G  \nYRYGR ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nYR GG \nYRYGRB',
                '      \n      \n      \n      \n      \n      \n      \n      \nR     \nY     \nYR GG \nYRYGRB',
                '      \n      \n      \n      \n      \n      \n      \n      \nR     \nYR    \nYRGGG \nYRYGRB',
                '      \n      \n      \n      \n      \n      \n      \n      \nR G   \nYRG   \nYRGGG \nYRYGRB',
                '      \n      \n      \n      \n      \n      \n      \n      \nR GG  \nYRGY  \nYRGGG \nYRYGRB',
                '      \n      \n      \n      \n      \n      \n      \n      \nR GG  \nYRGY y\nYRGGGB\nYRYGRB',
                '      \n      \n      \n      \n      \n      \n      \n      \nR GGG \nYRGYGy\nYRGGGB\nYRYGRB',
                '      \n      \n      \n      \n      \n      \n      \n B    \nRRGGG \nYRGYGy\nYRGGGB\nYRYGRB',
                '      \n      \n      \n      \n      \n R    \n y    \n B    \nRRGGG \nYRGYGy\nYRGGGB\nYRYGRB',
                '      \n      \n      \n      \n      \n R    \n y    \n B GB \nRRGGG \nYRGYGy\nYRGGGB\nYRYGRB',
                '      \n      \n      \n      \n      \n R    \n y    \n B GBB\nRRGGGR\nYRGYGy\nYRGGGB\nYRYGRB',
                '      \n      \n      \n      \n      \n R  R \n y  g \n B GBB\nRRGGGR\nYRGYGy\nYRGGGB\nYRYGRB',
                '      \n      \n      \n      \n      \n R  R \n yb g \n BRGBB\nRRGGGR\nYRGYGy\nYRGGGB\nYRYGRB',
                '      \n      \n      \n      \n Y    \n R  R \n yb g \nRBRGBB\nRRGGGR\nYRGYGy\nYRGGGB\nYRYGRB',
                '      \n      \n      \n      \n Y    \nRR  R \nRyb g \nRBRGBB\nRRGGGR\nYRGYGy\nYRGGGB\nYRYGRB',
                '      \n      \n g    \n Y    \n Y    \nRR  R \nRyb g \nRBRGBB\nRRGGGR\nYRGYGy\nYRGGGB\nYRYGRB',
                '      \n      \n      \n      \n      \n      \n      \n     B\n    RR\n  b gy\n  R BB\nBBYYRB'],
            [
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nB     \nB     ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nBB    \nBB    ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nBBB   \nBBB   ',
                '      \n      \n      \n      \n      \n      \n      \n      \nB     \nB     \nBBB   \nBBB   ',
                '      \n      \n      \n      \n      \n      \n      \n      \nBB    \nBB    \nBBB   \nBBB   ',
                '      \n      \n      \n      \n      \n      \n      \n      \nBBB   \nBBG   \nBBB   \nBBB   ',
                '      \n      \n      \n      \n      \n      \n      \n      \nBBB   \nBBG   \nBBBB  \nBBBB  ',
                '      \n      \n      \n      \n      \n      \n      \n      \nBBB   \nBBG   \nBBBBB \nBBBBB ',
                '      \n      \n      \n      \n      \n      \n      \n      \nBBB   \nBBG   \nBBBBBB\nBBBBBR',
                '      \n      \n      \n      \n      \n      \nR     \nR     \nBBB   \nBBG   \nBBBBBB\nBBBBBR',
                '      \n      \n      \n      \n      \n      \nRR    \nRR    \nBBB   \nBBG   \nBBBBBB\nBBBBBR',
                '      \n      \n      \n      \n      \n      \nRR    \nRR    \nBBBR  \nBBGR  \nBBBBBB\nBBBBBR',
                '      \n      \n      \n      \n      \n      \nRR    \nRR    \nBBBRR \nBBGRR \nBBBBBB\nBBBBBR',
                '      \n      \n      \n      \n      \n      \nRRR   \nRRR   \nBBBRR \nBBGRR \nBBBBBB\nBBBBBR',
                '      \n      \n      \n      \n      \n  R   \nRRR   \nRRRR  \nBBBRR \nBBGRR \nBBBBBB\nBBBBBR',
                '      \n      \n      \n      \nR     \nR R   \nRRR   \nRRRR  \nBBBRR \nBBGRR \nBBBBBB\nBBBBBR',
                '      \n      \n      \n      \nRR    \nRRR   \nRRR   \nRRRR  \nBBBRR \nBBGRR \nBBBBBB\nBBBBBR',
                '      \n      \n      \nRR    \nRR    \nRRR   \nRRR   \nRRRR  \nBBBRR \nBBGRR \nBBBBBB\nBBBBBR',
                '      \n      \n      \nRR    \nRRR   \nRRR   \nRRRR  \nRRRR  \nBBBRR \nBBGRR \nBBBBBB\nBBBBBR',
                '      \n      \n Y    \nRRR   \nRRR   \nRRR   \nRRRR  \nRRRR  \nBBBRR \nBBGRR \nBBBBBB\nBBBBBR',
                '      \n      \n YG   \nRRR   \nRRR   \nRRRR  \nRRRR  \nRRRR  \nBBBRR \nBBGRR \nBBBBBB\nBBBBBR',
                '      \n      \n      \n      \n YG   \nRRR   \nRRR   \nRRRR  \nRRRR  \nRRRR  \n   RRR\n  GRRR'],
            [
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nRY    ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \n  Y   \nRYY   ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \n  Y G \nRYY R ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nRYY G \nRYY R ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \nRR    \nRYY G \nRYY R ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \nRRY   \nRYY G \nRYYGR ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \nRRY   \nRYY GR\nRYYGRR',
                '      \n      \n      \n      \n      \n      \n      \n      \nRY    \nRRY   \nRYY GR\nRYYGRR',
                '      \n      \n      \n      \n      \n      \n B    \n Y    \nRY    \nRRY   \nRYY GR\nRYYGRR',
                '      \n      \n      \n      \n      \n      \n B    \n YB   \nRYY   \nRRY   \nRYY GR\nRYYGRR',
                '      \n      \n      \n      \n      \n      \n BB   \n YB   \nRYY   \nRRY   \nRYYGGR\nRYYGRR',
                '      \n      \n      \n      \n      \n      \nBBB   \nBYB   \nRYY   \nRRY   \nRYYGGR\nRYYGRR',
                '      \n      \n      \n      \n Y    \n B    \nBBB   \nBYB   \nRYY   \nRRY   \nRYYGGR\nRYYGRR',
                '      \n      \n      \n      \n Y    \n BB   \nBBB   \nBYB   \nRYY   \nRRYR  \nRYYGGR\nRYYGRR',
                '      \n      \n      \n      \n Y    \n BB   \nBBB   \nBYB   \nRYY   \nRRYRRB\nRYYGGR\nRYYGRR',
                '      \n      \n      \n      \n Y    \n BB   \nBBB   \nBYB  B\nRYY  B\nRRYRRB\nRYYGGR\nRYYGRR',
                '      \n      \n      \n      \n Y    \n BB   \nBBB   \nBYB GB\nRYY GB\nRRYRRB\nRYYGGR\nRYYGRR',
                '      \n      \n      \n  Y   \n YB   \n BB   \nBBB   \nBYB GB\nRYY GB\nRRYRRB\nRYYGGR\nRYYGRR',
                '      \n      \n      \n  Y   \n YB   \n BB   \nBBB   \nBYBGGB\nRYYGGB\nRRYRRB\nRYYGGR\nRYYGRR',
                '      \n      \n      \n  Y   \n YB   \n BB   \nBBB   \nBYB   \nRYYGG \nRRYGG \nRYYG  \nRYYGG ',
                '      \n      \n b    \n YY   \n YB   \n BB   \nBBB   \nBYB   \nRYYGG \nRRYGG \nRYYG  \nRYYGG ',
                '      \n  G   \n bY   \n YY   \n YB   \n BB   \nBBB   \nBYB   \nRYYGG \nRRYGG \nRYYG  \nRYYGG ',
                '      \n  G   \n bY   \n YY   \n YB   \n BB   \nBBB   \nBYB R \nRYYGG \nRRYGG \nRYYG  \nRYYGGG',
                '      \n  G   \n bY   \n YY   \nRYB   \nRBB   \nBBB   \nBYB R \nRYYGG \nRRYGG \nRYYG  \nRYYGGG',
                '      \n      \n      \n      \n      \n      \nR     \nR   R \nR  GG \nR  GG \nR  G  \nRRGGGG',
                '      \n      \n      \n      \n      \n      \nR  Y  \nR  RR \nR  GG \nR  GG \nR  G  \nRRGGGG'],
            [
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nY     \nR     ',
                '      \n      \n      \n      \n      \n      \n      \n      \nG     \nY     \nY     \nR     ',
                '      \n      \n      \n      \n      \n      \n      \n      \nG     \nY     \nYY    \nRR    ',
                '      \n      \n      \n      \n      \n      \n      \n      \nG     \nY     \nYYB   \nRRR   ',
                '      \n      \n      \n      \n      \n      \n      \n      \nG     \nY     \nYYB   \nRRRRG ',
                '      \n      \n      \n      \n      \n      \n      \n      \nG     \nY     \nYYBGG \nRRRRG ',
                '      \n      \n      \n      \n      \n      \n      \n      \nGY    \nYY    \nYYBGG \nRRRRG ',
                '      \n      \n      \n      \n      \n      \n      \nGG    \nGY    \nYY    \nYYBGG \nRRRRG ',
                '      \n      \n      \n      \n      \n      \nYY    \nGG    \nGY    \nYY    \nYYBGG \nRRRRG ',
                '      \n      \n      \n      \n      \n Y    \nYY    \nGG    \nGY    \nYYB   \nYYBGG \nRRRRG ',
                '      \n      \n      \n      \n Y    \n Y    \nYY    \nGG    \nGYB   \nYYB   \nYYBGG \nRRRRG ',
                '      \n      \n      \n R    \n Y    \nYY    \nYY    \nGG    \nGYB   \nYYB   \nYYBGG \nRRRRG ',
                '      \n      \n      \n R    \n Y    \nYY    \nYY    \nGGG   \nGYB   \nYYBG  \nYYBGG \nRRRRG ',
                '      \n      \n      \n R    \n Y    \nYY    \nYY    \nGGG   \nGYBG  \nYYBGB \nYYBGG \nRRRRG ',
                '      \n      \n      \n R    \n Y    \nYY    \nYY R  \nGGGG  \nGYBG  \nYYBGB \nYYBGG \nRRRRG ',
                '      \n      \n      \n      \n R    \n Y    \nYY    \nYYB   \n YB   \nYYB   \nYYBR  \nRRRRB ',
                '      \n      \n      \n      \n R    \n Y    \nYY    \nYYB   \n YB   \nYYBR  \nYYBRY \nRRRRB ',
                '      \n      \n      \n      \n R    \n Y    \nYY    \nYYBB  \n YBB  \nYYBR  \nYYBRY \nRRRRB ',
                '      \n      \n      \n      \n R    \n Y    \nYYRG  \nYYBB  \n YBB  \nYYBR  \nYYBRY \nRRRRB ',
                '      \n      \n      \n      \n RG   \n YG   \nYYRG  \nYYBB  \n YBB  \nYYBR  \nYYBRY \nRRRRB ',
                '      \n      \n      \n      \n RG   \n YGG  \nYYRG  \nYYBB  \n YBB  \nYYBRR \nYYBRY \nRRRRB ',
                '      \n      \n      \n      \n R    \n Y    \nYYGG  \nYYGG  \n Y G  \nYY RR \nYYRRY \nRRRRB ',
                '      \n      \n      \n      \n R    \n Y    \nYYGG  \nYYGGr \n Y GB \nYY RR \nYYRRY \nRRRRB ',
                '      \n      \n      \n      \n R    \n Y    \nYYGG  \nYYGGr \n Y GB \nYY RR \nYYRRYG\nRRRRBG',
                '      \n      \n      \n      \n R    \n Y    \nYYGG  \nYYGGr \n Y GBB\nYY RRR\nYYRRYG\nRRRRBG',
                '      \n      \n      \n      \n R    \n Y G  \nYYGGG \nYYGGr \n Y GBB\nYY RRR\nYYRRYG\nRRRRBG',
                '      \n      \n      \n      \n      \n R    \n Y    \nYY    \nYY G  \n YGGG \nYYGGYG\nYY GBG'],
            [
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nB     \nB     ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nB    G\nB    R',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nB   RG\nB   RR',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n    G \nB   RG\nB  RRR',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n    G \nB  YRG\nB YRRR',
                '      \n      \n      \n      \n      \n      \n      \n      \n     B\n    GG\nB  YRG\nB YRRR',
                '      \n      \n      \n      \n      \n      \n      \n      \n   B B\n   YGG\nB  YRG\nB YRRR',
                '      \n      \n      \n      \n      \n      \n     R\n     g\n   B B\n   YGG\nB  YRG\nB YRRR',
                '      \n      \n      \n      \n      \n      \n     R\n   Y g\n   BBB\n   YGG\nB  YRG\nB YRRR',
                '      \n      \n      \n      \n      \n      \n    YR\n   YBg\n   BBB\n   YGG\nB  YRG\nB YRRR',
                '      \n      \n      \n      \n      \n      \n    YR\n   YBg\n   BBB\n  BYGG\nB YYRG\nB YRRR',
                '      \n      \n      \n      \n      \n      \n    YR\n    Bg\n    BB\n   YGG\nB  BRG\nBBBRRR',
                '      \n      \n      \n      \n      \n    R \n    YR\n    Bg\n   YBB\n   YGG\nB  BRG\nBBBRRR',
                '      \n      \n      \n      \n    y \n    R \n    YR\n   YBg\n   YBB\n   YGG\nB  BRG\nBBBRRR',
                '      \n      \n      \n    r \n    y \n    R \n   YYR\n   YBg\n   YBB\n   YGG\nB  BRG\nBBBRRR',
                '      \n      \n    b \n    r \n    y \n    RR\n   YYR\n   YBg\n   YBB\n   YGG\nB  BRG\nBBBRRR',
                '      \n    g \n    b \n    r \n    yR\n    RR\n   YYR\n   YBg\n   YBB\n   YGG\nB  BRG\nBBBRRR',
                '      \n    g \n    b \n    r \n    yR\n   BRR\n   YYR\n   YBg\n   YBB\n   YGG\nB BBRG\nBBBRRR',
                '      \n    g \n    b \n    r \n   ByR\n   BRR\n   YYR\n   YBg\n   YBB\n  GYGG\nB BBRG\nBBBRRR',
                '      \n    g \n    b \n    r \n   ByR\n   BRR\n   YYR\n   YBg\n   YBB\n GGYGG\nBRBBRG\nBBBRRR',
                '      \n    g \n    b \n    r \n   ByR\n   BRR\n   YYR\n   YBg\n G YBB\nYGGYGG\nBRBBRG\nBBBRRR',
                '      \n    g \n    b \n    r \n   ByR\n   BRR\n   YYR\n  GYBg\n GGYBB\nYGGYGG\nBRBBRG\nBBBRRR',
                '      \n      \n      \n      \n      \n    Y \n    g \n  G Bg\n GG BB\nYGG GG\nBRBBRG\nBBBRRR',
                '      \n      \n      \n      \n      \n      \n      \n      \n  G   \n GG Y \n GG R \nYR RRR'],
            [
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \n G    \n Y    ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \n G  B \n Y  G ',
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n    B \n G  B \n Y BG ',
                '      \n      \n      \n      \n      \n      \n      \n      \n    G \n    B \n G GB \n Y BG ',
                '      \n      \n      \n      \n      \n      \n      \n      \n    G \n    B \n GGGB \n YRBG ',
                '      \n      \n      \n      \n      \n      \n      \n      \n    G \n    B \n GGGBB\n YRBGG',
                '      \n      \n      \n      \n      \n      \n      \n      \n    GY\n    BG\n GGGBB\n YRBGG',
                '      \n      \n      \n      \n      \n      \n      \n    GY\n    GY\n    BG\n GGGBB\n YRBGG',
                '      \n      \n      \n      \n      \n      \n      \n    GY\n B  GY\n G  BG\n GGGBB\n YRBGG',
                '      \n      \n      \n      \n      \n      \n      \n    GY\n B GGY\n G BBG\n GGGBB\n YRBGG',
                '      \n      \n      \n      \n      \n    R \n    R \n    GY\n B GGY\n G BBG\n GGGBB\n YRBGG',
                '      \n      \n      \n      \n      \n    R \n   YR \n   RGY\n B GGY\n G BBG\n GGGBB\n YRBGG',
                '      \n      \n      \n      \n    R \n    R \n   YRB\n   RGY\n B GGY\n G BBG\n GGGBB\n YRBGG',
                '      \n      \n      \n      \n   BR \n   YR \n   YRB\n   RGY\n B GGY\n G BBG\n GGGBB\n YRBGG',
                '      \n      \n      \n      \n   BR \n   YR \n   YRB\n B RGY\n B GGY\n G BBG\n GGGBB\nYYRBGG',
                '      \n      \n    b \n    Y \n   BR \n   YR \n   YRB\n B RGY\n B GGY\n G BBG\n GGGBB\nYYRBGG',
                '      \n      \n    b \n    Y \n   BR \n   YR \n   YRB\n B RGY\n BGGGY\n GBBBG\n GGGBB\nYYRBGG',
                '      \n      \n    b \n    Y \n   BR \n   YR \n  RYRB\n BRRGY\n BGGGY\n GBBBG\n GGGBB\nYYRBGG',
                '      \n      \n      \n      \n      \n    Y \n    R \n  RYRG\n  RYRY\n GGRGY\n GGGGG\nYYRGGG',
                '      \n      \n      \n      \n      \n  B Y \n  R R \n  RYRG\n  RYRY\n GGRGY\n GGGGG\nYYRGGG',
                '      \n      \n      \n      \n  B   \n  B Y \n  R R \n  RYRG\n GRYRY\n GGRGY\n GGGGG\nYYRGGG',
                '      \n      \n      \n    y \n  B B \n  B Y \n  R R \n  RYRG\n GRYRY\n GGRGY\n GGGGG\nYYRGGG',
                '      \n      \n      \n    y \n    B \n    Y \n    R \n  BYRG\n GBYRY\n GGRGY\nBGGGGG\nYYRGGG',
                '      \n      \n      \n    y \n    B \n  B Y \n  Y R \n  BYRG\n GBYRY\n GGRGY\nBGGGGG\nYYRGGG',
                '      \n      \n      \n    y \n  R B \n  B Y \n  Y R \n GBYRG\n GBYRY\n GGRGY\nBGGGGG\nYYRGGG',
                '      \n      \n      \n      \n  B   \n  B   \n  Y y \n GB BG\n GBYYY\n GGYGY\nBGGGGG\nYY GGG',
                '      \n      \n      \n  Y   \n  B   \n  B   \n rY y \n GB BG\n GBYYY\n GGYGY\nBGGGGG\nYY GGG',
                '      \n      \n      \n  Y   \n  B   \n BB   \n rY y \n GB BG\n GBYYY\nRGGYGY\nBGGGGG\nYY GGG',
                '      \n      \n  R   \n  Y   \n BB   \n BB   \n rY y \n GB BG\n GBYYY\nRGGYGY\nBGGGGG\nYY GGG',
                '      \n      \n RR   \n RY   \n BB   \n BB   \n rY y \n GB BG\n GBYYY\nRGGYGY\nBGGGGG\nYY GGG',
                '      \n Y    \n RR   \n RY   \n BB   \n BB   \n rY y \n GB BG\nGGBYYY\nRGGYGY\nBGGGGG\nYY GGG'],
            [
                '      \n      \n      \n      \n      \n      \n      \n      \n      \n      \nR     \nR     ',
                '      \n      \n      \n      \n      \n      \n      \n      \nR     \nR     \nR     \nR     ',
                '      \n      \n      \n      \n      \n      \nG     \nG     \nR     \nR     \nR     \nR     ',
                '      \n      \n      \n      \nR     \nR     \nG     \nG     \nR     \nR     \nR     \nR     ',
                '      \n      \n      \n      \nR     \nR     \nG     \nG     \nR     \nR     \nRY    \nRY    ',
                '      \n      \n      \n      \nR     \nR     \nG     \nG     \nRY    \nRY    \nRY    \nRY    ',
                '      \n      \n      \n      \nR     \nR     \nGB    \nGY    \nRY    \nRY    \nRY    \nRY    ',
                '      \n      \n      \n      \nR     \nR     \nGB    \nGY    \nRY    \nRY    \nRYB   \nRYG   ',
                '      \n      \n      \n      \nR     \nR     \nGB    \nGY    \nRYY   \nRYY   \nRYB   \nRYG   ',
                '      \n      \n      \n      \nRR    \nRR    \nGB    \nGY    \nRYY   \nRYY   \nRYB   \nRYG   ',
                '      \n      \n      \n      \nRR    \nRR    \nGBB   \nGYR   \nRYY   \nRYY   \nRYB   \nRYG   ',
                '      \n      \n      \n      \nRRb   \nRRY   \nGBB   \nGYR   \nRYY   \nRYY   \nRYB   \nRYG   ',
                '      \n      \n      \n      \nRRb   \nRRY   \nGBB   \nGYR   \nRYY   \nRYY   \nRYBG  \nRYGG  ',
                '      \n      \n      \n      \nRRb   \nRRY   \nGBB   \nGYR   \nRYY   \nRYY   \nRYBGB \nRYGGB ',
                '      \n      \n      \n      \nRRb   \nRRY   \nGBB   \nGYR   \nRYY G \nRYY G \nRYBGB \nRYGGB ',
                '      \n      \n      \n      \nRRb   \nRRY   \nGBB   \nGYR   \nRYYGG \nRYYGG \nRYBGB \nRYGGB ',
                '      \n      \n      \n      \nRRb   \nRRY   \nGBB   \nGYR   \nRYYGG \nRYYGG \nRYBGBB\nRYGGBG',
                '      \n      \n      \n      \nRRb   \nRRY   \nGBBB  \nGYRR  \nRYYGG \nRYYGG \nRYBGBB\nRYGGBG',
                '      \n      \n      \n      \nRRb   \nRRY   \nGBBB  \nGYRRY \nRYYGG \nRYYGGB\nRYBGBB\nRYGGBG',
                '      \n      \n      \n      \nRRb   \nRRY   \nGBBB  \nGYRRYB\nRYYGGB\nRYYGGB\nRYBGBB\nRYGGBG',
                '      \n      \n      \n      \nRRb   \nRRY  B\nGBBB B\nGYRRYB\nRYYGGB\nRYYGGB\nRYBGBB\nRYGGBG',
                '      \n      \n      \n      \nRRb   \nRRY yB\nGBBBBB\nGYRRYB\nRYYGGB\nRYYGGB\nRYBGBB\nRYGGBG',
                '      \n      \n      \n      \nRRb g \nRRYByB\nGBBBBB\nGYRRYB\nRYYGGB\nRYYGGB\nRYBGBB\nRYGGBG',
                '      \n      \n      \n   R  \nRRbRg \nRRYByB\nGBBBBB\nGYRRYB\nRYYGGB\nRYYGGB\nRYBGBB\nRYGGBG',
                '      \n      \n      \n      \nRR    \nRR    \nG Y   \nGYR   \nRYY   \nRYY   \nRY    \nRYBR G']
        ]
        sol_set = [
            '      \n      \n      \n      \n      \n      \n      \n      \n      \n    R \n R  YR\nRR  RB',
            '      \n      \n      \n      \n      \n      \n      \n    R \n  GGY \n  GGYB\nGGGRYB\nGRRBBB',
            '      \n      \n      \nGG    \nRY    \nRRYB  \nRRRB  \nR RgY \nR RRG \nRRRRG \nRGGRGB\nRGRGGY',
            '      \n      \n      \n      \n      \n      \n      \n     B\n    RR\n  b gy\n  R BB\nBBYYRB',
            '      \n      \n      \n      \n YG   \nRRR   \nRRR   \nRRRR  \nRRRR  \nRRRR  \n   RRR\n  GRRR',
            '      \n      \n      \n      \n      \n      \nR  Y  \nR  RR \nR  GG \nR  GG \nR  G  \nRRGGGG',
            '      \n      \n      \n      \n      \n R    \n Y    \nYY    \nYY G  \n YGGG \nYYGGYG\nYY GBG',
            '      \n      \n      \n      \n      \n      \n      \n      \n  G   \n GG Y \n GG R \nYR RRR',
            '      \n Y    \n RR   \n RY   \n BB   \n BB   \n rY y \n GB BG\nGGBYYY\nRGGYGY\nBGGGGG\nYY GGG',
            '      \n      \n      \n      \nRR    \nRR    \nG Y   \nGYR   \nRYY   \nRYY   \nRY    \nRYBR G'
        ]

        for i,x in enumerate(fixed_tests):
            ver_funk(puzzle_fighter(x),[sol_set[i],[[fixed_tests[i][c],fixed_test_states[i][c]] for c in range(len(fixed_test_states[i]))]])
        
        # END FIXED TESTS

        
        
        
    
# 200 RANDOM TESTS (w/ B4B's tests randomly integrated)
@test.describe('200 RANDOM TESTS')
def _():

    # REFERENCE SOLUTION
    def funk(ar):
        MN = [[-1,0],[0,1],[1,0],[0,-1]]
        tome = [['' for c in range(6)] for i in range(13)]
        pg_data = {}
        peak = 12
        pgn = 0
        states_list = []
        def game_state(): return '\n'.join([''.join([v[0] if v else ' ' for v in x]) for x in tome][:12])
        def check_bounds(x): return x[0] >= 0 and x[0] < 12 and x[1] >= 0 and x[1] < 6
        def find_index(r,fn):
            for i,v in enumerate(r):
                if fn(v):
                    return i
        def refresh():
            nonlocal tome,peak
            crashG = []
            i = 10
            for i in range(10,peak-1,-1):
                for j in range(6):
                    z = tome[i][j]
                    if z and tome[i+1][j] == '':
                        if len(z) > 1:
                            n = z[1:]
                            p = pg_data[n]
                            h = p[2][0] - p[1][0]
                            j2 = p[1][1]
                            k = p[2][1]
                            i2 = i + 1
                            while all([v == '' for v in tome[i2][j2:k]]): i2 += 1
                            if i2 == i + 1:
                                j = k - 1
                                continue
                            i3 = p[1][0]
                            i2 -= 1
                            while i3 < i2 and i3 != p[2][0]:
                                if len(tome[i2][p[1][1]]): break
                                for j2 in range(p[1][1],k):
                                    tome[i3][j2] = ''
                                    tome[i2][j2] = z
                                i2 -= 1
                                i3 += 1
                            p[1][0] = i2 + 1 if i3 == p[2][0] else i3
                            p[2][0] = p[1][0] + h
                        else:
                            k = i
                            i2 = i + 1
                            while tome[i2][j] == '': i2 += 1
                            i2 -= 1
                            while k >= peak and len(tome[k][j]) < 2:
                                if tome[k][j]:
                                    tome[i2][j] = tome[k][j]
                                    tome[k][j] = ''
                                    i2 -= 1
                                k -= 1
            for i in range(i,12):
                if any(tome[i]):
                    peak = i
                    break
            for i in range(peak,12):
                for c,v in enumerate(tome[i]):
                    if v and v in 'rgby':
                        crashG.append([[i,c],v])
            return crashG if len(crashG) else False

        def crash_proc(x,y,clr):
            nonlocal tome,pg_data
            def scout(x1,y1,x2,y2):
                x1,y1 = x1 + x2,y1 + y2
                return [x1,y1] if check_bounds([x1,y1]) and len(tome[x1][y1]) and tome[x1][y1][0] in clR else None
            clR = clr + clr.upper()
            r = []
            tr = []
            for v in MN:
                z = scout(v[0],v[1],x,y)
                if z: r.append(z)
            if len(r) == 0: return False
            tome[x][y] = ''
            while len(r):
                for xx,yy in r:
                    if len(tome[xx][yy]) > 1 and tome[xx][yy][1:] in pg_data:
                        del pg_data[tome[xx][yy][1:]]
                    if tome[xx][yy] == '': continue
                    tome[xx][yy] = ''
                    for v in MN:
                        z = scout(v[0],v[1],xx,yy)
                        if z: tr.append(z)
                r,tr = tr,[]
            return True
        def pg_rangecheck(r):
            rng,xy,end,inc,clr,pgr = r
            if any([pg_data[v] and pg_data[v][1][xy] < rng[0] or pg_data[v][2][xy] > rng[1] for v in pgr]):
                return False
            scan_rng = end
            for v in pgr:
                if inc: scan_rng = max(pg_data[v][2][xy^1],scan_rng)
                else: scan_rng = min(pg_data[v][1][xy^1],scan_rng)
            if xy:
                if inc: ia,iz,ja,jz = end,scan_rng,rng[0],rng[1]
                else: ia,iz,ja,jz = scan_rng,end,rng[0],rng[1]
            else:
                if inc: ia,iz,ja,jz = rng[0],rng[1],end,scan_rng
                else: ia,iz,ja,jz = rng[0],rng[1],scan_rng,end
            for i in range(ia,iz):
                for j in range(ja,jz):
                    v = tome[i][j]
                    if not v or v[0] != clr: return False
                    if len(v) > 1 and not v[1:] in pgr:
                        pgr.append(v[1:])
                        if not pg_rangecheck(r): return False
            return pgr
        def pg_update():
            nonlocal tome,peak,pgn,pg_data
            #form new power gems
            for i in range(peak,12):
                for j in range(6):
                    z = tome[i][j]
                    if not z or len(z) > 1: continue
                    if all([check_bounds(x) for x in [[i,j+1],[i+1,j],[i+1,j+1]]]) and all([tome[x][y] == z for x,y in [[i,j+1],[i+1,j],[i+1,j+1]]]):
                        pgn += 1
                        pg_data[str(pgn)] = [z,[i,j]]
                        i2 = i + 1
                        j2 = j + 1
                        while j2 >= 0 and j2 < 6 and tome[i][j2] == z and tome[i2][j2] == z: j2 += 1
                        i2 += 1
                        while all([v == z for v in tome[i2][j:j2]]): i2 += 1
                        for vi in range(i,i2):
                            for vj in range(j,j2):
                                tome[vi][vj] += str(pgn)
                        pg_data[str(pgn)].append([i2,j2])
            for n in list(pg_data.keys()):
                if n not in pg_data: continue
                z0,[i,j],[i2,j2] = pg_data[n]
                nv = '{}{}'.format(z0,n)
                for q,v in enumerate([[-1,-1],[1,6]]):
                    inc,bnd = v
                    if q: vi,vj = i,j2-1
                    else: vi,vj = i,j
                    break_outer = False
                    vj += inc
                    while vj != bnd and tome[i][vj].startswith(z0):
                        while vi != i2 and tome[vi][vj].startswith(z0):
                            if len(tome[vi][vj]) > 1:
                                pg_set = [tome[vi][vj][1:]]
                                tpg = pg_data[pg_set[0]]
                                merge = pg_rangecheck([[i,i2],0,vj,1,z0,pg_set]) if q else pg_rangecheck([[i,i2],0,vj+1,0,z0,pg_set])
                                if merge:
                                    for v in merge:
                                        vj = max(pg_data[v][2][1]-1,vj) if q else min(pg_data[v][1][1],vj)
                                        del pg_data[v]
                                    vi = i2
                                    break
                                else:
                                    break_outer = True
                                    break
                            vi += 1
                        if break_outer or vi != i2: break
                        vi = i
                        vj += inc
                    pg_data[n][q+1][1] = vj + (q^1)
                    if q: j2 = pg_data[n][2][1]
                    else: j = pg_data[n][1][1]
                [pi,pj],[qi,qj] = pg_data[n][1:]
                jj = pj
                while pi < qi:
                    jj = pj
                    while jj < qj:
                        tome[pi][jj] = nv
                        jj += 1
                    pi += 1
                for q,v in enumerate([[-1,-1],[1,12]]):
                    inc,bnd = v
                    if q: vi,vj = i2-1,j
                    else: vi,vj = i,j
                    break_outer = False
                    vi += inc
                    while vi != bnd and tome[vi][j].startswith(z0):
                        while vj != j2 and tome[vi][vj].startswith(z0):
                            if len(tome[vi][vj]) > 1:
                                pg_set = [tome[vi][vj][1:]]
                                tpg = pg_data[pg_set[0]]
                                merge = pg_rangecheck([[j,j2],1,vi,1,z0,pg_set]) if q else pg_rangecheck([[j,j2],1,vi+1,0,z0,pg_set])
                                if merge:
                                    for i,v in enumerate(merge):
                                        vi = max(pg_data[v][2][0]-1,vi) if q else min(pg_data[v][1][0],vi)
                                        del pg_data[v]
                                    vj = j2
                                    break
                                else:
                                    break_outer = True
                                    break
                            vj += 1
                        if break_outer or vj != j2: break
                        vj = j
                        vi += inc
                    pg_data[n][q+1][0] = vi + (q^1)
                    if q: i2 = pg_data[n][2][0]
                    else: i = pg_data[n][1][0]
                [pi,pj],[qi,qj] = pg_data[n][1:]
                jj = pj
                while pi < qi:
                    jj = pj
                    while jj < qj:
                        tome[pi][jj] = nv
                        jj += 1
                    pi += 1
            return
        tome[12] = [0]*6
        for pair,s in ar:
            y = 3
            tail = 2
            gemcrash = False
            for vn in s:
                if vn == 'L': y -= 1
                elif vn == 'R': y += 1
                elif vn == 'A': tail = (3 + tail) % 4
                elif vn == 'B': tail = (tail + 1) % 4
                else: raise ValueError('invalid instruction: "{}"'.format(vn))
                if y <= 0: y = 1 if tail == 3 else 0
                elif y >= 5: y = 4 if tail == 1 else 5
            head_xy = [find_index(tome,lambda v: v[y] != '')-1,y]
            if tail == 0: tail_xy = [head_xy[0]-1,y]
            elif tail == 1: tail_xy = [find_index(tome,lambda v:v[y+1] != '')-1,y+1]
            elif tail == 2:
                tail_xy = [head_xy[0],y]
                head_xy[0] -= 1
            elif tail == 3: tail_xy = [find_index(tome,lambda v:v[y-1] != '')-1,y-1]
            if any(v[0] < 0 for v in [head_xy,tail_xy]): return [game_state(),states_list]
            for c,v in enumerate([head_xy,tail_xy]):
                tome[v[0]][v[1]] = pair[c]
                peak = min(v[0],peak)
            if '0' in pair:
                for i,v in enumerate([head_xy,tail_xy]):
                    x,y = v
                    if pair[i] == '0':
                        tome[x][y] = ''
                        gemcrash = True
                        if x == 11 or tome[x+1][y] == '': continue
                        crash_color = tome[x+1][y][0].upper()
                        for j in range(peak,12):
                            for c,v1 in enumerate(tome[j]):
                                if v1 and v1[0].upper() == crash_color:
                                    if len(v1) > 1 and v1[1:] in pg_data: del pg_data[v1[1:]]
                                    tome[j][c] = ''
            for c,v in enumerate([head_xy,tail_xy]):
                if pair[c] in 'rgby':
                    if crash_proc(v[0],v[1],pair[c]): gemcrash = True
                else:
                    for xx,yy in list(filter(lambda g: check_bounds(g) and tome[g[0]][g[1]] and tome[g[0]][g[1]] in 'rgby',[[xq+v[0],yq+v[1]] for xq,yq in MN])):
                        gemcrash = crash_proc(xx,yy,tome[xx][yy]) or gemcrash
            pg_update()
            while gemcrash:
                gemcrash = refresh()
                if gemcrash:
                    for v in gemcrash:
                        if crash_proc(v[0][0],v[0][1],v[1]): gemcrash = True
                if type(gemcrash) != bool: gemcrash = False
                pg_update()
            states_list.append([[pair,s],game_state()])
        return [game_state(),states_list]

    
    

    """
    ***************************
      "Fixed test randomizer"
                XD
    ***************************
    """




    nope=lambda x:x
    yes=lambda: rand(2)

    def shuf(lst):
        shuffle(lst)
        return lst


    # Data to create some specific edge cases (will be randomized in some ways, baseed on this)
    REARRANGED = [
        [ # b4b_smallset 1
            (shuf, [['RR',''],['RR','L'],['BB','R'],['BB','LL']]),
            (shuf, [['GG',''],['GG','L'],['GG','LL'],['GG','R']]),
            (nope, [['0B','LLL']]),
            (shuf, [['RG','AALL'],['By','BBABRRLR'],['GR','AAABLLRLL']]),
        ],
        [ # b4b_smallset 2
            (nope, [['RR',''],['RR', 'L'],['RR', 'B'],['RR', 'B'],['BB', 'LL'],['RR', 'LL'],['Bb', 'LLL']]),
            (shuf, [['GY','RLRLL'],['BY','BLLLR'],['GR','AAL']]),
        ],
        [ # b4b_smallset 3
            (shuf, [['RY',''],['RY','L'],['GG','BRR']]),
            (shuf, [['RR','R'],['BB','B']]),
            (nope, [['RR','B'],['BB','B'],['RR','B'],['RR','B'],['0B','LL'],['Gg','RR']]),
        ],
        [ # b4b_fixed_test
            (shuf, [['bY','B'],['RG','RR']]),
            (nope, [['yG','BBB']]),
            (shuf, [['GG','ARR'],['GY','']]),
            (shuf, [['Br','RR'],['YR','BBBL']]),
            (nope, [['RY','RR'],['GR','RRR'],['GY','B'],['RR','A'],['RB','ALLL'],['Yb','AAALL'],['rb','AALL'],['R0','ARR']]),
            (shuf, [['RY','AAARRR'],['GY','AAALLL']]),
            (nope, [['YB','BRR'],['GR','AAAR'],['YY','BBBR'],['GB','R'],['GG','AA'],['RY','AAAL']]),
            (shuf, [['RY','BR'],['BR','ALLL'],['RY','AARR']]),
        ],
        [ # complex area of single gems built on the fly, does NOT result in a power gem
            (shuf, [['YY','LLL'],['YY','LL'],['BB','L'],['YY',''],['YY','R'],['YY','RR']]),
            (shuf, [['YR','LLL'],['YR','LL'],['RB','AL']]),
            (shuf, [['YR',''],['RB','R'],['RB','RR'],['RB','AAL']]),
            (nope, [['R0','LLL']]),
        ],
        [# complex area of single gems built on the fly, SHOULD result in a power gem
            (shuf, [['YY','LLL'],['YY','LL'],['BB','L'],['YY',''],['YY','R'],['YY','RR']]),
            (shuf, [['YR','LLL'],['RR','LL'],['RB','AL']]),
            (shuf, [['YR',''],['RB','R'],['RB','RR'],['RB','AAL']]),
            (nope, [['R0','LLL']]),
        ],
        [ # '00' landing vertically: only one has actually an effect
            (shuf, [['YB','LLL'],['RY','LL'],['RR','L'],['BR',''],['YR','R'],['YR','RR']]),
            (nope, [['00','R']]),
        ],
        [ # '00' landing horizontally on two identical colors
            (shuf, [['YB','LLL'],['RY','LL'],['RR','L'],['RR',''],['YR','R'],['YR','RR']]),
            (nope, [['00','A']]),
        ],
        [ # '00' landing horizontally on two different colors
            (shuf, [['YB','LLL'],['RY','LL'],['RR','L'],['BR',''],['YR','R'],['YR','RR']]),
            (nope, [['00','A']]),
        ],
        [ # '00' landing horizontally on two different colors, one being a crash gem
            (shuf, [['YB','LLL'],['RY','LL'],['RR','L'],['bR',''],['YR','R'],['YR','RR']]),
            (nope, [['00','A']]),
        ],
        [ # user not checking outside of the board after a rainbow gem exploded, searching for something to drop later
            (nope, [['BB','LLL'],['BB','LLL'],['BB','LLL'],['BB','LLL'],['BB','LLL'],['BB','LLL'],['BB',''],['BB',''],['BB',''],['BB',''],['BB',''],['0B','']]),
        ],
        [ # massive cascade of explosions/drops, resulting in a power gem that should finally fall correctly
            (nope, [['bY','ALL'],['YY','BBBL']]),
            (shuf, [['YB','R'],['BR','LL'],['yg','AL'],['BY','RR']]),
            (nope, [['RR','AA'],['BB','R'],['RR','AR'],['BR','AAA'],['GB','AAA'],['RG','AA']]),
            (shuf, [['YR','BBRRR'],['YY','BBLLL'],['GB','L']]),
            (shuf, [['GB','AAL'],['RR','RR'],['bY','AAAR']]),
            (nope, [['0R','A'],['BY','L'],['yR','AAR'],['RY','AAAR'],['RY','BLL'],['RB','BBB'],['RY','LL'],['G0','LLL'],['B0','']]),
            (shuf, [['RG','LLL'],['YG','BBB']]),
        ],
        [ # powa expansion specific tests (jagged power gems, on long "shots")
            (nope, [['RR','BLL']]),
            (shuf, [['BB','BLL'],['BB','L'],['BB','A'],['GG','RR']]),
            (shuf, [['yR','L'],['YR','RR'],['RR','A']]),
            (nope, [['RR','A'],['YY','A'],['YY','A'],['RR','A']]),
            (shuf, [['RY','RR'],['RR','LLL'],['RR','LL']]),
            (nope, [['Ry','L'],['0B','LLL']]),
        ],
        [ # "non dropped" pairs (because gems already just below when entering the drop process) should still be seen to create powaGems
            (shuf, [['GG','AAL'],['GR',''],['GG','AAR']]),
            (nope, [['Rb','BRRR'],['Rg','AARRR'],['RG','AAARR'],['0Y','BR'],['RB','BL'],['RR','BBBL']]),
            (shuf, [['YY','RRR'],['YR','LL'],['GY','B'],['YY','R']]),
            (nope, [['Rg','BLL'],['BR','R'],['BB','AALL'],['GY','R'],['yR','AAAR'],['RB','AAL'],['BB','AA'],['RG','ALL'],['GG','AALL'],['YB','BB'],['gg','LLL'],['GY','LLL'],['BG','A'],['YG','AAAR'],['RB','LL'],['GG','A'],['YG','R'],['bY','AL'],['GY','AAL'],['YY','BRRR'],['YY','AARR'],['RG','RRR'],['GR','RRR'],['RB','BBB'],['BG','B'],['gr','AL'],['RG','BBBRR'],['gy','BL'],['YR','BBRRR'],['RB','L']]),
        ],
        [ # troubles due to the first '00' pair, apparently
            (shuf, [['YB','BBLLL'],['YR','B'],['gG','RRR'],['Ry','BBRRR']]),
            (shuf, [['YY','BBBL'],['YG','BBBRR']]),
            (shuf, [['YY','AARR'],['GG','BBBL'],['GR','R']]),
            (nope, [['00','AAL'],['GG',''],['GY','BBBLL'],['RR','BB'],['RR','AALL'],['GB','LL'],['00','AAARRR']]),
        ],
        [ # solution creates additionnal R simple gem to make powa at step 23
            (shuf, [['gR','AAAL'],['BB','AR']]),
            (shuf, [['bB','AAARRR'],['Ry','AALL']]),
            (nope, [['B0','BBBRRR']]),# rainbow crashing on the floor: check no effect
            (shuf, [['YR','BRRR'],['GR','LLL'],['GB','AA']]),
            (nope, [['RB','BRRR'],['BG',''],['RR','BL'],['RY','BL'],['GY','BBB'],['YY','LL'],['YG','R'],['YY','LLL'],['RG','AA'],['YG','BBB'],['Ry','AAAL'],['RR','BBBLL'],['RY','BLL'],['RR','BBLL'],['YG',''],['RR','BBL'],['BG','AAALLL'],['BG','LL'],['YY','BBR'],['GB','L'],['GB','R'],['BR','BB'],['RR','BBBLL'],['yR','BBBR'],['BY','RR'],['GY','AALL']]),
            (shuf, [['yg','AAARRR'],['Bg','AAA'],['RG','BB'],['RG','A'],['RR',''],['YG','']]), # game stopped at the step before, do not care about the order
        ],
        [ # solution creates additionnal 4 gems simple gems (I believe) to make powa at step 19
            (nope, [['RR','LL']]),
            (shuf, [['GY','AAALL'],['RR','B']]),
            (nope, [['BR','AAAL'],['Gr','BRRR'],['RR','LLL'],['YY','BBBR'],['BY','A'],['GY','A'],['GG','BRR'],['bR','BBBLLL'],['GG','AAAR'],['BR','AAAL'],['YB','AA'],['YY','BBLLL'],['YY','AALL'],['BG','A'],['RR','BR'],['YY','BBLLL'],['YY','LL'],['RB','AARR'],['GR','LLL'],['RY','AARR'],['BR',''],['YY','A'],['YR','BR']]),
            (shuf, [['Rg','AARR'],['BG','R'],['gR','BBBLL']]),
            (nope, [['YY','BB']]), # end of game
            (shuf, [['YY','AAA'],['0y','BBR'],['RG','ALL'],['00','LAALBR'],['g0','LLRRABR']]),
        ],
        [ # new variation of the previous bug, which showes that your code is actually replacing existing gems while expanding up:
        # at step 11: replace the RR vertical pair (5,3 and 6,3) with a 2x2 Y powaGem at (5,3 -> 6,4). The Y0 was landing on (7,4) and (7,5).
            (nope, [['YY','BR'],['YY','AAAR'],['YG',''],['GG','BBBRRR']]),
            (shuf, [['BR','BBRRR'],['RB','BBBLLL'],['YB','BBR'],['YR','AA']]),
            (nope, [['BR','BR'],['bG','RRR'],['RB','LLL'],['0Y','AAARRR'],['BG','AARRR'],['RR','BRRR'],['GY','B'],['YY','AAALL'],['GR','BL'],['YG','AAALL']]),
            (shuf, [['YR','LL'],['GB','RR'],['RR','']]),
        ],
        [
            (shuf, [['BB','LLL'],['BB','LL'],['GG','L'],['GG',''],['GG','AR']]),
            (shuf, [['BB','AR'],['RR','B']]),
            (nope, [['RR','B'],['RR','B'],['RR','B'],['RR','BLL'],['RR','BLL'],['RR','BLL'],['RR','AR'],['YY','AR'],['RR','AR'],['GG','AR'],['RR','AR'],['YY','AR'],['RR','AR'],['YY','B'],['YY','B'],['RR','B'],['YY','BLL'],['RR','BLL'],['RR','BLL'],['YY','BLL'],['B0','LLL'],['Y0','LLL']]),
            (shuf, [['RR','ALLL'], ['RG','ALL'], ['RR','B'], ['YB','RR']]),
        ],
        [
            (shuf, [['YG','BBRRR'],['BY','R'],['YG',''],['GY','L']]),
            (nope, [['RY','A'],['YY','BBBLL']]),
            (shuf, [['YG','AA'],['Gg','AALLL'],['GG','']]),
            (nope, [['GB','B'],['YB','BBRR'],['GR','BL'],['RR','BL'],['GY',''],['YR','B'],['GR','AAARRR'],['YY','ALL'],['GY','AAAR'],['GB','BBBRR'],['GG','R'],['BG','BL'],['RG',''],['RG',''],['YR','BBBRRR'],['GG','BBRRR'],['YY','R'],['RB','AAARR'],['YB','BL'],['GG','AAARRR']]),
            # game ended somewhere in the previous sequence...
            (shuf, [['RY','BLL'],['BB','BBL'],['YR','AAA'],['0R','ARRR'],['BG','L'],['RB','AAA'],['RB','AA'],['GB','BBBL'],['YY',''],['RR','BBLL']]),
        ],
        [
            (shuf, [['BY','BRR'],['ry','L'],['BG','BBBLLL']]),
            (nope, [['YY','AAARR']]),
            (shuf, [['RY','RRR'],['YY','R']]),
            (shuf, [['YR','AR'],['GR','AL']]),
            (shuf, [['BB','LLL'],['GY',''],['BG','L'],['GG','AAR'],['GG','RRR']]),
            (nope, [['RY','R'],['0Y','BBBRR'],['Bb','ALLL'],['GR',''],['R0','BBLLL'],['R0','AAALLL'],['GB','AAARR'],['BB','A'],['YB','B'],['GB','RRR'],['RB','AARRR'],['RB','AAL'],['RG','A'],['GY','AAAR'],['RR','AAAL'],['RG','L'],['GG','LL'],['GG','ARRR'],['BG','AALLL'],['YB','L'],['RG',''],['YG','AAA'],['GR','BBB']]),
            (shuf, [['RB','AA'],['ry','BRRR']]), # end of game at next move.
            (nope, [['YY','AA'],['RB','B'],['YB','RRR'],['BR','BRRR'],['RR','AAAL'],['RG',''],['RG','AARR'],['GB','AAAR'],['RR','RRR'],['RY','B'],['RG','BR'],['RG','AAALL'],['YR','RR'],['YB','BBBLLL'],['GB','AA'],['BG','BBBRRR']]),
            # out of game:
            (shuf, [['YB','AAALLL'],['BY','A'],['YG','BBB'],['GY',''],['GY','BRR'],['Rr','BL'],['RG','L'],['RY','AAA'],['BY','AR'],['RR','AALL'],['YG','AAAR'],['YR','BBR'],['YB','AAARRR'],['YG','BB']]),
        ],
    ]

    NEW_ONES_BY_DOC_2019_07_31 = [
        [
            (shuf, [['rB','A'],['BR','LL']]),
            (shuf, [['RY','BRRR'],['RB','AAALLL'],['BY','B']]),
            (shuf, [['Yb','AAL'],['RB','BBBLLL']]),
            (shuf, [['GY','LLL'],['BY','BB']]),
            (nope, [['YY','BBB'],['RR','BR']]),
            (shuf, [['GR','BBB'],['Bb','ALL'],['YY','AARRR']]),
            (nope, [['gG','BL']]),
            (shuf, [['GY','L'],['Rr','AAALLL'],['Yy','BRRR']]),
            (shuf, [['GB','BBLL'],['YB','AAA'],['YB','AALLL']]),
            (shuf, [['BY','AAALLL'],['BB','RR'],['G0','A']]),
            (nope, [['RG','AAR'],['RB','RR'],['BR','BL'],['yY','RRR']]),
            (shuf, [['YG','LLL'],['BR','BB'],['BY','AR'],['BG','L']]),
            (nope, [['GB','A'],['bG','AAR']]),
            (shuf, [['BB',''],['YB','AAAL'],['Bg','LLL']]),
            (shuf, [['BY','BR'],['RG','AALLL']]),
            (shuf, [['BG','BRRR'],['YB','AAA']]),
            (nope, [['BY','LLL']]), # end of game
            (shuf, [['GR','AAR'],['GY','RRR'],['RR','BBBRRR'],['YB','RRR'],['YR','BRRR'],['G0','AAL'],['GY','AAL'],['YY','BBBRRR'],['YG','ALLL'],['BR','AALLL'],['RG','BBLL'],['RB','LL'],['RY','RR'],['Bg','AAA'],['BB','BBBL'],['RY','AAA'],['RG','BBBRR'],['BB','BL'],['GG','B'],['RG','BLLL'],['YG','RRR'],['yb','B'],['YB','A'],['RR','AAA'],['YG','BLL']]),
        ],
        [
            (shuf, [['GR','AALL'],['RR','B'],['YY','R'],['YB','BBRR']]),
            (shuf, [['BG','AA'],['YB','ALLL'],['YB','BBBRR']]),
            (shuf, [['Rr','BBRRR'],['BB','BB'],['GR','BBBLLL']]),
            (nope, [['YG','RR'],['yr','R'],['RR',''],['YB',''],['YR','B']]),
            (shuf, [['YB','AAAL'],['GB','BRRR']]),
            (nope, [['B0','RRR']]),
            (shuf, [['RR','BBL'],['Br','BBRR']]),
            (nope, [['GB','L']]),
            (shuf, [['RB','BL'],['RB','BBR']]),
            (nope, [['BG','AR']]),
            (shuf, [['RB','BBRRR'],['GB','A'],['rY','BBLL']]),
            (nope, [['B0','LL']]),
            (shuf, [['YG','BBB'],['BY','BBBLLL']]),
            (shuf, [['YR',''],['RY','AAR'],['YB','RR'],['Bb','BLLL']]),
            (nope, [['GB','B'],['YB','AAL']]),
            (shuf, [['GB','B'],['BR','R']]),
            (nope, [['YY','AAARR'],['BB','BBBR'],['YG','BR']]),
            (shuf, [['GY','RR'],['RY','BBLL'],['GY','A']]),
            (shuf, [['YB','AAA'],['BR','AARR']]),
            (nope, [['RR','BBL'],['GB','RRR']]),# end of game
            (shuf, [['BB',''],['GB','BBBL'],['BB','AAARR'],['Yr',''],['Gr','BLLL'],['rY','LL'],['GY','BB'],['BR','ALLL'],['GB',''],['YY','AAAL'],['GG','L'],['YG','AAA'],['BR','BBR'],['RB','BBRR']]),
        ],
        [
            (shuf, [['YR','BBBRR'],['YB','AAL']]),
            (nope, [['YB','ALL']]),
            (shuf, [['RG','BLLL'],['YY','']]),
            (shuf, [['RG','AA'],['RY','ALL'],['BY','AR']]),
            (shuf, [['RY','AAAL'],['BB','BBRR']]),
            (nope, [['YB','AAL'],['BY','BBB'],['GY','AAARRR'],['YB','']]),
            (shuf, [['Yb','BBR'],['YG','BLL']]),
            (nope, [['YY','BR'],['YB','B'],['R0','BL']]),
            (shuf, [['RG','AAALL'],['GG','']]),
            (nope, [['GR','LLL'],['GG','AAAL']]),
            (shuf, [['BG','BBR'],['BB','BB'],['YY','AAALL']]),
            (shuf, [['GB','BBBLLL'],['GB','AAL']]),
            (nope, [['RB','AAALLL'],['BG','BBL'],['GB','BR'],['RR','AL'],['0B','AA'],['YG','RRR'],['B0','BB']]),
            (shuf, [['RB','BBBLL'],['YG','BBB'],['GR','LLL']]),
            (nope, [['BB','LL']]),
            (shuf, [['YR','LL'],['Ry','AAL']]),
            (shuf, [['BY','AR'],['BY','BBBLL']]),
            (nope, [['yR','AAR']]),
        ],
    ]


    TABLE_SYM = str.maketrans('RLAB','LRBA')
    GEMS      = 'RGBY'
    GEMS_CRH  = GEMS+GEMS.swapcase()
    PERM      = list(GEMS)
    RANDOMIZE = True
    WITH_SHUF = True

    def symmetrizer(moves):
        m = moves.translate(TABLE_SYM)
        iR = m.find('R')
        if iR<0: iR = rand(len(m) or 1)
        return m[:iR]+'L'+m[iR:]

    def convertFixedDataToRandomizedInput(data):
        shuffle(PERM)
        permuted  = ''.join(PERM)+''.join(PERM).swapcase()
        permTable = str.maketrans(GEMS_CRH, permuted) if RANDOMIZE else str.maketrans('','')
        sym       = symmetrizer if RANDOMIZE and yes() else nope
        chained   = list(chain.from_iterable( f(lst) if WITH_SHUF else lst for f,lst in data ))
        return [ [pair.translate(permTable), sym(m)] for pair,m in chained ]


    # Additional edge cases by @Blind4Basics (added 2019.07.30)
    B4B_edge_cases_20190730 = list(map(convertFixedDataToRandomizedInput, REARRANGED + NEW_ONES_BY_DOC_2019_07_31))



    '''
    Unrandomized versions of the different test, plus the shorter versions ("beginning of tests used to fix bugs"):
    ---------------------------------------------------------------------------------------------------------------

    # Additional edge cases by @Blind4Basics (added 2019.07.30)
    B4B_edge_cases_20190730 = [
        # older edge case (orig. b4b_fixed_test)
        [['bY','B'],['RG','RR'],['yG','BBB'],['GG','ARR'],['GY',''],['Br','RR'],['YR','BBBL'],['RY','RR'],['GR','RRR'],['GY','B'],['RR','A'],['RB','ALLL'],['Yb','AAALL'],['rb','AALL'],['R0','ARR'],['RY','AAARRR'],['GY','AAALLL'],['YB','BRR'],['GR','AAAR'],['YY','BBBR'],['GB','R'],['GG','AA'],['RY','AAAL'],['RY','BR'],['BR','ALLL'],['RY','AARR']],

        # 3 older edge cases (orig. b4b_fixed_smallset)
        [['RR',''],['RR','L'],['BB','R'],['BB','LL'],['GG',''],['GG','L'],['GG','LL'],['GG','R'],['0B','LLL'],['RG','AALL'],['By','BBABRRLR'],['GR','AAABLLRLL']],
        [['RR',''],['RR', 'L'],['RR', 'B'],['RR', 'B'],['BB', 'LL'],['RR', 'LL'],['Bb', 'LLL'],['GY','RLRLL'],['yY','BLLLR'],['GR','AAL']],
        [['YY','B'],['RR','B'],['GG','BRR'],['RR','R'],['BB','B'],['RR','B'],['BB','B'],['RR','B'],['RR','B'],['0B','LL'],['Gg','RR']],

        # complex area of single gems built on the fly, does NOT result in a power gem
        [['YY','LLL'],['YY','LL'],['BB','L'],['YY',''],['YY','R'],['YY','RR'],['YR','LLL'],['YR','LL'],['RB','AL'],['YR',''],['RB','R'],['RB','RR'],['RB','AAL'],['R0','LLL']],

        # complex area of single gems built on the fly, SHOULD result in a power gem
        [['YY','LLL'],['YY','LL'],['BB','L'],['YY',''],['YY','R'],['YY','RR'],['YR','LLL'],['RR','LL'],['RB','AL'],['YR',''],['RB','R'],['RB','RR'],['RB','AAL'],['R0','LLL']],

        # '00' landing vertically: only one has actually an effect
        [['YB','LLL'],['RY','LL'],['RR','L'],['BR',''],['YR','R'],['YR','RR'],['00','R']],

        # '00' landing horizontally on two identical colors
        [['YB','LLL'],['RY','LL'],['RR','L'],['RR',''],['YR','R'],['YR','RR'],['00','A']],

        # '00' landing horizontally on two different colors
        [['YB','LLL'],['RY','LL'],['RR','L'],['BR',''],['YR','R'],['YR','RR'],['00','A']],

        # '00' landing horizontally on two different colors, one being a crash gem
        [['YB','LLL'],['RY','LL'],['RR','L'],['bR',''],['YR','R'],['YR','RR'],['00','A']],

        # user not checking outside of the board after a rainbow gem exploded
        [['BB','LLL'],['BB','LLL'],['BB','LLL'],['BB','LLL'],['BB','LLL'],['BB','LLL'],['BB',''],['BB',''],['BB',''],['BB',''],['BB',''],['0B','']],

        # massive cascade of explosions/drops, result in a power gem that should fall correctly
        [['bY','ALL'],['YY','BBBL'],['YB','R'],['BR','LL'],['yg','AL'],['BY','RR'],['RR','AA'],['BB','R'],['RR','AR'],['BR','AAA'],['GB','AAA'],['RG','AA'],['YR','BBRRR'],['YY','BBLLL'],['GB','L'],['GB','AAL'],['RR','RR'],['bY','AAAR'],['0R','A'],['BY','L'],['yR','AAR'],['RY','AAAR'],['RY','BLL'],['RB','BBB'],['RY','LL'],['G0','LLL'],['B0',''],['RG','LLL'],['YG','BBB']],

        # powa expansion specific tests (jagged power gems, on long "shots")
        [['RR','BLL'],['BB','BLL'],['BB','L'],['BB','A'],['GG','RR'],['yR','L'],['YR','RR'],['RR','A'],['RR','A'],['YY','A'],['YY','A'],['RR','A'],['RY','RR'],['RR','LLL'],['RR','LL'],['Ry','L'],['0B','LLL']],

        # "non dropped" pairs (because already gems just below when entering the drop process) should still be seen to create powaGems
        [['GG','AAL'],['Rb','BRRR'],['GG','AAR'],['GR',''],['Rg','AARRR'],['RG','AAARR'],['0Y','BR'],['RB','BL'],['RR','BBBL'],['YY','RRR'],['YR','LL'],['GY','B'],['YY','R'],['Rg','BLL'],['BR','R'],['BB','AALL'],['GY','R'],['yR','AAAR'],['RB','AAL'],['BB','AA'],['RG','ALL'],['GG','AALL'],['YB','BB'],['gg','LLL'],['GY','LLL'],['BG','A'],['YG','AAAR'],['RB','LL'],['GG','A'],['YG','R'],['bY','AL'],['GY','AAL'],['YY','BRRR'],['YY','AARR'],['RG','RRR'],['GR','RRR'],['RB','BBB'],['BG','B'],['gr','AL'],['RG','BBBRR'],['gy','BL'],['YR','BBRRR'],['RB','L']],

        # beginning of tests used to fix bugs
        [['YB','BBLLL'],['YR','B'],['gG','RRR'],['Ry','BBRRR'],['YY','BBBL'],['YG','BBBRR'],['YY','AARR'],['GG','BBBL'],['GR','R'],['00','AAL'],['GG',''],['GY','BBBLL'],['RR','BB'],['RR','AALL'],['GB','LL'],['00','AAARRR']],
        [['gR','AAAL'],['BB','AR'],['bB','AAARRR'],['Ry','AALL'],['B0','BBBRRR'],['YR','BRRR'],['GR','LLL'],['GB','AA'],['RB','BRRR'],['BG',''],['RR','BL'],['RY','BL'],['GY','BBB'],['YY','LL'],['YG','R'],['YY','LLL'],['RG','AA'],['YG','BBB'],['Ry','AAAL'],['RR','BBBLL'],['RY','BLL'],['RR','BBLL'],['YG',''],['RR','BBL'],['BG','AAALLL'],['BG','LL'],['YY','BBR'],['GB','L'],['GB','R'],['BR','BB'],['RR','BBBLL'],['yR','BBBR'],['BY','RR'],['GY','AALL'],['yg','AAARRR'],['Bg','AAA'],['RG','BB'],['RG','A'],['RR',''],['YG','']],
        [['RR','LL'],['GY','AAALL'],['RR','B'],['BR','AAAL'],['Gr','BRRR'],['RR','LLL'],['YY','BBBR'],['BY','A'],['GY','A'],['GG','BRR'],['bR','BBBLLL'],['GG','AAAR'],['BR','AAAL'],['YB','AA'],['YY','BBLLL'],['YY','AALL'],['BG','A'],['RR','BR'],['YY','BBLLL'],['YY','LL'],['RB','AARR'],['GR','LLL'],['RY','AARR'],['BR',''],['YY','A'],['YR','BR'],['Rg','AARR'],['BG','R'],['gR','BBBLL'],['YY','BB'],['YY','AAA']],
        [['YY','BR'],['YY','AAAR'],['YG',''],['GG','BBBRRR'],['BR','BBRRR'],['RB','BBBLLL'],['YB','BBR'],['YR','AA'],['BR','BR'],['bG','RRR'],['RB','LLL'],['0Y','AAARRR'],['BG','AARRR'],['RR','BRRR'],['GY','B'],['YY','AAALL'],['GR','BL'],['YG','AAALL'],['YR','LL']],
        [['BB','LLL'],['BB','LL'],['GG','L'],['GG',''],['GG','AR'],['BB','AR'],['RR','B'],['RR','B'],['RR','B'],['RR','B'],['RR','BLL'],['RR','BLL'],['RR','BLL'],['RR','AR'],['YY','AR'],['RR','AR'],['GG','AR'],['RR','AR'],['YY','AR'],['RR','AR'],['YY','B'],['YY','B'],['RR','B'],['YY','BLL'],['RR','BLL'],['RR','BLL'],['YY','BLL'],['B0','LLL'],['Y0','LLL']],
        [['YG','BBRRR'],['BY','R'],['YG','AAAR'],['YR','AA'],['GY','L'],['YY','BBBLL'],['YG','AA'],['Gg','AALLL'],['GG',''],['GB','B'],['YB','BBRR'],['GR','BL'],['RR','BL'],['GY',''],['YR','B'],['GR','AAARRR'],['YY','ALL'],['GY','AAAR'],['GB','BBBRR'],['GG','R'],['BG','BL'],['RG',''],['RG',''],['YR','BBBRRR'],['GG','BBRRR'],['YY','R'],['RB','AAARR'],['YB','BL'],['GG','AAARRR'],['RY','BLL'],['BB','BBL'],['YR','AAA'],['0R','ARRR'],['BG','L'],['RB','AAA'],['RB','AA'],['GB','BBBL'],['YY',''],['RR','BBLL'],['yR','AAAL'],['GB','AL'],['RB','BB'],['BR','AAA'],['RY','AAARRR'],['GB','LLL'],['Yg','BBLL'],['BY','AAR'],['YR','BBLLL'],['YR','BLL'],['YY',''],['BG','BBBRR'],['RG','LL'],['RR','B'],['RG','AARR'],['GG','ALL'],['BR','AAARRR'],['YR','BLL'],['BB','AAAR'],['gG','BBBRR'],['bY','BBBL'],['RY','L'],['RB','AAL'],['BB','AAALL'],['YG','BR'],['RG','AAL'],['BY','BBLL'],['YB','B'],['BG','BBB'],['RG','AALLL'],['Gr','BBR'],['YB','AA'],['GG','AALL'],['GY','BBRR'],['rB','BLLL'],['0R','ALL'],['BG','LLL'],['gR','BBBLL'],['GB','BBBLL'],['GB','AAR'],['bY','']],
        [['BY','BRR'],['ry','L'],['BG','BBBLLL'],['YY','AAARR'],['RY','RRR'],['YY','R'],['YR','AR'],['GR','AL'],['BB','LLL'],['GY',''],['BG','L'],['GG','AAR'],['GG','RRR'],['RY','R'],['0Y','BBBRR'],['Bb','ALLL'],['GR',''],['R0','BBLLL'],['R0','AAALLL'],['GB','AAARR'],['BB','A'],['YB','B'],['GB','RRR'],['RB','AARRR'],['RB','AAL'],['RG','A'],['GY','AAAR'],['RR','AAAL'],['RG','L'],['GG','LL'],['GG','ARRR'],['BG','AALLL'],['YB','L'],['RG',''],['YG','AAA'],['GR','BBB'],['RB','AA'],['ry','BRRR'],['YY','AA'],['RB','B'],['YB','RRR'],['BR','BRRR'],['RR','AAAL'],['RG',''],['RG','AARR'],['GB','AAAR'],['RR','RRR'],['RY','B'],['RG','BR'],['RG','AAALL'],['YR','RR'],['YB','BBBLLL'],['GB','AA'],['BG','BBBRRR'],['YB','AAALLL'],['BY','A'],['YG','BBB'],['GY',''],['GY','BRR'],['Rr','BL'],['RG','L'],['RY','AAA'],['BY','AR'],['RR','AALL'],['YG','AAAR'],['YR','BBR'],['YB','AAARRR'],['YG','BB']],

        # 3 ADDITIONAL EDGE CASES ADDED 2019.07.31 (doc)
        [['rB','A'],['BR','LL'],['RY','BRRR'],['RB','AAALLL'],['BY','B'],['Yb','AAL'],['RB','BBBLLL'],['GY','LLL'],['BY','BB'],['YY','BBB'],['RR','BR'],['GR','BBB'],['Bb','ALL'],['YY','AARRR'],['gG','BL'],['GY','L'],['Rr','AAALLL'],['Yy','BRRR'],['GB','BBLL'],['YB','AAA'],['YB','AALLL'],['BY','AAALLL'],['BB','RR'],['G0','A'],['RG','AAR'],['RB','RR'],['BR','BL'],['yY','RRR'],['YG','LLL'],['BR','BB'],['BY','AR'],['BG','L'],['GB','A'],['bG','AAR'],['BB',''],['YB','AAAL'],['Bg','LLL'],['BY','BR'],['RG','AALLL'],['BG','BRRR'],['YB','AAA'],['BY','LLL'],['GR','AAR'],['GY','RRR'],['RR','BBBRRR'],['YB','RRR'],['YR','BRRR'],['G0','AAL'],['GY','AAL'],['YY','BBBRRR'],['YG','ALLL'],['BR','AALLL'],['RG','BBLL'],['RB','LL'],['RY','RR'],['Bg','AAA'],['BB','BBBL'],['RY','AAA'],['RG','BBBRR'],['BB','BL'],['GG','B'],['RG','BLLL'],['YG','RRR'],['yb','B'],['YB','A'],['RR','AAA'],['YG','BLL']],
        [['GR', 'AALL'], ['RR', 'B'], ['YY', 'R'], ['YB', 'BBRR'], ['BG', 'AA'], ['YB', 'ALLL'], ['YB', 'BBBRR'], ['Rr', 'BBRRR'], ['BB', 'BB'], ['GR', 'BBBLLL'], ['YG', 'RR'], ['yr', 'R'], ['RR', ''], ['YB', ''], ['YR', 'B'], ['YB', 'AAAL'], ['GB', 'BRRR'], ['B0', 'RRR'], ['RR', 'BBL'], ['Br', 'BBRR'], ['GB', 'L'], ['RB', 'BL'], ['RB', 'BBR'], ['BG', 'AR'], ['RB', 'BBRRR'], ['GB', 'A'], ['rY', 'BBLL'], ['B0', 'LL'], ['YG', 'BBB'], ['BY', 'BBBLLL'], ['YR', ''], ['RY', 'AAR'], ['YB', 'RR'], ['Bb', 'BLLL'], ['GB', 'B'], ['YB', 'AAL'], ['GB', 'B'], ['BR', 'R'], ['YY', 'AAARR'], ['BB', 'BBBR'], ['YG', 'BR'], ['GY', 'RR'], ['RY', 'BBLL'], ['GY', 'A'], ['YB', 'AAA'], ['BR', 'AARR'], ['RR', 'BBL'], ['GB', 'RRR'], ['BB', ''], ['GB', 'BBBL'], ['BB', 'AAARR'], ['Yr', ''], ['Gr', 'BLLL'], ['rY', 'LL'], ['GY', 'BB'], ['BR', 'ALLL'], ['GB', ''], ['YY', 'AAAL'], ['GG', 'L'], ['YG', 'AAA'], ['BR', 'BBR'], ['RB', 'BBRR']],
        [['YR', 'BBBRR'], ['YB', 'AAL'], ['YB', 'ALL'], ['RG', 'BLLL'], ['YY', ''], ['RG', 'AA'], ['RY', 'ALL'], ['BY', 'AR'], ['RY', 'AAAL'], ['BB', 'BBRR'], ['YB', 'AAL'], ['BY', 'BBB'], ['GY', 'AAARRR'], ['YB', ''], ['Yb', 'BBR'], ['YG', 'BLL'], ['YY', 'BR'], ['YB', 'B'], ['R0', 'BL'], ['RG', 'AAALL'], ['GG', ''], ['GR', 'LLL'], ['GG', 'AAAL'], ['BG', 'BBR'], ['BB', 'BB'], ['YY', 'AAALL'], ['GB', 'BBBLLL'], ['GB', 'AAL'], ['RB', 'AAALLL'], ['BG', 'BBL'], ['GB', 'BR'], ['RR', 'AL'], ['0B', 'AA'], ['YG', 'RRR'], ['B0', 'BB'], ['RB', 'BBBLL'], ['YG', 'BBB'], ['GR', 'LLL'], ['BB', 'LL'], ['YR', 'LL'], ['Ry', 'AAL'], ['BY', 'AR'], ['BY', 'BBBLL'], ['yR', 'AAR']]
    ]
    #'''


    # RNG function
    def RN(n,q=0):
        return randint(0,n-1) + q

    # assign random index value to B4B's tests (within range dictated by length of test case)
    B4B_edge_cases_index_list = {}
    for tc in B4B_edge_cases_20190730:
        moves_ct = len(tc)
        rnge = (40,0) if moves_ct < 21 else (80,40) if moves_ct < 51 else (80,120)
        test_pos = RN(*rnge)
        while test_pos in B4B_edge_cases_index_list:
            test_pos = RN(*rnge)
        B4B_edge_cases_index_list[test_pos] = tc


    # RANDOM TEST GENERATOR
    def sequence_gen(n):
        def gemgem():
            return [colors[RN(4)],colors[RN(4)]]
        def gemcrash():
            return [colors[RN(4)].lower(),colors[RN(4)]]
        def crashcrash():
            return [x.lower() for x in gemgem()]
        def gemrainbow():
            return [colors[RN(4)],'0']
        def doublerainbow():
            return ['0','0']
        r = []
        colors = 'RGBY'
        while n:
            pair = gemgem() if RN(6) else gemcrash() if RN(4) else crashcrash() if RN(2) else gemrainbow() if RN(4) else doublerainbow()
            if RN(2):
                pair.reverse()
            move = 'AB'[RN(2)]*RN(4) + 'RL'[RN(2)]*RN(4)
            r.append([''.join(pair),move])
            n -= 1
        return r

    verify_test = lambda r: ver_funk(puzzle_fighter([x[:] for x in r]),funk(r))
    i = 0
    @test.it('Short instruction sets (40 tests)')
    def _():
        nonlocal i
        # 10 <= moves <= 20
        while i < 40:
            if i in B4B_edge_cases_index_list:
                verify_test(B4B_edge_cases_index_list[i])
            else:
                verify_test(sequence_gen(RN(11,10)))
            i += 1
    

    @test.it('Medium instruction sets (80 tests)')
    def _():
        nonlocal i
        # 25 <= moves <= 50
        while i < 120:
            if i in B4B_edge_cases_index_list:
                verify_test(B4B_edge_cases_index_list[i])
            else:
                verify_test(sequence_gen(RN(26,25)))
            i += 1
    
    
    @test.it('Long instruction sets (80 tests)')
    def _():
        nonlocal i
        # 60 <= moves <= 100
        while i < 200:
            if i in B4B_edge_cases_index_list:
                verify_test(B4B_edge_cases_index_list[i])
            else:
                verify_test(sequence_gen(RN(41,60)))
            i += 1
