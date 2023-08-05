import os
import cv2
import numpy as np
import random
from typing import Any, Union
import math

from ipso_phen.ipapi.tools.csv_writer import AbstractCsvWriter

import logging

logger = logging.getLogger(os.path.splitext(__name__)[-1].replace(".", ""))


class ToolFamily:
    ANCILLARY = "Ancillary"
    CLUSTERING = "Clustering"
    DEMO = "Demo"
    DEFAULT_PROCESS = "Execute default process"
    FEATURE_EXTRACTION = "Feature extraction"
    EXPOSURE_FIXING = "Exposure fixing"
    ASSERT = "Assert..."
    IMAGE_GENERATOR = "Image generator"
    IMAGE_INFO = "Image info"
    MASK_CLEANUP = "Mask cleanup"
    PRE_PROCESSING = "Pre processing"
    ROI = "Create an ROI"
    THRESHOLD = "Threshold"
    VISUALIZATION = "Visualization"
    WHITE_BALANCE = "White balance"
    UNKNOWN = "Unknown"
    PCV = "PlantCV"
    # Deprecated
    ROI_DYNAMIC = "ROI (dynamic)"
    ROI_STATIC = "ROI (static)"
    ROI_PP_IMAGE = "ROI on pre processed image"
    ROI_RAW_IMAGE = "ROI on raw image"


tool_family_hints = {
    ToolFamily.ANCILLARY: "Tools mostly used inside other tools",
    ToolFamily.CLUSTERING: "Clustering tools",
    ToolFamily.DEMO: "Demo tools, start here if you want to understand how to create/edit tools",
    ToolFamily.DEFAULT_PROCESS: """Execute a class pipeline linked to the selected image experiment,
    if no class pipeline is available an error will be reported""",
    ToolFamily.FEATURE_EXTRACTION: "Tools to extract features from a segmented image",
    ToolFamily.EXPOSURE_FIXING: "Fix image exposure, the resulting image will be used for color analysis",
    ToolFamily.IMAGE_GENERATOR: "Creates one or more images from a selected image",
    ToolFamily.IMAGE_INFO: "Gives info about current image",
    ToolFamily.MASK_CLEANUP: "Cleans a coarse mask generated by threshold tools",
    ToolFamily.PRE_PROCESSING: """Transform the image to help segmentation, 
    the image may not retain it's 
    properties. Changes here will be ignored when extracting features""",
    ToolFamily.ROI: "Create an ROI",
    ToolFamily.ASSERT: "Assert something, returns wether or not assertion is passed",
    ToolFamily.THRESHOLD: "Creates a mask that keeps only parts of the image",
    ToolFamily.VISUALIZATION: "Visualization tools",
    ToolFamily.WHITE_BALANCE: """Tools to help change white balance, depending on where those tools are set in the pipeline they or
    may not be ignored when extracting features""",
    ToolFamily.UNKNOWN: "There should be nothing here",
    ToolFamily.PCV: "UI integration of a PlantCV script",
}

tool_groups_pipeline = [
    ToolFamily.ASSERT,
    ToolFamily.FEATURE_EXTRACTION,
    ToolFamily.EXPOSURE_FIXING,
    ToolFamily.MASK_CLEANUP,
    ToolFamily.PRE_PROCESSING,
    ToolFamily.ROI,
    ToolFamily.THRESHOLD,
    ToolFamily.WHITE_BALANCE,
    ToolFamily.IMAGE_GENERATOR,
    ToolFamily.VISUALIZATION,
]

IO_IMAGE = "io_image"
IO_MASK = "io_mask"
IO_ROI = "io_roi"
IO_DATA = "io_data"
IO_NONE = "io_none"

MERGE_MODE_AND = "merge_mode_and"
MERGE_MODE_OR = "merge_mode_or"
MERGE_MODE_CHAIN = "merge_mode_chain"
MERGE_MODE_NONE = "merge_mode_none"


def io_type_to_str(io_type: str) -> str:
    if io_type == IO_IMAGE:
        return "image"
    elif io_type == IO_MASK:
        return "mask"
    elif io_type == IO_ROI:
        return "ROI"
    elif io_type == IO_DATA:
        return "data"
    elif io_type == IO_NONE:
        return "none"
    else:
        return "unknown"


