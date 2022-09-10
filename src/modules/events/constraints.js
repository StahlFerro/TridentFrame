/**
 * Constrain number input fields to obey certain criteria
 * @param {Event} event keydown event
 * @param {Boolean} must_unsigned Enforce unsigned numbers only
 * @param {Boolean} must_whole Enforce whole numbers only
 * @returns {Boolean} True or false
 */
export function numConstrain(event, must_unsigned = false, must_whole = false) {
  console.log(event);
  console.log("num constrain args", must_unsigned, must_whole);
  let current_value = event.target.value;
  console.log("current value", current_value);
  let key = event.key;
  let is_unsigned = false;
  let is_whole = false;
  let is_violating = false;
  if ((current_value.includes(".") && key == ".") || key == 'e') {
    event.preventDefault();
    return false;
  } else {
    if (must_unsigned) {
      is_violating = event.key == '-' ? true : is_violating;
      console.log("is violating must_unsigned", event.key == '-');
    }
    if (must_whole) {
      is_violating = event.key == '.' ? true : is_violating;
      console.log("is violating must_whole", event.key == '.');
    }
    if (is_violating) {
      event.preventDefault();
      return false;
    } else {
      return true;
    }
  }
}

export function posWholeNumConstrain(event) {
  console.log(event.key);
  if (event.key != "." && event.key != '-') {
    console.log("IS DIGIT!");
    return true;
  } else {
    console.log("IS NOT DIGIT!");
    event.preventDefault();
  }
}

export function wholeNumConstrain(event) {
  console.log('wholeNumConstrain', event.key);
  if (event.key != "." && event.key != 'e') {
    console.log("IS DIGIT!");
    return true;
  } else {
    console.log("IS NOT DIGIT!");
    event.preventDefault();
  }
};

export function floatConstrain(event) {
  console.log('float constrain', event);
  let current_value = event.target.value;
  let key = event.key;
  if (current_value.includes(".") && key == ".") {
    event.preventDefault();
  } else {
    return true;
  }
  // let float_regex = new RegExp('(^[0-9]*\\.?[0-9]*$)');
  // if (float_regex.test(event.target.value)) {
  //   console.log("IS FLOAT!");
  //   return true;
  // }
  // else {
  //   console.log("NOT FLOAT!");
  //   event.preventDefault();
  // }
}
