/**
 * Class containing the summary of a preview image properties.
 */
class PreviewImageSummary {
  constructor(width, height, fileSize, isAnimated, frameCount, averageFPS, averageDuration, loopCount, format) {
    this.width = width;
    this.height = height;
    this.fileSize = fileSize;
    this.isAnimated = isAnimated;
    this.frameCount = frameCount;
    this.averageFPS = averageFPS;
    this.averageDuration = averageDuration;
    this.loopCount = loopCount;
    this.format = format;
  }

  get dimensionString() {
    return `${this.width} x ${this.height}`;
  }

  toSummaryText() {
    let text = `Dimensions: ${this.dimensionString}\n` +
    `File size: ${this.fileSize}\n` +
    `Total frames: ${this.frameCount}\n` +
    `FPS: ${this.averageFPS}\n` +
    `Duration: ${this.averageDuration} seconds\n` +
    `Loop count: ${this.loopCount}\n` +
    `Format: ${this.format}`;
    return text;
  }
}

export default PreviewImageSummary;
