DEFAULT_IDLE_WAVING_ANGLE = 1.0
MIN_IDLE_WAVING_ANGLE = -360.0
MAX_IDLE_WAVING_ANGLE = 360.0

DEFAULT_IDLE_WAVING_DURATION = 2.0
MIN_IDLE_WAVING_DURATION = 0.01
MAX_IDLE_WAVING_DURATION = 60.0
IDLE_WAVING_DURATION_PRECISION = 2

IDLE_WAVING_INTERPOLATION_ITEMS = (
	("BEZIER", "Bezier", "Smooth Bezier interpolation"),
	("LINEAR", "Linear", "Linear interpolation"),
	("SINE", "Sine", "Sine easing"),
	("QUAD", "Quadratic", "Quadratic easing"),
	("CUBIC", "Cubic", "Cubic easing"),
)
DEFAULT_IDLE_WAVING_INTERPOLATION = "BEZIER"

IDLE_WAVING_EASING_ITEMS = (
	("AUTO", "Automatic", "Automatic easing"),
	("EASE_IN", "Ease In", "Accelerate at the start"),
	("EASE_OUT", "Ease Out", "Decelerate at the end"),
	("EASE_IN_OUT", "Ease In Out", "Accelerate and decelerate"),
)
DEFAULT_IDLE_WAVING_EASING = "EASE_IN_OUT"