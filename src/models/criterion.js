const { Preset } = require('./presets.js');

class TransformativeCriteria {
  constructor() {
    this.width = "";
    this.height = "";
    this.resize_method = "BICUBIC";
    this.flip_x = false;
    this.flip_y = false;
    this.rotation = 0;
  }

  /**
   * Update properties from Preset instance.
   * @param {Preset} preset Preset instance
   */
  updateFromPreset(preset) {
    console.debug('updateFromPreset');
    // Loop through all key value pairs on presetObject
    for (const [k, v] of Object.entries(preset.presetObject)) {
      // Check if key in presetObject exist as a property on criteria
      if (k in this) {
        // Skip if value in presetObject is null or empty string
        if (!v) continue;
        else {
          this[k] = v;
        }
      }
    }
  }
}


class AnimationCriteria extends TransformativeCriteria {
  constructor() {
    super();
    this.fps = "";
    this.delay = "";
    this.delays_are_even = true;
    this.delays_list = [];
    this.is_reversed = false;
    this.preserve_alpha = false;
    this.loop_count = null;
    this.start_frame = null;
    this.frame_skip_count = null;
    this.frame_skip_gap = null;
    this.frame_skip_offset = null;
    this.frame_skip_maintain_delay = false;
  }

  getFramesInfo(frameCount) {
    const skip = Number.parseInt(this.frame_skip_count ?? 0);
    const gap = Number.parseInt(this.frame_skip_gap ?? 0) > 0 ? Number.parseInt(this.frame_skip_gap) : 1;
    const offset = - Number.parseInt(this.frame_skip_offset ?? 0);
    const cycleLength = skip + gap;
    const framesInfo = {};
    for (let index = 0; index < frameCount; index++){
      const cycleOrd = Math.floor((index + offset) / cycleLength);
      const currentCycleGapMax = cycleOrd * cycleLength + gap - 1 - offset;
      const isSkipped = false;
      if (index > currentCycleGapMax) {
        isSkipped = true;
      }
      framesInfo[index] = {'isSkipped': isSkipped};
    }
    // console.log(framesInfo);
    return framesInfo;
  }

  validateSkipFrames(count) {
    const framesInfo = this.getFramesInfo(count);
    return this._validateSkipFrames(framesInfo);
  }

  _validateSkipFrames(framesInfo) {
    const skippedFrames = Object.entries(framesInfo).map(([k, v]) => v.isSkipped);
    const unskippedFrameCount = skippedFrames.filter(sk => !sk).length;
    if (unskippedFrameCount >= 2)
      return true;
    return false;
  }
}



class CreationCriteria extends AnimationCriteria {
  constructor() {
    super();
    this.format = "gif";
  }
}


class ModificationCriteria extends CreationCriteria {
  constructor() {
    super();
    this.delay_handling = "MULTIPLY_AVERAGE";
  }
}


class GIFOptimizationCriteria {
  constructor() {
    this.is_optimized = false;
    this.optimization_level = "1";
    this.is_lossy = false;
    this.lossy_value = 30;
    this.is_reduced_color = false;
    this.color_space = 256;
    this.is_unoptimized = false
    this.dither_method = "FLOYD_STEINBERG";
    this.palletization_method = "ADAPTIVE"
    this.is_dither_alpha = false;
    this.dither_alpha_method = "SCREENDOOR";
    this.dither_alpha_threshold = 50;
  }
}


class APNGOptimizationCriteria {
  constructor() {
    this.apng_is_optimized = false;
    this.apng_optimization_level = "1";
    this.apng_is_reduced_color = false;
    this.apng_color_count = 256;
    this.apng_quantization_enabled = false;
    this.apng_quantization_quality_min = 65;
    this.apng_quantization_quality_max = 80;
    this.apng_quantization_speed = 3;
    this.apng_is_unoptimized = false;
    this.apng_convert_color_mode = false;
    this.apng_new_color_mode = "RGBA";
  }
}

export {
  TransformativeCriteria,
  CreationCriteria,
  ModificationCriteria,
  GIFOptimizationCriteria,
  APNGOptimizationCriteria,
}