const FORBIDDEN_FILENAME_CHARACTERS_WINDOWS = [
  '<', '>', ':', '"', '/', '\\', '|', '?', '*'
];
const FORBIDDEN_FILENAME_WORDS_WINDOWS = [
  'CON', 'COM', 'LPT', 'AUX', 'PRN', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8',
  'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
];
const FORBIDDEN_FILENAME_CHARACTERS_LINUX = [
  '/'
];

const SlashDirection = Object.freeze({
  FORWARD: "forward",
  BACKWARD: "backward"
})

/**
 * Get list of characters that is forbidden to be used for filenames depending on the current platform
 * @returns {Array} List of forbidden characters/strings
 */
export function getSystemForbiddenFilenameCharacters() {
  if (process.platform == "win32")
    return FORBIDDEN_FILENAME_CHARACTERS_WINDOWS;
  else if (process.platform == "linux")
    return FORBIDDEN_FILENAME_CHARACTERS_LINUX;
}

/**
 * Convert Windows backslash paths to forward slash paths: `foo\\bar` ➔ `foo/bar`.
 * [Forward-slash paths can be used in Windows](http://superuser.com/a/176395/6877) as long as they're not extended-length paths and don't contain any non-ascii characters.
 * https://github.com/sindresorhus/slash/blob/main/index.js
 * @param {string} filePath 
 * @param {SlashDirection} slashDirection 
 */
function _slash(filePath, slashDirection = SlashDirection.FORWARD) {
  if (slashDirection == SlashDirection.FORWARD) {
    let isExtendedLengthPath = /^\\\\\?\\/.test(filePath); // https://docs.winbatch.com/mergedProjects/WindowsInterfaceLanguage/html/Extended-Length_Path.htm
    let hasNonAscii = /[^\u0000-\u0080]+/.test(filePath); // eslint-disable-line no-control-regex
    if (isExtendedLengthPath || hasNonAscii) {
      return filePath;
    }
    return filePath.replace(/\\/g, '/');
  }
  else if (slashDirection == SlashDirection.BACKWARD) {
    return filePath.replace(/\//g, '\\');
  }
}

export function slashForward(path) {
  return _slash(path, SlashDirection.FORWARD);
}

export function slashBackward(path) {
  return _slash(path, SlashDirection.BACKWARD);
}

/**
 * Escapes local machine path for Electron's src view
 * @param {string} localPath Path to file
 * @returns {string} Escaped local path
 */
export function escapeLocalPath(localPath) {
  let escapePath = "";
  // let escapePath = encodeURI(localPath);
  // if (process.platform == "win32")
  //   localPath = _slash(localPath, SlashDirection.FORWARD);
  // if (process.platform == "win32")
  escapePath = localPath
    .replace("%", "%25")
    .replace("#", "%23");
  // else
  //   escapePath = localPath;
  console.log(localPath);
  console.log(escapePath);
  return escapePath;
}

/**
 * Check if string is valid for a file name.
 * @param {string} filename File name to check
 * @returns {boolean} true if filename is valid, else false.
 */
export function validateFilename(filename) {
  let forbidden_string = getSystemForbiddenFilenameCharacters().join();
  let regex = new RegExp(forbidden_string, 'g');
  let is_valid = !filename.match(regex);
  return is_valid;
}

/**
 * Get the file name without extensions
 * @param {string} filename File name including extension
 */
export function stem(filename) {
  return filename.replace(/\.[^/.]+$/, "")
}