function escapeLocalPath(path) {
  return path.replace("%", "%25");
}

function validateFilename(filename) {
  // Valid if the filename does not contain these characters: <>:"/\|?*
  var is_valid = !filename.match(/[<>:"\/\\|\?\*]/g);
  if (is_valid) {
    return {"valid": true, "msg": ""};
  }
  else {
    return {"valid": false, "msg": `File names must not contain these following characters: < > : " / \\ | ? *`};
  }
}


function stem(filename) {
  return filename.replace(/\.[^/.]+$/, "")
}

module.exports = {
  escapeLocalPath: escapeLocalPath,
  validateFilename: validateFilename,
  stem: stem,
}
