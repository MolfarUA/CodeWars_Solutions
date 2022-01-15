String code(String s) {
    List<String> m = ['10','11','0110','0111','001100','001101','001110','001111','00011000','00011001'];
    return s.split('').map((x) => m[int.parse(x)]).join('');
}
String decode(String str) {
    var ret = "", i = 0, lg = str.length;
    while (i < lg) {
        var zero_i = i;
        while ((zero_i < lg) && (str[zero_i] != "1")) {
            zero_i++;
        }
        var l = zero_i - i + 2;
        var ss = str.substring(zero_i + 1, zero_i + l);
        ret += int.parse(ss, radix: 2).toString();
        i = zero_i + l;
    }
    return ret;
}
__________________________
import 'dart:convert';

String code(String s) => s.split('')
  .map((el) => '0'*((int.parse(el)).toRadixString(2).length -1) + '1' 
       + (int.parse(el)).toRadixString(2)).toList().join();

String decode(String str) {
  List<String> lst = [];
  var ct = 1;
  int i = 0;
  while(i < str.length-1){
    if(str[i] == '0'){
     i++;
    } else {
      lst.add(str.substring(i+1,i+1+ct));
      i += ct+1;
       ct = 0;
     }
      ct++;
  }           
  return lst.map((el) => int.parse(el, radix: 2).toString()).toList().join();
}
__________________________
final table = <String, String>{
  '0': '10',
  '1': '11',
  '2': '0110',
  '3': '0111',
  '4': '001100',
  '5': '001101',
  '6': '001110',
  '7': '001111',
  '8': '00011000',
  '9': '00011001'
};

String code(String s) {
  final a = s.split('');
  var result = '';
  for (var c in a) {
    result += table[c]!;
  }
  return result;
}

String decode(String str) {
  var start = 0;
  var result = '';
  while (start != str.length) {
    for (var element in table.values) {
      final a = str.substring(start, element.length + start);
      if (a == element) {
        var key = table.keys.firstWhere((k) => table[k] == element);
        result += key;
        start += element.length;
        break;
      }
    }
  }

  return result;
}
__________________________
String code(String s) {
  final sb = StringBuffer();

  s.split('').forEach((ch) {
    final b = int.parse(ch).toRadixString(2);
    sb.write('0' * (b.length - 1) + '1' + b);
  });

  return sb.toString();
}

String decode(String str) {
  bool isLenBits = true;
  var len = 1;
  final arr = <String>[];
  final sb = StringBuffer();
  for (final ch in str.split('')) {
    if (isLenBits) {
      if (ch == '0') {
        ++len;
      } else if (ch == '1') {
        isLenBits = false;
      }
    } else {
      sb.write(ch);
      --len;
      if (len == 0) {
        arr.add(sb.toString());
        sb.clear();
        isLenBits = true;
        len = 1;
      }
    }
  }
  arr.forEach((e) => sb.write(int.parse(e, radix: 2)));
  return sb.toString();
}

__________________________
String code(String s) {
    return s.split('').map(int.parse).map((e) => e.toRadixString(2)).map((bin) {
      final code = '${'0' * (bin.length - 1)}1';
      return '$code$bin';
    }).join();
}

String decode(String str) {
    final result = StringBuffer();
    var count = 0;
    for (var i = 0; i < str.length; ++i) {
      if (str[i] == '0') {
        count++;
        continue;
      }
      ++count;
      ++i;
      final dig = int.parse(str.substring(i, i + count), radix: 2);
      result.write(dig);
      i = i + count - 1;
      count = 0;
    }
    return result.toString();
}
