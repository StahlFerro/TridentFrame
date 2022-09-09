class TransformativeCriteria {
  constructor() {
    this.width = "";
    this.height = "";
    this.resize_method = "BICUBIC";
    this.flip_x = false;
    this.flip_y = false;
    this.rotation = 0;
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
    this.loop_count = "";
    this.start_frame = "";
    this.skip_frame = 0;
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