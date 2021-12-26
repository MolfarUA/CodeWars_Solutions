#adapted from Zozo-senpai work

test.describe("Pig Latin")
test.assert_equals(pig_it('Pig latin is cool'),'igPay atinlay siay oolcay')
test.assert_equals(pig_it('This is my string'),'hisTay siay ymay tringsay')
from random import shuffle
base=[
  ['Acta est fabula', 'ctaAay steay abulafay'],
  ['Barba non facit philosophum', 'arbaBay onnay acitfay hilosophumpay'],
  ['Cucullus non facit monachum', 'ucullusCay onnay acitfay onachummay'],
  ['Dura lex sed lex', 'uraDay exlay edsay exlay'],
  ['Errare humanum est', 'rrareEay umanumhay steay'],
  ['Fluctuat nec mergitur', 'luctuatFay ecnay ergiturmay'],
  ['Gutta cavat lapidem', 'uttaGay avatcay apidemlay'],
  ['Hic et nunc', 'icHay teay uncnay'],
  ['In vino veritas', 'nIay inovay eritasvay'],
  ['Lux in tenebris lucet', 'uxLay niay enebristay ucetlay'],
  ['Morituri nolumus mori', 'orituriMay olumusnay orimay'],
  ['Nunc est bibendum', 'uncNay steay ibendumbay'],
  ['O tempora o mores !', 'Oay emporatay oay oresmay !'],
  ['Panem et circenses', 'anemPay teay ircensescay'],
  ['Quis custodiet ipsos custodes ?', 'uisQay ustodietcay psosiay ustodescay ?'],
  ['Requiescat in pace', 'equiescatRay niay acepay'],
  ['Sic transit gloria mundi', 'icSay ransittay loriagay undimay'],
  ['Timeo Danaos et dona ferentes', 'imeoTay anaosDay teay onaday erentesfay'],
  ['Ultima necat', 'ltimaUay ecatnay'],
  ['Veni vidi vici', 'eniVay idivay icivay']]
shuffle(base)
for item in base:
    test.assert_equals(pig_it(item[0]),item[1],"You should 'pig' \""+item[0]+"\"")
