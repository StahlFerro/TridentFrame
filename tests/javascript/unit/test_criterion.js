import { strictEqual } from 'assert';
import { CreationCriteria } from '../../../src/models/criterion';


describe("criterion test", function () {
  /**
   * 
   * @param {CreationCriteria} criteria Creation criteria
   * @param {int} frameCount Frame count
   * @param {object} frameInfo Frame information
   */
  function getSkippedFrames(criteria, frameCount, skippedFramesList) {
    it(`Criteria with frame skip information below:
        skip           : ${criteria.frame_skip_count}, 
        gap            : ${criteria.frame_skip_gap}, 
        offset         : ${criteria.frame_skip_offset}, 
        maintain delay : ${criteria.frame_skip_maintain_delay}, 
        frame count    : ${frameCount}
        should have these frames skipped: ${skippedFramesList}`, function() {
      let frameInfo = criteria.getFramesInfo(frameCount);
      let skipsList = Object.entries(frameInfo).map(([k, v]) => v['isSkipped'])
      console.log(skipsList);
      console.log(skippedFramesList);
      strictEqual(skipsList.length, skippedFramesList.length);
      const equalItems = skipsList.every((skip, index) => skip == skippedFramesList[index]);
      strictEqual(equalItems, true);
    });
  }

  let criteria01 = new CreationCriteria();
  criteria01.frame_skip_count = 0;
  criteria01.frame_skip_gap = 0;
  criteria01.frame_skip_offset = 0;
  criteria01.frame_skip_maintain_delay = false;

  let criteria02 = new CreationCriteria();
  criteria02.frame_skip_count = 1;
  criteria02.frame_skip_gap = 0;
  criteria02.frame_skip_offset = 0;
  criteria02.frame_skip_maintain_delay = false;

  let criteria03 = new CreationCriteria();
  criteria03.frame_skip_count = 1;
  criteria03.frame_skip_gap = 0;
  criteria03.frame_skip_offset = 1;
  criteria03.frame_skip_maintain_delay = false;

  let criteria04 = new CreationCriteria();
  criteria04.frame_skip_count = 1;
  criteria04.frame_skip_gap = 2;
  criteria04.frame_skip_offset = 0;
  criteria04.frame_skip_maintain_delay = false;

  let criteria05 = new CreationCriteria();
  criteria05.frame_skip_count = 2;
  criteria05.frame_skip_gap = 1;
  criteria05.frame_skip_offset = 1;
  criteria05.frame_skip_maintain_delay = false;

  let skipFrameAssertionsList = [
    [criteria01, 2, [false, false]],
    [criteria01, 5, [false, false, false, false, false]],
    [criteria02, 2, [false, true]],
    [criteria02, 3, [false, true, false]],
    [criteria02, 11, [false, true, false, true, false, true, false, true, false, true, false]],
    [criteria03, 2, [true, false]],
    [criteria03, 6, [true, false, true, false, true, false]],
    [criteria04, 2, [false, false]],
    [criteria04, 4, [false, false, true, false]],
    [criteria04, 10, [false, false, true, false, false, true, false, false, true, false]],
    [criteria05, 2, [true, false]],
  ];

  for (let assertionTuple of skipFrameAssertionsList) {
    getSkippedFrames(...assertionTuple);
  }
})
