from pxr import Gf, UsdGeom
from omni.usd import get_context

import omni.kit.app
import omni.appwindow
import carb.input

PLAYER_PATH = "/World/PLAYER"

MOVE_STEP = 0.5
ZOOM_STEP = 500.0

move_state = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "zoom_in": False,
    "zoom_out": False,
}

app_window = omni.appwindow.get_default_app_window()
keyboard = app_window.get_keyboard()

input_iface = carb.input.acquire_input_interface()


def on_key(event, *args):

    if event.type == carb.input.KeyboardEventType.KEY_PRESS:

        if event.input == carb.input.KeyboardInput.UP:
            move_state["up"] = True

        elif event.input == carb.input.KeyboardInput.DOWN:
            move_state["down"] = True

        elif event.input == carb.input.KeyboardInput.LEFT:
            move_state["left"] = True

        elif event.input == carb.input.KeyboardInput.RIGHT:
            move_state["right"] = True

        elif event.input == carb.input.KeyboardInput.A:
            move_state["zoom_in"] = True
            print("ZOOM IN")

        elif event.input == carb.input.KeyboardInput.D:
            move_state["zoom_out"] = True
            print("ZOOM OUT")

    elif event.type == carb.input.KeyboardEventType.KEY_RELEASE:

        if event.input == carb.input.KeyboardInput.UP:
            move_state["up"] = False

        elif event.input == carb.input.KeyboardInput.DOWN:
            move_state["down"] = False

        elif event.input == carb.input.KeyboardInput.LEFT:
            move_state["left"] = False

        elif event.input == carb.input.KeyboardInput.RIGHT:
            move_state["right"] = False

        elif event.input == carb.input.KeyboardInput.A:
            move_state["zoom_in"] = False

        elif event.input == carb.input.KeyboardInput.D:
            move_state["zoom_out"] = False


keyboard_sub = input_iface.subscribe_to_keyboard_events(
    keyboard,
    on_key
)


def on_update(event):

    stage = get_context().get_stage()

    player = stage.GetPrimAtPath(PLAYER_PATH)

    if not player.IsValid():
        print("PLAYER NOT FOUND")
        return

    xform = UsdGeom.Xformable(player)

    translate_op = None

    for op in xform.GetOrderedXformOps():

        if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
            translate_op = op
            break

    if translate_op is None:
        print("NO TRANSLATE OP")
        return

    pos = translate_op.Get()

    if move_state["up"]:
        pos += Gf.Vec3d(0, 0, MOVE_STEP)

    if move_state["down"]:
        pos += Gf.Vec3d(0, 0, -MOVE_STEP)

    if move_state["left"]:
        pos += Gf.Vec3d(MOVE_STEP, 0, 0)

    if move_state["right"]:
        pos += Gf.Vec3d(-MOVE_STEP, 0, 0)

    if move_state["zoom_in"]:
        pos += Gf.Vec3d(0, 0, ZOOM_STEP)

    if move_state["zoom_out"]:
        pos += Gf.Vec3d(0, 0, -ZOOM_STEP)

    translate_op.Set(pos)


app = omni.kit.app.get_app()

update_sub = app.get_update_event_stream().create_subscription_to_pop(
    on_update,
    name="PlayerMovement"
)

print("PLAYER MOVEMENT ACTIVE")
print("UP = FORWARD")
print("DOWN = BACKWARD")
print("LEFT = LEFT")
print("RIGHT = RIGHT")
print("A = ZOOM IN")
print("D = ZOOM OUT")

