import bpy

from ....properties.ui.types import DancerSelectionType
from ...states import state


def move_current_frame_to_min_loaded_frame():
    if bpy.context is None or bpy.context.scene is None:
        return
    bpy.context.scene.frame_set(state.dancer_load_frames[0])


def show_full_min_max_frame():
    if bpy.context is None:
        return
    dopesheet_editor = next(
        a for a in bpy.context.screen.areas if a.type == "DOPESHEET_EDITOR"
    )
    region = next(r for r in dopesheet_editor.regions if r.type == "WINDOW")
    space = dopesheet_editor.spaces[0]
    with bpy.context.temp_override(area=dopesheet_editor, region=region, space=space):
        bpy.ops.anim.scene_range_frame()


# set frame by such way does not trigger limits of frame_range_min/max
def set_min_max_frame(min: int, max: int):
    if not bpy.context or min >= max:
        return

    setattr(bpy.context.window_manager, "ld_ui_frame_range_min", 0)
    setattr(bpy.context.window_manager, "ld_ui_frame_range_max", max)
    setattr(bpy.context.window_manager, "ld_ui_frame_range_min", min)
    show_full_min_max_frame()


def set_loaded_frame_at_full_range():
    music_frame = state.partial_load_frames
    state.dancer_load_frames = music_frame

    set_min_max_frame(music_frame[0], music_frame[1])

    if not bpy.context:
        return


def set_state_of_loaded_frame_range():
    if not bpy.context:
        return

    min_frame = getattr(bpy.context.window_manager, "ld_ui_frame_range_min")
    max_frame = getattr(bpy.context.window_manager, "ld_ui_frame_range_max")
    state.dancer_load_frames = (min_frame, max_frame)

    if not bpy.context:
        return


def init_loaded_frame_range():
    if not bpy.context:
        return

    music_frame = state.partial_load_frames
    if bpy.context.scene.frame_start == 1 and bpy.context.scene.frame_end == 250:
        set_min_max_frame(music_frame[0], music_frame[1])
    else:
        set_min_max_frame(bpy.context.scene.frame_start, bpy.context.scene.frame_end)


def init_show_dancer():
    state.show_dancers = [True] * len(state.dancer_names)

    if bpy.context is None:
        return

    dancer_selection = getattr(bpy.context.window_manager, "ld_ui_dancers_selection")
    dancer_selection.clear()
    for dancer in state.dancer_names:
        dancer_selection_item: DancerSelectionType = getattr(
            bpy.context.window_manager, "ld_ui_dancers_selection"
        ).add()
        dancer_selection_item.name = dancer
        dancer_selection_item.shown = True


# Set state.show_dancers from ld_ui_dancers_selection
def set_state_of_dancer_selection():
    if not bpy.context:
        return
    dancer_props: list[DancerSelectionType] = getattr(
        bpy.context.window_manager, "ld_ui_dancers_selection"
    )

    show_dancer = [dancer.shown for dancer in dancer_props]
    state.show_dancers = show_dancer


def init_dancer_selection_from_state():
    if not bpy.context:
        return
    dancer_props: list[DancerSelectionType] = getattr(
        bpy.context.window_manager, "ld_ui_dancers_selection"
    )

    if not dancer_props:
        for dancer in state.dancer_names:
            dancer_selection_item: DancerSelectionType = getattr(
                bpy.context.window_manager, "ld_ui_dancers_selection"
            ).add()
            dancer_selection_item.name = dancer
            dancer_selection_item.shown = True
    else:
        return