def merge_mode_to_str(merge_mode: str) -> str:
    if merge_mode == MERGE_MODE_AND:
        return "AND"
    elif merge_mode == MERGE_MODE_OR:
        return "OR"
    elif merge_mode == MERGE_MODE_CHAIN:
        return "CHAIN"
    elif merge_mode == MERGE_MODE_NONE:
        return "NONE"
    else:
        return "unknown"


AVAILABLE_FEATURES = sorted(
    [
        # Header - text values
        "experiment",
        "plant",
        "date_time",
        "hist_bins",
        # Morphology
        "area",
        "hull_area",
        "width_data",
        "shape_height",
        "centroid",
        "shape_solidity",
        "shape_extend",
        "straight_bounding_rectangle",
        "rotated_bounding_rectangle",
        "minimum_enclosing_circle",
        "bound_data",
        "quantile_width_4",
        # Color descriptors
        "color_std_dev",
        "color_mean",
        "quantile_color_5",
        # Chlorophyll data
        "chlorophyll_mean",
        "chlorophyll_std_dev",
    ]
)

DEFAULT_COLOR_MAP = cv2.COLORMAP_JET

RGB = "rgb"
LAB = "lab"
HSV = "hsv"
MSP = "msp"
NDVI = "ndvi"
CHLA = "chla"

_HSV_CHANNELS = dict(
    h="hue",
    s="saturation",
    v="value",
)
_LAB_CHANNELS = dict(
    l="lightness",
    a="a_green-red",
    b="b_blue-yellow",
)
_RGB_CHANNELS = dict(
    rd="red",
    gr="green",
    bl="blue",
)
_MSP_CHANNELS = dict(
    wl_520="wl_520",
    wl_550="wl_550",
    wl_671="wl_671",
    wl_680="wl_680",
    wl_720="wl_720",
    wl_800="wl_800",
    wl_905="wl_905",
)
_NDVI_CHANNELS = dict(
    ndvi_720="ndvi_720",
    ndvi_800="ndvi_800",
    ndvi_905="ndvi_905",
)
_CHLA_CHANNELS = dict(chloro="chlorophyll")

CHANNELS_BY_SPACE = dict(
    hsv=_HSV_CHANNELS,
    lab=_LAB_CHANNELS,
    rgb=_RGB_CHANNELS,
    msp=_MSP_CHANNELS,
    ndvi=_NDVI_CHANNELS,
    chla=_CHLA_CHANNELS,
)
CHANNELS_FLAT = {
    **_HSV_CHANNELS,
    **_LAB_CHANNELS,
    **_RGB_CHANNELS,
    **_MSP_CHANNELS,
    **_NDVI_CHANNELS,
    **_CHLA_CHANNELS,
}

C_BLACK = (0, 0, 0)
C_BLUE = (255, 0, 0)
C_BLUE_VIOLET = (226, 43, 138)
C_CABIN_BLUE = (209, 133, 67)
C_CYAN = (255, 255, 0)
C_DIM_GRAY = (105, 105, 105)
C_FUCHSIA = (255, 0, 255)
C_GREEN = (0, 128, 0)
C_LIGHT_STEEL_BLUE = (222, 196, 176)
C_LIME = (0, 255, 0)
C_MAROON = (0, 0, 128)
C_ORANGE = (80, 127, 255)
C_PURPLE = (128, 0, 128)
C_RED = (0, 0, 255)
C_SILVER = (192, 192, 192)
C_TEAL = (128, 128, 0)
C_WHITE = (255, 255, 255)
C_YELLOW = (0, 255, 255)

all_colors_dict = dict(
    black=C_BLACK,
    blue=C_BLUE,
    blue_violet=C_BLUE_VIOLET,
    blue_cabin=C_CABIN_BLUE,
    cyan=C_CYAN,
    dim_grey=C_DIM_GRAY,
    fuchsia=C_FUCHSIA,
    green=C_GREEN,
    light_steel_blue=C_LIGHT_STEEL_BLUE,
    lime=C_LIME,
    maroon=C_MAROON,
    orange=C_ORANGE,
    purple=C_PURPLE,
    red=C_RED,
    silver=C_SILVER,
    teal=C_TEAL,
    white=C_WHITE,
    yellow=C_YELLOW,
)

ALL_COLORS = [v for v in all_colors_dict.values()]

