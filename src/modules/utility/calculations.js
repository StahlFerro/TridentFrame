/**
 * Round to a certain decimal place.
 * @param {number} number Floating point number to round.
 * @param {number} precision Decimal places to round to.
 */
export function roundPrecise(number, precision = 0) {
  // let mult = Math.pow(10, precision);
  // return (Math.round(number * mult) / mult);
  return Number(Math.round(`${number}e${precision}`) + `e-${precision}`);
}

/**
 * Gets the greatest common divisor between two numbers.
 * @param {number} a First number
 * @param {number} b Second number
 */
export function gcd(a, b) {
  if (b == 0)
    return a;
  else
    return gcd(b, (a % b));
}
