<script>
const zerorpc = require("zerorpc");
let client = new zerorpc.Client({ heartbeatInterval: 3600 * 1000 });
client.connect("tcp://127.0.0.1:42069");

// const ImageViewer = require("iv-viewer").default;

module.exports.client = client;
// module.exports.ImageViewer = ImageViewer;
</script>