TEST_IMG_IN_BOOL_OUT = "img_in_bool_out"
TEST_IMG_IN_IMG_OUT = "img_in_img_out"
TEST_IMG_IN_MSK_OUT = "img_in_msk_out"
TEST_OUTPUT_FOLDER = "output_folder"
TEST_SCR_IN_MSK_OUT = "script_in_msk_out"
TEST_SCR_IN_NFO_OUT = "script_in_info_out"
TEST_IMG_IN_ROI_OUT = "img_in_roi_out"
TEST_VIZ = "visualization"


def bgr_to_rgb(color: tuple) -> tuple:
    """Converts from BGR to RGB

    Arguments:
        color {tuple} -- Source color

    Returns:
        tuple -- Converted color
    """
    return (color[2], color[1], color[0])


def rgb_to_bgr(color: tuple) -> tuple:
    """Converts from RGB to BGR

    Arguments:
        color {tuple} -- Source color

    Returns:
        tuple -- Converted color
    """
    return (color[0], color[1], color[2])


def get_hr_channel_name(channel):
    """Returns human readable channel name

    Arguments:
        channel {str} -- channel short name

    Raises:
        NameError -- raise exception if unknown channel

    Returns:
        str -- human readable channel name
    """

    if channel in CHANNELS_BY_SPACE[HSV]:
        return f"hsv: {CHANNELS_FLAT[channel]}"
    elif channel in CHANNELS_BY_SPACE[LAB]:
        return f"lab: {CHANNELS_FLAT[channel]}"
    elif channel in CHANNELS_BY_SPACE[RGB]:
        return f"rgb: {CHANNELS_FLAT[channel]}"
    elif channel in CHANNELS_BY_SPACE[MSP]:
        return f"msp {CHANNELS_FLAT[channel]}"
    elif channel in CHANNELS_BY_SPACE[NDVI]:
        return f"ndvi {CHANNELS_FLAT[channel]}"
    elif channel in CHANNELS_BY_SPACE[CHLA]:
        return f"chla {CHANNELS_FLAT[channel]}"
    else:
        raise NameError("Unknown channel")


def get_channel_name(channel):
    """Returns human readable channel name

    Arguments:
        channel {str} -- channel short name

    Raises:
        NameError -- raise exception if unknown channel

    Returns:
        str -- human readable channel name
    """

    if channel in CHANNELS_BY_SPACE[HSV]:
        return CHANNELS_FLAT[channel]
    elif channel in CHANNELS_BY_SPACE[LAB]:
        return CHANNELS_FLAT[channel]
    elif channel in CHANNELS_BY_SPACE[RGB]:
        return CHANNELS_FLAT[channel]
    elif channel in CHANNELS_BY_SPACE[MSP]:
        return CHANNELS_FLAT[channel]
    elif channel in CHANNELS_BY_SPACE[NDVI]:
        return CHANNELS_FLAT[channel]
    elif channel in CHANNELS_BY_SPACE[CHLA]:
        return CHANNELS_FLAT[channel]
    else:
        raise NameError("Unknown channel")


def create_channel_generator(
    channels=(),
    include_vis: bool = True,
    include_ndvi: bool = False,
    include_msp: bool = False,
    include_chla: bool = False,
):
    """Create channel iterator, selection possible

    Keyword Arguments:
        channels {list} -- accepted channels, if None then all (default: {[]})
    """
    if channels:
        for cs_name, cs_data in CHANNELS_BY_SPACE.items():
            for channel_id, channel_name in cs_data.items():
                if (channel_id in channels) or not channels:
                    yield cs_name, channel_id, channel_name
    else:
        groups = []
        if include_vis:
            groups.extend((RGB, HSV, LAB))
        if include_msp:
            groups.append(MSP)
        if include_ndvi:
            groups.append(NDVI)
        if include_chla:
            groups.append(CHLA)

        for cs in groups:
            for k, v in CHANNELS_BY_SPACE[cs].items():
                if (k in channels) or not channels:
                    yield cs, k, v


