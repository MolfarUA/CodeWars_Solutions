solution = /^(0|(10((0|11)(1|00))*(10|(0|11)01)|11)(01*0(0|101|1(1|00)((0|11)(1|00))*(10|(0|11)01)))*1)+$/

__________________________
solution = /^((0|1((1(01*00)*01*010|(0|1(01*00)*01*011)(((0|11)1|10(01*00)*01*011))*((0|11)0|10(01*00)*01*010)))*(1(01*00)*1|(0|1(01*00)*01*011)(((0|11)1|10(01*00)*01*011))*10(01*00)*1)))+$/

_________________________
q1q4 = '1(01*00)*01*01|0((0|11)|10(01*00)*01*01)'
q4q4 = '1((0|11)|10(01*00)*01*01)'
q4q0 = '110(01*00)*1'
q1q1 = "(#{q1q4})(#{q4q4})*0"
q1q0a = '1(01*00)*1|010(01*00)*1'
q1q0b = "(#{q1q4})(#{q4q4})*(#{q4q0})"
q1q0 = "(#{q1q1})*((#{q1q0a})|(#{q1q0b}))"
q0q0 = "0|1(#{q1q0})"
solution = new RegExp "^(0|1(#{q1q0}))(#{q0q0})*$"

____________________________________________
solution = /^(0|(10((0|11)(1|00))*(10|(0|11)01)|11)(01*0(0|101|1(1|00)((0|11)(1|00))*(10|(0|11)01)))*1)+$/;
