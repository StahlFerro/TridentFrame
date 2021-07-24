const assert = require('assert');

describe("Formatter test", function () {
    it('should parse json stdout and execute callback', function () {
      let x = 360;
      let doubler = () => { x = x * 2 };
      let sampleStdout = '{"debug": "Image created"}'
      parseStdOutAndCall(sampleStdout, doubler);
      assert.strictEqual(x, 4);
    })
})
