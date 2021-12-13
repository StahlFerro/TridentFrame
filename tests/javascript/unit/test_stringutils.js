import { strictEqual } from 'assert';
import { formatBytes, varToSpaceUpper } from "../../../src/modules/utility/stringutils";


describe("stringutils.formatBytes() test", function () {
  function formatBytesMultiTest(bytes, precision, expectedFileSize) {
    it(`${bytes} bytes rounded to ${precision} decimal places is ${expectedFileSize}`, function() {
      let actualFormatted = formatBytes(bytes, precision)
      strictEqual(actualFormatted, expectedFileSize);
    });
  }

  let assertions_list = [
    [0, 0, "0 B"],
    [1023, 0, "1023 B"],
    [2048, 0, "2 KB"],
    [6789, 3, "6.63 KB"],
    [4160557, 5, "3.96782 MB"],
    [893321359, 3, "851.938 MB"],
    [1049204261, 2, "1000.6 MB"],
    [1111111111, 2, "1.03 GB"],
  ];

  for (let assertion_tuple of assertions_list) {
    formatBytesMultiTest(...assertion_tuple);
  }
})


describe("stringutils.varSpaceToUpper() test", function() {
  function varSpaceToUpperMultiTest(var_name, expectedLabel) {
    it(`Variable name ${var_name} removed underscore and set uppercased is ${expectedLabel}`, function() {
      let actualLabel = varToSpaceUpper(var_name);
      strictEqual(actualLabel, expectedLabel);
    });
  }

  let assertions_list = [
    ["general_info", "GENERAL INFO"],
    ["animation_info", "ANIMATION INFO"],
  ];

  for (let assertion_tuple of assertions_list) {
    varSpaceToUpperMultiTest(...assertion_tuple);
  }
})