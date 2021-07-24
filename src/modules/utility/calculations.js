function roundPrecise(number, precision = 0) {
  let mult = Math.pow(10, precision);
  return (Math.round(number * mult) / mult);
}

/**
 * Gets the greatest common divisor between two numbers
 * @param {number} a 
 * @param {number} b 
 */
function gcd(a, b) {
  if (b == 0)
    return a;
  else
    return gcd(b, (a % b));
}


module.exports = {
  roundPrecise: roundPrecise,
  gcd: gcd,
}
