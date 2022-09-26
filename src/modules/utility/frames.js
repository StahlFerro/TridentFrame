function buildFrameInfo(frameCount, skip, gap, offset) {
  const cycleLength = skip + gap;
  const framesInfo = {};
  for (let index = 0; index < frameCount; index++){
    const cycleOrd = Math.floor((index + offset) / cycleLength);
    const currentCycleGapMax = cycleOrd * cycleLength + gap - 1 - offset;
    const isSkipped = false;
    if (index > currentCycleGapMax) {
      isSkipped = true;
    }
    framesInfo[index] = {'isSkipped': isSkipped, 'cyleOrd': cycleOrd, 'currentCycleGapMax': currentCycleGapMax, 'cycleLength': cycleLength, 'offset': offset};
  }
  console.log(framesInfo);
  return framesInfo;
}

module.exports.buildFrameInfo = buildFrameInfo;
