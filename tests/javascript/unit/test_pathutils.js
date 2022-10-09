import { strictEqual } from 'assert';
import  { escapeLocalPath } from "../../../src/modules/utility/pathutils";


describe("pathutils.escapeLocalPath() test", function () {
  function escapeLocalPathMultiTest(localPath, expectedEscapedPath) {
    it(`Path ${localPath} should be escaped into ${expectedEscapedPath}`, function() {
      let escapedPath = escapeLocalPath(localPath, expectedEscapedPath)
      strictEqual(escapedPath, expectedEscapedPath);
    });
  }

  let assertionsList = [
    ["spaced + - = # $ @ & % ,", "spaced + - = %23 $ @ & %25 ,"],
  ];

  for (let assertionTuple of assertionsList) {
    escapeLocalPathMultiTest(...assertionTuple);
  }
})
