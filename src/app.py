from dataclasses import dataclass
from enum import auto, Enum

import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.use('svg')


class Mode(Enum):
    RECT = auto()
    CIRCLE = auto()
    SPLINE = auto()


@dataclass
class State:
    x: float = 0.
    y: float = 0.
        
        
class InteractiveMplChart(ft.Container):
    def __init__(
        self,
        **kwargs
    ):
        self.start_point = State()
        self.current_point = State()
        
        self.fig, self.ax = plt.subplots(1, 1, figsize=(4,4))
            
        self.ax.plot([-10, 10], [0, 20])
        self.vspan = self.ax.axvspan(0, 0, color='blue', alpha=0.1, lw=0.5)
        self.vspan.set_visible(False)
        self.points = self.ax.scatter([], [], c='red')

        self.ax.set_xlim(-40, 40)
        self.ax.set_ylim(-40, 40)
        self.ax.set_aspect('equal')
        self.fig.tight_layout()
        
        self.chart = MatplotlibChart(self.fig, expand=False)
        
        gd = ft.GestureDetector(
            drag_interval=20,
            on_pan_start=self._pan_start,
            on_pan_update=self._pan_update,
            on_pan_end=self._pan_end,
            on_tap_down=self._on_clicked,
            on_double_tap_down=self._on_double_clicked,
        )
        super().__init__(content=ft.Stack([gd, ft.TransparentPointer(self.chart)]),
                         expand=False,
                         **kwargs
                         )
        
    def _modify_vspan(self, x1, x2) -> np.ndarray:
        xy = np.array([[x1, 0.],
                       [x1, 1.],
                       [x2, 1.],
                       [x2, 0.],
                       [x1, 0.]])
        self.vspan.set_xy(xy)
        
    def _pixel_to_coord(self, clicked_x, clicked_y) -> tuple[float, float]:
        axis_bbox = self.ax.get_position()

        x_rel = (clicked_x / self.width - axis_bbox.x0) / axis_bbox.width
        y_rel = ((1 - clicked_y / self.height) - axis_bbox.y0) / axis_bbox.height
        
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        
        x = (xmax - xmin) * x_rel + xmin
        y = (ymax - ymin) * y_rel + ymin
        return x, y
        
    def _on_clicked(self, e: ft.TapEvent) -> None:
        print(f'clicked: ({e.local_x=}, {e.local_y=})')
        print(self._pixel_to_coord(e.local_x, e.local_y))
        
    def _on_double_clicked(self, e: ft.TapEvent) -> None:
        print(f'double_clicked')
        
    def _pan_start(self, e: ft.DragStartEvent) -> None:
        x, y = self._pixel_to_coord(e.local_x, e.local_y)
        self.start_point.x = x
        self.start_point.y = y
        
        self.vspan.set_visible(True)
        print(f'pan_started: ({e.local_x=}, {e.local_y=})')

    def _pan_update(self, e: ft.DragUpdateEvent) -> None:
        x, y = self._pixel_to_coord(e.local_x, e.local_y)
        self.current_point.x = x
        self.current_point.y = y
        self._modify_vspan(self.start_point.x, self.current_point.x)
        # print(f'pan_updated: ({e.local_x=}, {e.local_y=})')
        self.chart.update()
        
    def _pan_end(self, e: ft.DragEndEvent) -> None:
        print(f'pan_ended: ({self.start_point=}, {self.current_point=})')
    
    
class InteractiveImage():
    def __init__(self):
        pass
        

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
        self.page.update()
        
    # def _pan_start(self, e: ft.DragStartEvent) -> None:
    #     self.start_point.x = e.local_x
    #     self.start_point.y = e.local_y
    #     print(f'pan_started: ({e.local_x=}, {e.local_y=})')

    # def _pan_update(self, e: ft.DragUpdateEvent) -> None:
    #     self.current_point.x = e.local_x
    #     self.current_point.y = e.local_y
    #     print(f'pan_updated: ({e.local_x=}, {e.local_y=})')
        
    # def _on_clicked(self, e: ft.TapEvent) -> None:
    #     # self.points.points.append(ft.Offset(e.local_x, e.local_y))
    #     # self.canvas.shapes.append(cv.Points([ft.Offset(e.local_x, e.local_y)],
    #     #                                     point_mode=cv.PointMode.POINTS,
    #     #                                     paint=ft.Paint(color=ft.colors.RED, stroke_width=10)
    #     #                                     ))
    #     # self.canvas.update()
    #     # print(self.canvas.shapes)
    #     print(f'clicked: ({e.local_x=}, {e.local_y=})')
        
    # def _on_double_clicked(self, e: ft.TapEvent) -> None:
    #     print(f'double_clicked')
        
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
        
        # gd1 = ft.GestureDetector(
        #     drag_interval=10,
        #     on_pan_start=self._pan_start,
        #     on_pan_update=self._pan_update,
        #     on_tap_down=self._on_clicked,
        #     on_double_tap_down=self._on_double_clicked,
        #     # width=500,
        #     # height=500,
        #     expand=True
        # )
        
        # fig, ax = plt.subplots(1, 1)
        # ax.plot([0, 1], [0, 1])
        # plt.tight_layout()
        # self.chart = MatplotlibChart(fig, expand=True)
        
        # self.points = cv.Points(point_mode=cv.PointMode.POINTS,
        #                         paint=ft.Paint(color=ft.colors.RED, stroke_width=10))
        # self.canvas = cv.Canvas([self.points],
        #                         content=gd1
        #                         )
        self.chart = InteractiveMplChart(width=640, height=640,
                                         bgcolor=ft.colors.AMBER
                                         )

        self.page.add(
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Container(self.chart, bgcolor=ft.colors.BLUE, expand=False)
                    # ft.Stack([
                    #     ft.TransparentPointer(self.chart),
                    #     gd1,
                    # ], width=1000,
                    #     height=1000)
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.START
            )
        )


def main(page: ft.Page):
    app = App(page)
    app.run()


ft.app(target=main, view=ft.WEB_BROWSER)