from enum import StrEnum

class Storage(StrEnum):
    AIO = "aio"
    ADOBE = "adobe"
    EXTERNAL = "external"
    AZURE = "azure"
    DROPBOX = "dropbox"


class MimeType(StrEnum):
    DNG = "image/x-adobe-dng"
    JPEG = "image/jpeg"
    PNG = "image/png"
    PSD = "image/vnd.adobe.photoshop"
    TIFF = "image/tiff"


class PngCompression(StrEnum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Colorspace(StrEnum):
    BITMAP = "bitmap"
    GREYSCALE = "greyscale"
    INDEXED = "indexed"
    RGB = "rgb"
    CMYK = "cmyk"
    MULTICHANNEL = "multichannel"
    DUOTONE = "duotone"
    LAB = "lab"


class StandardIccProfileNames(StrEnum):
    ADOBE_RGB_1998 = "Adobe RGB (1998)"
    APPLE_RGB = "Apple RGB"
    COLORMATCH_RGB = "ColorMatch RGB"
    SRGB = "sRGB IEC61966-2.1"
    DOTGAIN_10 = "Dot Gain 10%"
    DOTGAIN_15 = "Dot Gain 15%"
    DOTGAIN_20 = "Dot Gain 20%"
    DOTGAIN_25 = "Dot Gain 25%"
    DOTGAIN_30 = "Dot Gain 30%"
    GRAY_GAMMA_18 = "Gray Gamma 1.8"
    GRAY_GAMMA_22 = "Gray Gamma 2.2"


class CreateMaskType(StrEnum):
    BINARY = "binary"
    SOFT = "soft"


class WhiteBalance(StrEnum):
    AS_SHOT = "As Shot"
    AUTO = "Auto"
    CLOUDY = "Cloudy"
    CUSTOM = "Custom"
    DAYLIGHT = "Daylight"
    FLASH = "Flash"
    FLUORESCENT = "Fluorescent"
    SHADE = "Shade"
    TUNGSTEN = "Tungsten"


class ManageMissingFonts(StrEnum):
    USE_DEFAULT = "useDefault"
    FAIL = "fail"


class BackgroundFill(StrEnum):
    WHITE = "white"
    BACKGROUND_COLOR = "backgroundColor"
    TRANSPARENT = "transparent"


class LayerType(StrEnum):
    LAYER = "layer"
    TEXT_LAYER = "textLayer"
    ADJUSTMENT_LAYER = "adjustmentLayer"
    LAYER_SECTION = "layerSection"
    SMART_OBJECT = "smartObject"
    BACKGROUND_LAYER = "backgroundLayer"
    FILL_LAYER = "fillLayer"


class BlendMode(StrEnum):
    NORMAL = "normal"
    DISSOLVE = "dissolve"
    DARKEN = "darken"
    MULTIPLY = "multiply"
    COLOR_BURN = "colorBurn"
    LINEAR_BURN = "linearBurn"
    DARKER_COLOR = "darkerColor"
    LIGHTEN = "lighten"
    SCREEN = "screen"
    COLOR_DODGE = "colorDodge"
    LINEAR_DODGE = "linearDodge"
    LIGHTER_COLOR = "lighterColor"
    OVERLAY = "overlay"
    SOFT_LIGHT = "softLight"
    HARD_LIGHT = "hardLight"
    VIVID_LIGHT = "vividLight"
    LINEAR_LIGHT = "linearLight"
    PIN_LIGHT = "pinLight"
    HARD_MIX = "hardMix"
    DIFFERENCE = "difference"
    EXCLUSION = "exclusion"
    SUBTRACT = "subtract"
    DIVIDE = "divide"
    HUE = "hue"
    SATURATION = "saturation"
    COLOR = "color"
    LUMINOSITY = "luminosity"


class TextOrientation(StrEnum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class ParagraphAlignment(StrEnum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    JUSTIFY_LEFT = "justifyLeft"
    JUSTIFY_CENTER = "justifyCenter"
    JUSTIFY_RIGHT = "justifyRight"


class HorizontalAlignment(StrEnum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class VerticalAlignment(StrEnum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


class JobOutputStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    UPLOADING = "uploading"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
