<script>
const zerorpc = require("zerorpc");
let client = new zerorpc.Client({ heartbeatInterval: 300000 });
client.connect("tcp://127.0.0.1:4242");

const ImageViewer = require("iv-viewer").default;
const GIF_DELAY_DECIMAL_PRECISION = 2;

module.exports.client = client;
module.exports.ImageViewer = ImageViewer;
module.exports.GIF_DELAY_DECIMAL_PRECISION = GIF_DELAY_DECIMAL_PRECISION;
</script>
