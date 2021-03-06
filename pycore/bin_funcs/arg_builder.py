from typing import List, Tuple
from ..core_funcs.criterion import ModificationCriteria, GIFOptimizationCriteria, APNGOptimizationCriteria


def gifsicle_mod_args(criteria: ModificationCriteria, gif_criteria: GIFOptimizationCriteria) -> List[Tuple[str, str]]:
    """Get a list of gifsicle arguments from either ModificationCriteria, or GIFOptimizationCriteria

    Args:
        criteria (ModificationCriteria): Image modification criteria
        gif_criteria (GIFOptimizationCriteria): GIF Optimization criteria

    Returns:
        List[Tuple[str, str]]: List of two valued tuples containing imagemagick argument on the first value, and a status string to echo out on the second value
    """
    args = []
    if criteria.must_resize():
        args.append((f"--resize={criteria.width}x{criteria.height}", "Resizing image..."))
    if criteria.orig_delay != criteria.delay:
        args.append((f"--delay={int(criteria.delay * 100)}", f"Setting per-frame delay to {criteria.delay}"))
    if gif_criteria.is_optimized and gif_criteria.optimization_level:
        args.append((f"--optimize={gif_criteria.optimization_level}", f"Optimizing image with level {gif_criteria.optimization_level}..."))
    if gif_criteria.is_lossy and gif_criteria.lossy_value:
        args.append((f"--lossy={gif_criteria.lossy_value}", f"Lossy compressing with value: {gif_criteria.lossy_value}..."))
    if gif_criteria.is_reduced_color and gif_criteria.color_space:
        args.append((f"--colors={gif_criteria.color_space}", f"Reducing colors to: {gif_criteria.color_space}..."))
    # if criteria.flip_x:
    #     args.append(("--flip-horizontal", "Flipping image horizontally..."))
    # if criteria.flip_y:
    #     args.append((f"--flip-vertical", "Flipping image vertically..."))
    if criteria.orig_loop_count != criteria.loop_count:
        loop_count = criteria.loop_count
        loop_arg = "--loopcount"
        if (not loop_count or loop_count == 0):
            loop_arg = "--loopcount"
        elif (loop_count == 1):
            loop_arg = '--no-loopcount'
        elif (loop_count > 1):
            loop_arg = f'--loopcount={loop_count - 1}'
        args.append((loop_arg, f"Changing loop count to {loop_count or 'Infinite'}..."))
    return args


def imagemagick_args(gifopt_criteria: GIFOptimizationCriteria) -> List[Tuple[str, str]]:
    """Get a list of imagemagick arguments from a GIFOptimizationCriteria

    Args:
        gifopt_criteria (GIFOptimizationCriteria): GIF Optimization Criteria

    Returns:
        List[Tuple[str, str]]: List of two valued tuples containing imagemagick argument on the first value, and a status string to echo out on the second value
    """
    args = []
    if gifopt_criteria.is_unoptimized:
        args.append(("-coalesce", "Unoptimizing GIF..."))
    # if criteria.rotation and criteria.rotation != 0:
    #     args.append((f"-rotate {criteria.rotation}", f"Rotating image {criteria.rotation} degrees..."))
    return args


def apngdis_args(criteria: ModificationCriteria) -> List[Tuple[str, str]]:
    args = []
    return args


