from dataclasses import dataclass
from enum import auto, Enum

import flet as ft
import flet.canvas as cv


class Mode(Enum):
    RECT = auto()
    CIRCLE = auto()
    SPLINE = auto()


@dataclass
class State:
    x: float = 0.
    y: float = 0.
        

class App():
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.page.title = 'Flet Practice'
        self.mode = Mode.RECT
        self.start_point = State()
        self.current_point = State()
        
    def _on_mode_selected(self, e: ft.ControlEvent) -> None:
        print(e)
        self.mode = Mode(e.control.selected_index+1)
        print(f'mode changed: {self.mode}')
        
    def _pan_start(self, e: ft.DragStartEvent) -> None:
        self.start_point.x = e.local_x
        self.start_point.y = e.local_y
        print(f'pan_started: ({e.local_x=}, {e.local_y=})')

    def _pan_update(self, e: ft.DragUpdateEvent) -> None:
        self.current_point.x = e.local_x
        self.current_point.y = e.local_y
        print(f'pan_updated: ({e.local_x=}, {e.local_y=})')
        
    def _on_clicked(self, e: ft.TapEvent) -> None:
        self.points.points.append(ft.Offset(e.local_x, e.local_y))
        # self.canvas.shapes.append(cv.Points([ft.Offset(e.local_x, e.local_y)],
        #                                     point_mode=cv.PointMode.POINTS,
        #                                     paint=ft.Paint(color=ft.colors.RED, stroke_width=10)
        #                                     ))
        self.canvas.update()
        print(self.canvas.shapes)
        print(f'clicked')
        
    def _on_double_clicked(self, e: ft.TapEvent) -> None:
        print(f'double_clicked')
        
    def run(self):
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            # extended=True,
            min_width=100,
            min_extended_width=400,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.FAVORITE_BORDER,
                    selected_icon=ft.icons.FAVORITE,
                    label='Rect'
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label='Circle'
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label='Spline'
                ),
            ],
            on_change=self._on_mode_selected,
        )
        
        gd1 = ft.GestureDetector(
            drag_interval=10,
            on_pan_start=self._pan_start,
            on_pan_update=self._pan_update,
            on_tap_down=self._on_clicked,
            on_double_tap_down=self._on_double_clicked
        )
        
        self.points = cv.Points(point_mode=cv.PointMode.POINTS,
                                paint=ft.Paint(color=ft.colors.RED, stroke_width=10))
        self.canvas = cv.Canvas([self.points],
                                content=gd1
                                )
        

        self.page.add(
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    self.canvas,
                ],
                expand=True,
            )
        )


def main(page: ft.Page):
    app = App(page)
    app.run()


ft.app(main, view=ft.WEB_BROWSER)