from enum import StrEnum


class RobotCommand(StrEnum):
    MOVE_FORWARD = "move_forward"
    MOVE_BACKWARD = "move_backward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    STOP = "stop"
    SPEED_UP = "speed_up"
    SLOW_DOWN = "slow_down"