def channel_color(channel: str):
    """
    Retruns a color cooresponding to the channel
    :param channel:
    :return:
    """
    if channel == "rd":
        return C_RED
    elif channel == "gr":
        return C_GREEN
    elif channel == "bl":
        return C_BLUE
    elif channel == "l":
        return C_DIM_GRAY
    elif channel == "a":
        return C_FUCHSIA
    elif channel == "b":
        return C_YELLOW
    elif channel == "h":
        return C_BLUE_VIOLET
    elif channel == "s":
        return C_CYAN
    elif channel == "v":
        return C_ORANGE
    elif channel == "wl_520":
        return (0x00, 0xFF, 0x36)
    elif channel == "wl_550":
        return (0x00, 0xFF, 0xA3)
    elif channel == "wl_671":
        return (0, 0, 200)
    elif channel == "wl_680":
        return (0x0, 0x0, 150)
    elif channel == "wl_720":
        return (125, 0x0, 150)
    elif channel == "wl_800":
        return (200, 0x0, 150)
    elif channel == "wl_905":
        return (255, 0x0, 150)
    elif channel == "ndvi_720":
        return (0x0, 180, 0x0)
    elif channel == "ndvi_800":
        return (0x0, 200, 0x0)
    elif channel == "ndvi_905":
        return (0x0, 220, 0x0)
    elif channel == "chlorophyll":
        return C_LIME
    else:
        return C_BLACK


def random_color(restrained: bool = True) -> tuple:
    """
    Retrurns a random color
    :param restrained: if True color will be selected from a list
    :return: tuple, BGR color
    """
    if restrained:
        return ALL_COLORS[random.randrange(0, len(ALL_COLORS))]
    else:
        return (
            random.randrange(0, 255),
            random.randrange(0, 255),
            random.randrange(0, 255),
        )


def scaled_rgb(mag, color_min, color_max):
    """ Return a tuple of integers, as used in AWT/Java plots. """
    try:
        x = float(mag - color_min) / (color_max - color_min)
    except ZeroDivisionError:
        logger.exception("Scaled rgb tried to divide by 0")
        x = 0.5  # color_max == color_min
    blue = min((max((4 * (0.75 - x), 0.0)), 1.0))
    red = min((max((4 * (x - 0.25), 0.0)), 1.0))
    green = min((max((4 * math.fabs(x - 0.5) - 1.0, 0.0)), 1.0))
    return int(red * 255), int(green * 255), int(blue * 255)


def build_color_steps(step_count: int) -> list:
    """
    Builds a list containing step_count different colors from blue to yellow
    :param step_count:
    :return:
    """
    if step_count <= 1:
        return [C_LIGHT_STEEL_BLUE]
    else:
        return [
            scaled_rgb(mag=i, color_min=0, color_max=step_count)
            for i in range(step_count)
        ]


def ensure_odd(
    i: int, min_val: Union[None, int] = None, max_val: Union[None, int] = None
) -> int:
    """Transforms an odd number into pair number by adding one

    Arguments:
        i {int} -- number

    Returns:
        int -- Odd number
    """
    if (i > 0) and (i % 2 == 0):
        i += 1
    if min_val is not None:
        return max(i, min_val)
    if max_val is not None:
        return min(i, max_val)
    return i


def resize_image(src_img, **kwargs):
    """
    Resizes image may keep aspect ration
    :param src_img:
    """

    target_rect = kwargs.get("target_rect", None)
    if target_rect is not None:
        w, h, ar = target_rect.width, target_rect.height, target_rect.ar
    else:
        w = kwargs.get("width", 100)
        h = kwargs.get("height", 100)
        ar = w / h
    keep_aspect_ratio = kwargs.get("keep_aspect_ratio", False) is True

    i_h, i_w = src_img.shape[:2]
    if keep_aspect_ratio and (ar > 0):
        i_ar = i_w / i_h
        if ar > i_ar:
            n_h = int(h)
            n_w = int(n_h * i_ar)
        else:
            n_w = int(w)
            n_h = int(n_w / i_ar)
    else:
        n_w = int(w)
        n_h = int(h)

    if (len(src_img.shape) == 2) and kwargs.get("output_as_bgr", True):
        src_img = cv2.cvtColor(src_img, cv2.COLOR_GRAY2BGR)

    src_img = cv2.resize(src_img, (n_w, n_h), interpolation=cv2.INTER_CUBIC)

    return src_img


def scale_image(src_img, scale_factor):
    return resize_image(
        src_img=src_img,
        width=round(src_img.shape[1] * scale_factor),
        height=round(src_img.shape[0] * scale_factor),
        keep_aspect_ratio=False,
        output_as_bgr=False,
    )


