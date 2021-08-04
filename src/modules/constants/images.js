export const PROCESSING_IMG_EXTS = ["png", "gif", "jpg", "jpeg"];
export const INSPECTING_IMG_EXTS = [...PROCESSING_IMG_EXTS, "webp"]
export const DIALOG_PROCESSING_EXT_FILTERS = [{
  name: "Images",
  extensions: PROCESSING_IMG_EXTS,
}, ];
export const DIALOG_INSPECTING_EXT_FILTERS = [{
  name: "Images",
  extensions: INSPECTING_IMG_EXTS,
}, ];
export const GIF_DELAY_DECIMAL_PRECISION = 2;
export const APNG_DELAY_DECIMAL_PRECISION = 3;