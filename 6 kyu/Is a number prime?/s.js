function isPrime(num) {
  if (num < 2) return false;
  const limit = Math.sqrt(num);
  for (let i = 2; i <= limit; ++i) {
    if (num % i === 0) {
      return false;
    }
  }
  return true;
}
________________________
function isPrime(num) {
    if (num <= 1) return false;  // الأرقام 1 أو أقل مش أعداد أولية
    for (let i = 2; i <= Math.sqrt(num); i++) {
        if (num % i === 0) return false; // لو لقيت قاسم غير 1 ونفسه يبقى مش أولي
    }
    return true; // لو مفيش قاسم يبقى أولي
}
________________________
function isPrime(num) {
  //TODO
if (num <= 1) {
    return false;
  }

  // Solo necesitamos verificar hasta la raíz cuadrada de num
  let sqrt = Math.sqrt(num);

  for (let i = 2; i <= sqrt; i++) {
    if (num % i === 0) {
      return false;
    }
  }

  return true;
}