def enclose_image(a_cnv, img, rect, frame_width: int = 0):
    """Resize and copy source image to canvas rect while conserving aspect ratio

    Arguments:
        a_cnv {numpy array} -- target canvas
        img {numpy array} -- src image
        rect {TRect} -- enclosing rectangle

    Returns:
        numpy array -- modified target canvas
    """

    # old_h, old_w = img.shape[:2]
    # if (rect.width == old_w) and (rect.height == old_h):
    #     a_cnv = img.copy()
    # else:
    resized_image = resize_image(img.copy(), target_rect=rect, keep_aspect_ratio=True)
    n_h, n_w = resized_image.shape[:2]

    dx = int((rect.width - n_w) / 2)
    dy = int((rect.height - n_h) / 2)
    rect.inflate(-dx, -dx, -dy, -dy)
    rect.width = n_w
    rect.height = n_h
    a_cnv[rect.top : rect.bottom, rect.left : rect.right] = resized_image

    if frame_width:
        cv2.rectangle(
            img=a_cnv,
            pt1=(rect.left, rect.top),
            pt2=(rect.right, rect.bottom),
            color=(255, 255, 255),
            thickness=frame_width,
        )

    return a_cnv


def multi_and(image_list: tuple):
    """Performs an AND with all the images in the tuple

    :param image_list:
    :return: image
    """
    img_lst = [i for i in image_list if i is not None]
    list_len_ = len(img_lst)

    if list_len_ == 0:
        return None
    elif list_len_ == 1:
        return img_lst[0]
    else:
        res = cv2.bitwise_and(img_lst[0], img_lst[1])
        if len(img_lst) > 2:
            for current_image in img_lst[2:]:
                res = cv2.bitwise_and(res, current_image)

        return res


def multi_or(image_list: tuple):
    """Performs an OR with all the images in the tuple

    :param image_list:
    :return: image
    """
    img_lst = [i for i in image_list if i is not None]
    list_len_ = len(img_lst)

    if list_len_ == 0:
        return None
    elif list_len_ == 1:
        return img_lst[0]
    else:
        res = cv2.bitwise_or(img_lst[0], img_lst[1])
        if list_len_ > 2:
            for current_image in img_lst[2:]:
                res = cv2.bitwise_or(res, current_image)
        return res


def get_kernel(size: int, shape: int):
    """Builds morphology kernel

    :param size: kernel size, must be odd number
    :param shape: select shape of kernel
    :return: Morphology kernel
    """
    return cv2.getStructuringElement(shape, (size, size))


def open(
    image: Any,
    kernel_size: int = 3,
    kernel_shape: int = cv2.MORPH_ELLIPSE,
    rois: tuple = (),
    proc_times: int = 1,
):
    """Morphology - Open wrapper

    Arguments:
        image {numpy array} -- Source image
        kernel_size {int} -- kernel size
        kernel_shape {int} -- cv2 constant
        roi -- Region of Interrest
        proc_times {int} -- iterations

    Returns:
        numpy array -- opened image
    """
    morph_kernel = get_kernel(kernel_size, kernel_shape)
    if rois:
        result = image.copy()
        for roi in rois:
            r = roi.as_rect()
            result[r.top : r.bottom, r.left : r.right] = cv2.morphologyEx(
                result[r.top : r.bottom, r.left : r.right],
                cv2.MORPH_OPEN,
                morph_kernel,
                iterations=proc_times,
            )
    else:
        result = cv2.morphologyEx(
            image, cv2.MORPH_OPEN, morph_kernel, iterations=proc_times
        )
    return result


def close(
    image: Any,
    kernel_size: int = 3,
    kernel_shape: int = cv2.MORPH_ELLIPSE,
    rois: tuple = (),
    proc_times: int = 1,
):
    """Morphology - Close wrapper

    Arguments:
        image {numpy array} -- Source image
        kernel_size {int} -- kernel size
        kernel_shape {int} -- cv2 constant
        roi -- Region of Interest
        proc_times {int} -- iterations

    Returns:
        numpy array -- closed image
    """
    morph_kernel = get_kernel(kernel_size, kernel_shape)
    if rois:
        result = image.copy()
        for roi in rois:
            r = roi.as_rect()
            result[r.top : r.bottom, r.left : r.right] = cv2.morphologyEx(
                result[r.top : r.bottom, r.left : r.right],
                cv2.MORPH_CLOSE,
                morph_kernel,
                iterations=proc_times,
            )
    else:
        result = cv2.morphologyEx(
            image, cv2.MORPH_CLOSE, morph_kernel, iterations=proc_times
        )
    return result


