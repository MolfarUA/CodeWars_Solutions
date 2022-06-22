563f037412e5ada593000114


function calculateYears(principal, interest, tax, desired) {
  return Math.ceil(
    Math.log(desired / principal) / 
    Math.log(1 + interest * (1 - tax))
  );
}
_________________________
function calculateYears(principal, interest, tax, desired) {
var year = 0;
    while (principal < desired){
        principal += principal * interest * (1 - tax);
        year +=1;
     }
    return year;
}
_________________________
function calculateYears(P,I,T,D) { return Math.ceil( Math.log(D/P) / Math.log1p(I*(1-T)) ); }
_________________________
function calculateYears(principal, interest, tax, desired) {
    var start = 0;
    while(principal < desired) {
      var intBeforeTax = principal * interest;
      var intRate = (intBeforeTax - (intBeforeTax * tax));
      principal+=intRate;
      start++;
    }
    return start;
}
