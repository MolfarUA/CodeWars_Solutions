test.describe("Fixed tests")
test.assert_equals(zipvalidate('142784'), True, 'should return True for valid postcode')
test.assert_equals(zipvalidate('642784'), True, 'should return True for valid postcode')

test.assert_equals(zipvalidate('111'), False, 'postcode should be 6 digits long')
test.assert_equals(zipvalidate('1111111'), False, 'postcode should be 6 digits long')
test.assert_equals(zipvalidate('AA5590'), False, 'postcode should be with no letters')
test.assert_equals(zipvalidate(''), False, 'an empty string is not a postcode')
test.assert_equals(zipvalidate('\n245980'), False, 'postcode should be with digits only')
test.assert_equals(zipvalidate('245980\n'), False, 'postcode should be with digits only')
test.assert_equals(zipvalidate('245980a'), False, 'postcode should be with digits only')
test.assert_equals(zipvalidate('24598a'), False, 'postcode should be with digits only')
test.assert_equals(zipvalidate(' 310587 '), False, 'postcode should be with digits only (no spaces)')
test.assert_equals(zipvalidate('555555'), False, 'postcode can\'t start with 0,5,7,8 or 9')
test.assert_equals(zipvalidate('775255'), False, 'postcode can\'t start with 0,5,7,8 or 9')
test.assert_equals(zipvalidate('875555'), False, 'postcode can\'t start with 0,5,7,8 or 9')
test.assert_equals(zipvalidate('012345'), False, 'postcode can\'t start with 0,5,7,8 or 9')
test.assert_equals(zipvalidate('968345'), False, 'postcode can\'t start with 0,5,7,8 or 9')
test.assert_equals(zipvalidate('@68345'), False, 'postcode can\'t start with a non-digit character')


test.describe("Some random tests")
from random import shuffle, randint

rnd = lambda x: randint(0, x-1)
  
def tst(x):
      uu = [[0,5,7,8,9][x]]
      vv = [1,2,3,4,6]; shuffle(vv)
      ww = [1,2,3,"A","S","G","E","T","S","_"]; shuffle(ww)
      cc = [1,2,3,"!","@",".","?","'","$",","]; shuffle(cc)
      ii = ["A","z","_","@","#"]; shuffle(ii)
      dd = vv + uu; shuffle(dd)
      mm = ["valid","too short","too long","non-digit","non-digit","invalid 1st digit","invalid 1st char (non-digit)"]
      tt = list(range(7)); shuffle(tt)
#      print uu, vv, ww, cc, ii, dd, mm, tt
      for t in tt:
          zipcode = "";
          zipcode = (vv[:1] + dd[:5],
                      vv[:1] + dd[:1+rnd(3)],
                      vv[:1] + dd[:6+rnd(3)],
                      vv[:1] + ww[:5],
                      vv[:1] + cc[:5],
                      uu[:1] + dd[:5],
                      ii[:1] + dd[:5],
                  )[t]
      zipcode = ''.join(map(str, zipcode))
      test.it(" Is " + zipcode + " a valid postcode?")
      test.assert_equals(zipvalidate(zipcode), not t, mm[t])

for i in range(42):
    tst(i % 5)

''' JS for reference
test.describe("Some random tests...",function(){
  var arrnd = function(aa){return Test.randomize(aa.slice(0)) };
  var rnd = function(x){ return ~~(Math.random()*x) }
  
  var tst = function(x){
    var tt = arrnd([0,1,2,3,4,5,6]),
        uu = [[0,5,7,8,9][x]],
        vv = arrnd([1,2,3,4,6]),
        ww = arrnd([1,2,3,"A","S","G","E","T","S","_"]),
        cc = arrnd([1,2,3,"!","@",".","?","'","$",","]),
        ii = arrnd(["A","z","_","@","#"]),
        dd = arrnd(vv.concat(uu)),
        mm = ["valid","too short","too long","non-digit","non-digit","invalid 1st digit","invalid 1st char (non-digit)"];
    tt.forEach(function(t){
      var zip = "";
      switch(t){
        case 0: zip = [vv[0]].concat(dd.slice(0,5)); break;
        case 1: zip = [vv[0]].concat(dd.slice(0,1+rnd(3))); break;
        case 2: zip = [vv[0]].concat(dd.slice(0,6+rnd(3))); break;
        case 3: zip = [vv[0]].concat(ww.slice(0,5)); break;
        case 4: zip = [vv[0]].concat(cc.slice(0,5)); break;
        case 5: zip = [uu[0]].concat(dd.slice(0,5)); break;
        case 6: zip = [ii[0]].concat(dd.slice(0,5)); break;
      }
      zip = zip.join('');
      console.log(" Is "+zip+" a valid postcode ?");
      Test.assertEquals(zipvalidate(zip),!t,mm[t])
    })
  }
  for(var x=0; x<5; x++) tst(x);
  
})
'''