def dilate(
    image: Any,
    kernel_size: int = 3,
    kernel_shape: int = cv2.MORPH_ELLIPSE,
    rois: tuple = (),
    proc_times: int = 1,
):
    """Morphology - Dilate wrapper

    Arguments:
        image {numpy array} -- Source image
        kernel_size {int} -- kernel size
        kernel_shape {int} -- cv2 constant
        roi -- Region of Interrest
        proc_times {int} -- iterations

    Returns:
        numpy array -- dilated image
    """
    morph_kernel = get_kernel(kernel_size, kernel_shape)
    if rois:
        result = image.copy()
        for roi in rois:
            if roi is not None:
                r = roi.as_rect()
                result[r.top : r.bottom, r.left : r.right] = cv2.dilate(
                    result[r.top : r.bottom, r.left : r.right],
                    morph_kernel,
                    iterations=proc_times,
                )
    else:
        result = cv2.dilate(image, morph_kernel, iterations=proc_times)
    return result


def erode(
    image: Any,
    kernel_size: int = 3,
    kernel_shape: int = cv2.MORPH_ELLIPSE,
    rois: tuple = (),
    proc_times: int = 1,
):
    """Morphology - Erode wrapper

    Arguments:
        image {numpy array} -- Source image
        kernel_size {int} -- kernel size
        kernel_shape {int} -- cv2 constant
        roi -- Region of Interrest
        proc_times {int} -- iterations

    Returns:
        numpy array -- eroded image
    """
    morph_kernel = get_kernel(kernel_size, kernel_shape)
    if rois:
        result = image.copy()
        for roi in rois:
            if roi is not None:
                r = roi.as_rect()
                result[r.top : r.bottom, r.left : r.right] = cv2.erode(
                    result[r.top : r.bottom, r.left : r.right],
                    morph_kernel,
                    iterations=proc_times,
                )
    else:
        result = cv2.erode(image, morph_kernel, iterations=proc_times)
    return result


def morphological_gradient(
    image: Any,
    kernel_size: int = 3,
    kernel_shape: int = cv2.MORPH_ELLIPSE,
    rois: tuple = (),
):
    """Morphology - Erode wrapper

    Arguments:
        image {numpy array} -- Source image
        kernel_size {int} -- kernel size
        kernel_shape {int} -- cv2 constant
        roi -- Region of Interrest
        proc_times {int} -- iterations

    Returns:
        numpy array -- eroded image
    """
    morph_kernel = get_kernel(kernel_size, kernel_shape)
    if rois:
        result = image.copy()
        for roi in rois:
            if roi is not None:
                r = roi.as_rect()
                result[r.top : r.bottom, r.left : r.right] = cv2.morphologyEx(
                    result[r.top : r.bottom, r.left : r.right],
                    cv2.MORPH_GRADIENT,
                    morph_kernel,
                )
    else:
        result = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, morph_kernel)
    return result


def get_contours(mask, retrieve_mode, method):
    return cv2.findContours(mask.copy(), retrieve_mode, method)[-2:-1][0]


def get_contours_and_hierarchy(mask, retrieve_mode, method):
    return cv2.findContours(mask.copy(), retrieve_mode, method)[-2:]


def group_contours(mask):
    """Gets contours from mask and merges them into single one"""
    id_objects, obj_hierarchy = get_contours_and_hierarchy(
        mask=mask, retrieve_mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE
    )

    stack = np.zeros((len(id_objects), 1))

    for c, cnt in enumerate(id_objects):
        if obj_hierarchy[0][c][2] == -1 and obj_hierarchy[0][c][3] > -1:
            stack[c] = 0
        else:
            stack[c] = 1
    ids = np.where(stack == 1)[0]
    if len(ids) > 0:
        return np.vstack([id_objects[i] for i in ids])
    else:
        return []


class MaskLineData(object):
    __slots__ = [
        "height_pos",
        "nz_span",
        "nz_count",
        "solidity",
        "last_span",
        "nz_pos",
        "tag",
    ]

    def __init__(self, line_number: int, line_data: list, last_span):
        ln_dt = np.nonzero(line_data)[0]
        self.height_pos = line_number
        self.nz_span = ln_dt[-1] - ln_dt[0] + 1 if len(ln_dt) > 0 else 0
        self.nz_count = len(ln_dt)
        self.solidity = self.nz_count / self.nz_span if self.nz_span != 0 else 0
        self.last_span = last_span
        self.nz_pos = ln_dt
        self.tag = "none"

    def __str__(self):
        return f"[height: {self.height_pos}][width: {self.nz_span}][solidity: {self.solidity}]"

    def __eq__(self, other):
        return np.array_equal(self.nz_pos, other.nz_pos)

    def is_inside(self, other):
        if other is None:
            return False
        if len(self.nz_pos) == 0:
            return True
        for i in self.nz_pos:
            if i not in other.nz_pos:
                return False
        return True

    def merge_and(self, line1, line2):
        if (line1 is None) or (line2 is None):
            ln_dt = np.array([])
        else:
            ln_dt = np.array([idx for idx in line1.nz_pos if idx in line2.nz_pos])
        self.nz_span = ln_dt[-1] - ln_dt[0] + 1 if len(ln_dt) > 0 else 0
        self.nz_count = len(ln_dt)
        self.solidity = self.nz_count / self.nz_span if self.nz_span != 0 else 0
        self.nz_pos = ln_dt

    def merge_or(self, line1, line2):
        ln_dt = []
        if line1 is not None:
            ln_dt = ln_dt + [idx for idx in line1.nz_pos]
        if line2 is not None:
            ln_dt = ln_dt + [idx for idx in line2.nz_pos]
        ln_dt = np.array(sorted(list(set(ln_dt))))
        self.nz_span = ln_dt[-1] - ln_dt[0] + 1 if len(ln_dt) > 0 else 0
        self.nz_count = len(ln_dt)
        self.solidity = self.nz_count / self.nz_span if self.nz_span != 0 else 0
        self.nz_pos = ln_dt

    def clear(self):
        self.nz_span = 0
        self.nz_count = 0
        self.solidity = 0
        self.nz_pos = []
        self.tag = "none"


class MaskData(object):
    def __init__(self, mask):
        self._height = None
        self._width = None
        self._is_continuous = True
        self._lines_data = []
        self._mask = mask
        last_span_ = 0
        for line_number, line in enumerate(mask):
            # Build line data
            cur_ln_dt = MaskLineData(line_number, line, last_span_)
            if (cur_ln_dt.nz_count == 0) and (len(self._lines_data) == 0):
                continue
            last_span_ = cur_ln_dt.nz_span
            self._lines_data.append(cur_ln_dt)
        if self.lines_data:
            while self.lines_data[-1].nz_count == 0:
                del self.lines_data[-1]

    def to_mask(self, first_line=-1, last_line=-1, colour=255):
        msk_out = np.zeros_like(self.mask)
        if first_line == -1:
            first_line = 0
        if last_line == -1:
            last_line = self.mask_height
        for line in self.lines_data[first_line:last_line]:
            for i in line.nz_pos:
                msk_out[line.height_pos][i] = colour
        return msk_out

    def find_by_height(self, height):
        for ld in self._lines_data:
            if ld.height_pos == height:
                return ld
        return None

    def find_top_bottom_non_full_lines(self, height):
        ld = self.find_by_height(height=height)
        if ld is None:
            return None, None
        ht = height - 1
        ld_up = self.find_by_height(height=ht)
        while (ld_up is not None) and ld.is_inside(ld_up) and (ht > self.top_index):
            ht -= 1
            ld_up = self.find_by_height(height=ht)
        ht = height + 1
        ld_down = self.find_by_height(height=ht)
        while (
            (ld_down is not None) and ld.is_inside(ld_down) and (ht < self.bottom_index)
        ):
            ht += 1
            ld_down = self.find_by_height(height=ht)
        return ld_up, ld_down

    def horizontal_lines_at(
        self, height: int, min_length: int = 1, fully_isolated: bool = True
    ):
        res = False
        try:
            # Get the lines we need
            ld = self.find_by_height(height=height)
            if ld is None or (ld.nz_count < min_length):
                res = None

            if ld.solidity >= 0.99:
                ld_up, ld_down = self.find_top_bottom_non_full_lines(height)
            else:
                ld_up = self.find_by_height(height=height - 1)
                ld_down = self.find_by_height(height=height + 1)

            # Build line candidates spans
            run = []
            runs = [run]
            expect = None
            top_nok = False
            bottom_nok = False
            for v in ld.nz_pos:
                is_continuous = (v == expect) or (expect is None)
                if (ld_up is not None) and (v in ld_up.nz_pos):
                    top_nok = True
                if (ld_down is not None) and (v in ld_down.nz_pos):
                    bottom_nok = True
                neighbors_nok = (fully_isolated and (top_nok or bottom_nok)) or (
                    top_nok and bottom_nok
                )
                if is_continuous and not neighbors_nok:
                    run.append(v)
                else:
                    run = [v]
                    runs.append(run)
                    top_nok = False
                    bottom_nok = False
                expect = v + 1

            res = [
                (ld.height_pos, run[0], run[-1]) for run in runs if len(run) >= min_length
            ]
        except Exception as e:
            logger.exception(f"Raised {repr(e)}")
            res = None
        finally:
            return res

    def percent_height(self, percent: float):
        return self.bottom_index - self.height * percent

    def get_pos_height(self, value):
        if isinstance(value, int):
            return value
        elif isinstance(value, float) and (value <= 1):
            return self.percent_height(value)
        else:
            return None

    def line_at(self, i):
        i = self.get_pos_height(i)
        if i is None:
            return 0
        return self.find_by_height(i)

    def width_at(self, i):
        ld = self.line_at(i)
        if ld:
            return ld.nz_span
        else:
            return 0

    def nz_count_at(self, i):
        ld = self.line_at(i)
        if ld:
            return ld.nz_count
        else:
            return 0

    def is_full_line(self, height):
        ld = self.find_by_height(height=height)
        return (ld is not None) and (ld.nz_count == self.width)

    def height_quantile_mask(self, total, index, colour=255):
        """
        Returns portion of mask in quantile target
        :param total: quantile total
        :param index: quantile index
        :param tag: update parsed lines tags with this value
        :return: numpy array
        """
        splits = np.array_split(
            np.array(range(self.top_index, self.bottom_index + 1)), total
        )
        start, stop = splits[index][0], splits[index][-1] + 1

        return self.to_mask(
            first_line=start - self.top_index,
            last_line=stop - self.top_index,
            colour=colour,
        )

    def width_quantile_stats(self, total, index, tag=None):
        """
        Returns width statistics for the plant
        :param total: quantile total
        :param index: quantile index
        :param tag: update parsed lines tags with this value
        :return: total, solidity, min, max, average & standard deviation
        """
        splits = np.array_split(
            np.array(range(self.top_index, self.bottom_index + 1)), total
        )
        start, stop = splits[index][0], splits[index][-1] + 1

        dt = np.array([self.width_at(idx) for idx in range(start, stop)])
        means, std_devs = cv2.meanStdDev(dt)

        area_ = np.sum(np.array([self.nz_count_at(idx) for idx in range(start, stop)]))
        hullish_ = np.sum(np.array([self.width_at(idx) for idx in range(start, stop)]))

        if tag is not None:
            for idx in range(start, stop):
                ld = self.line_at(idx)
                if ld is not None:
                    ld.tag = tag

        return (
            area_,
            hullish_,
            area_ / hullish_,
            np.min(dt),
            np.max(dt),
            means[0][0],
            std_devs[0][0],
        )

    @property
    def lines_data(self):
        return self._lines_data

    @property
    def height(self):
        if self._height is None:
            if self._lines_data:
                self._height = self.bottom_index - self.top_index
            else:
                self._height = 0
        return self._height

    @property
    def width(self):
        if self._width is None:
            if self._lines_data:
                max_width_ = 0
                for ld in self._lines_data:
                    if ld.nz_span > max_width_:
                        max_width_ = ld.nz_span
                self._width = max_width_
            else:
                self._width = 0
        return self._width

    @property
    def mask_width(self):
        return self._mask.shape[1] if self._mask is not None else 0

    @property
    def mask_height(self):
        return self._mask.shape[0] if self._mask is not None else 0

    @property
    def is_continuous(self):
        return self._is_continuous

    @property
    def top_index(self):
        if len(self._lines_data) > 0:
            return self._lines_data[0].height_pos
        else:
            return 0

    @property
    def bottom_index(self):
        if len(self._lines_data) > 0:
            return self._lines_data[-1].height_pos
        else:
            return 0

    @property
    def mask(self):
        return self._mask

    @property
    def area(self):
        return (
            np.sum(np.array([l.nz_count for l in self.lines_data]))
            if len(self._lines_data) > 0
            else 0
        )


class DefaultCsvWriter(AbstractCsvWriter):
    def __init__(self):
        super().__init__()
        self.data_list = dict.fromkeys(AVAILABLE_FEATURES)
