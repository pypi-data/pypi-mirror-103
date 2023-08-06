from collections.abc import Iterable
import base64
import math
import numpy as np
import pyglet
import re
import textwrap

from .graph import Graph, Vertex
from .point import dist


WIDTH = 960
HEIGHT = 720
FPS = 60
DEFAULT_ANIMATION_DURATION = 0.5


VERT_COLOR = (127, 127, 127)
HOVERED_VERT_COLOR = (255, 0, 0)
EDGE_COLOR = (95, 95, 95)
HOVERED_EDGE_COLOR = (127, 127, 127)
FLIPPABLE_EDGE_COLOR = (63, 63, 255)
GHOST_EDGE_COLOR = (47, 47, 47)
CROSS_EDGE_COLOR = (127, 47, 47)
WARNING_TEXT_COLOR = (255, 0, 127, 255)

VERT_RADIUS = 3.0
HOVERED_VERT_RADIUS = 4.0
EDGE_RADIUS = 1.0
HOVERED_EDGE_RADIUS = 1.5
HOVERED_EDGE_RADIUS_FLIPPABLE = 2.0
GHOST_EDGE_RADIUS = 1.0

VERTEX_HOVER_RADIUS = 15.0
EDGE_HOVER_RADIUS = 10.0


class VisualizationWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(
            width=WIDTH,
            height=HEIGHT,
            config=pyglet.gl.Config(sample_buffers=1, samples=4),
            file_drops=True,
        )

        # UI elements
        self.instructions_label = pyglet.text.Label(
            "",
            x=10,
            y=self.height - 10,
            multiline=True,
            width=1000,
            anchor_x='left',
            anchor_y='top',
        )
        self.colinear_warning_label = pyglet.text.Label(
            base64.b64decode("Q29saW5lYXIgcG9pbnRzPwoKTk9UIEJZIFRIRSB"
                             + "IQUlSIE9GIE1ZIENISU5OWSBDSElOIENISU4=").decode('utf-8'),
            x=self.width // 2,
            y=self.height // 2,
            multiline=True,
            width=self.width,
            align='center',
            anchor_x='center',
            anchor_y='center',
            bold=True,
            font_size=20,
            color=WARNING_TEXT_COLOR,
        )

        # Visualization state
        self.graph = Graph()
        self.animation_multiplier = 1
        self.mouse_pos = np.array([0.0, 0.0])
        self.hover_target = None

        # Animation state
        self.animation_progress = 0.0
        self.animation_queue = []
        self.replay_lines = []
        self.warning_text_countdown = 0.0

        pyglet.clock.schedule_interval(self.step_animation, 1/FPS)

    ###########################################################################
    # INPUT

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.F and self.animation_multiplier < 4:
            self.animation_multiplier *= 5 ** (1/4)
        if symbol == pyglet.window.key.S and self.animation_multiplier > 1/4:
            self.animation_multiplier /= 5 ** (1/4)

    def on_mouse_motion(self, x, y, dx, dy):
        self.update_nearest_thing(x, y)

    def on_mouse_drag(self, x, y, *args, **kwargs):
        self.update_nearest_thing(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button != pyglet.window.mouse.LEFT:
            return
        if self.animation_queue:
            return
        if isinstance(self.hover_target, tuple):
            if self.graph.can_flip(*self.hover_target):
                self.enqueue_anim('flip', self.hover_target)
        if isinstance(self.hover_target, Vertex):
            self.enqueue_anim('remove', self.hover_target)
        if self.hover_target is None and not self.graph.hull_contains(*self.mouse_pos):
            self.enqueue_anim('add', self.mouse_pos)
        self.update_nearest_thing(x, y)

    def on_file_drop(self, x, y, paths):
        for path in paths:
            with open(path) as f:
                self.replay_lines += list(f)

    def update_nearest_thing(self, x=None, y=None):
        if x is not None and y is not None:
            self.mouse_pos = np.array([float(x), float(y)])

        if self.animation_queue:
            self.hover_target = None
            return

        nearest_vertex = None
        if self.graph.vertices:
            nearest_vertex = min(
                self.graph.vertices,
                key=lambda v: dist(self.mouse_pos, v.loc),
            )
            if dist(self.mouse_pos, nearest_vertex.loc) > VERTEX_HOVER_RADIUS:
                nearest_vertex = None

        nearest_edge = None
        nearest_edge_dist = EDGE_HOVER_RADIUS
        for (a, b) in self.graph.edges():
            edge_dist = dist_point_to_line_segment(
                a.loc, b.loc, self.mouse_pos,
            )
            if edge_dist is not None and edge_dist < nearest_edge_dist:
                nearest_edge = (a, b)
                nearest_edge_dist = edge_dist

        self.hover_target = nearest_vertex or nearest_edge

    ###########################################################################
    # RENDERING

    def on_draw(self):
        self.clear()

        # Update and draw text
        self.update_instructions_text()
        self.instructions_label.draw()
        if self.warning_text_countdown > 0.0:
            self.colinear_warning_label.draw()

        # Initialize draw lists
        self.vertex_coords = []
        self.vertex_colors = []
        self.draw_indices = []

        # Draw order (lowest to highest):
        # - "ghost" edges
        # - graph edges
        # - graph vertices

        # Draw ghost edges
        if self.animation_queue:
            for action, loc in self.animation_queue:
                if action == 'add':
                    self.draw_ghost_edges(loc)
                    break
                if action == 'remove':
                    break
        elif self.hover_target is None:
            self.draw_ghost_edges(self.mouse_pos)

        # Draw edges in the graph
        for e in self.graph.edges():
            if e == self.hover_target or self.is_flip_queued(e):
                radius = HOVERED_EDGE_RADIUS
                if self.graph.can_flip(*e):
                    color = FLIPPABLE_EDGE_COLOR
                else:
                    color = HOVERED_EDGE_COLOR
            else:
                radius = EDGE_RADIUS
                color = EDGE_COLOR
            if self.is_next_flip_queued(e):
                self.draw_graph_edge_flip_animation(*e, radius, color)
            else:
                v1, v2 = e
                self.draw_graph_edge(v1.loc, v2.loc, radius, color)

        # Draw vertices in the graph
        for v in self.graph.vertices:
            self.draw_graph_vertex(
                v,
                radius=HOVERED_VERT_RADIUS if v is self.hover_target else VERT_RADIUS,
                color=HOVERED_VERT_COLOR if v is self.hover_target else VERT_COLOR,
            )

        pyglet.graphics.draw_indexed(
            self.num_verts(),
            pyglet.gl.GL_TRIANGLES,
            self.draw_indices,
            ('v2f', self.vertex_coords),
            ('c3B', self.vertex_colors),
        )

    def update_instructions_text(self):
        self.instructions_label.text = textwrap.dedent(f"""\
        Click outside the graph to add a new vertex.
        Click near an edge to flip it.
        Click on a vertex to remove it.

        Cursor: ({int(self.mouse_pos[0])}, {int(self.mouse_pos[1])})

        Animation multiplier: {self.animation_multiplier:.2f}
        [f] faster
        [s] slower
        """)

    def draw_graph_vertex(self, v, radius, color):
        """Add a graph vertex to the draw list."""
        x, y = v.loc
        x1, x2 = x - radius, x + radius
        y1, y2 = y - radius, y + radius
        coords = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
        self.draw_quad(coords, color)

    def draw_graph_edge_flip_animation(self, v1, v2, radius, color):
        n1 = v1.get_next_nbr(v2).loc
        n2 = v2.get_next_nbr(v1).loc
        v1 = v1.loc
        v2 = v2.loc

        # Swap points if it will make the animation cover less distance.
        if dist(v1, n1) + dist(v2, n2) > dist(v1, n2) + dist(v2, n1):
            n1, n2 = n2, n1

        # Interpolate between the old vertices and the new ones.
        p1 = interpolate(v1, n1, self.animation_progress)
        p2 = interpolate(v2, n2, self.animation_progress)
        self.draw_graph_edge(p1, p2, radius, color)

    def draw_ghost_edges(self, new_pos):
        try:
            v1, v2 = self.graph.find_convex_nbrs(Vertex(*new_pos))
            if v1 is not None and v2 is not None:
                radius = GHOST_EDGE_RADIUS
                color = GHOST_EDGE_COLOR
                self.draw_graph_edge(new_pos, v1.loc, radius, color)
                self.draw_graph_edge(new_pos, v2.loc, radius, color)
                color = CROSS_EDGE_COLOR
                self.draw_graph_edge(v1.loc, v2.loc, radius, color)
        except ValueError:
            pass  # ok if it fails

    def draw_graph_edge(self, a, b, radius, color):
        """Add a graph edge to the draw list."""
        fwd = b - a
        fwd *= np.true_divide(radius, np.linalg.norm(fwd))
        left = np.array([-fwd[1], fwd[0]])  # rotate `fwd` counterclockwise 90
        right = -left
        back = -fwd
        coords = [
            a + back + left,
            a + back + right,
            b + fwd + left,
            b + fwd + right,
        ]
        self.draw_quad(coords, color)

    def draw_quad(self, quad_verts, color):
        """Add an arbitrary quadrilateral to the draw list."""
        assert len(quad_verts) == 4
        base = self.num_verts()
        self.vertex_coords += list(flatten(quad_verts))
        self.vertex_colors += list(color) * 4
        self.draw_indices += [base + i for i in [0, 1, 2, 3, 2, 1]]

    def num_verts(self):
        return len(self.vertex_coords) // 2

    def is_flip_queued(self, e):
        v1, v2 = e
        return (('flip', (v1, v2)) in self.animation_queue
                or ('flip', (v2, v1)) in self.animation_queue)

    def is_next_flip_queued(self, e):
        if not self.animation_queue:
            return False
        v1, v2 = e
        next_queued = self.animation_queue[0]
        return (('flip', (v1, v2)) == next_queued
                or ('flip', (v2, v1)) == next_queued)

    def enqueue_anim(self, action, loc, log=True):
        if action == 'add':
            try:
                a, b = self.graph.find_convex_nbrs(Vertex(*self.mouse_pos))
                for e in self.graph.get_cross_edges(a, b):
                    self.enqueue_anim('flip', e, log=False)
            except ValueError:
                pass
            if log:
                print("Add vertex at", loc)
        elif action == 'remove':
            v = loc
            for n in v.nbrs:
                if self.graph.can_flip(v, n):
                    self.enqueue_anim('flip', (v, n), log=False)
            if log:
                print("Remove vertex at", loc)
        elif action == 'flip':
            if log:
                print("Flip edge between", loc[0], "and", loc[1])
        self.animation_queue.append((action, loc))

    def step_animation(self, dt):
        if self.warning_text_countdown > 0.0:
            self.warning_text_countdown -= dt

        if not self.animation_queue:
            if self.replay_lines:
                self.replay_line(self.replay_lines.pop(0))
            if not self.animation_queue:
                return

        action, loc = self.animation_queue[0]
        if action == 'flip':
            self.animation_progress += (self.animation_multiplier * dt
                                        / DEFAULT_ANIMATION_DURATION)
            if self.animation_progress >= 1:
                self.graph.flip_edge(*loc)
                self.animation_queue.pop(0)
                self.animation_progress = 0.0
                self.update_nearest_thing()
        elif action == 'add':
            try:
                self.graph.add_vertex(*loc)
            except ValueError as e:
                # failed to add vertices (probably because colinear)
                print("Failed to add vertex:", e)
                self.warning_text_countdown = 2.0
            self.animation_queue.pop(0)
            self.update_nearest_thing()
        elif action == 'remove':
            self.graph.remove_vertex(loc)
            self.animation_queue.pop(0)
            self.update_nearest_thing()

    def replay_line(self, line):
        line = line.lower()
        coords = [float(x) for x in re.findall(r'[\d]+\.', line)]

        if line.startswith('add'):
            # Add vertex
            self.enqueue_anim('add', np.array(coords))
        elif line.startswith('remove'):
            # Remove vertex
            self.enqueue_anim('remove', self.find_vertex(coords))
        elif line.startswith('flip'):
            # Flip edge
            edge = (self.find_vertex(coords[:2]),
                    self.find_vertex(coords[2:]))
            self.enqueue_anim('flip', edge)

    def find_vertex(self, loc):
        return [v for v in self.graph.vertices if (v.loc == np.array(loc)).all()][0]


def flatten(it):
    """Flatten nested iterators.

    Implementation based on https://stackoverflow.com/a/2158532/4958484.
    """
    for elem in it:
        if isinstance(elem, Iterable) and not isinstance(elem, (str, bytes)):
            yield from flatten(elem)
        else:
            yield elem


def dist_point_to_line_segment(a, b, p):
    """Returns the distance from a point `p` to a line segment `(a, b)`, or
    `None` if the point is beyond the bounds of the line segment.

    Immplementation based on
    https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Vector_formulation.
    """
    n = b - a
    line_length = np.linalg.norm(n)
    n /= line_length
    v = p - a
    v_parallel = np.dot(v, n)
    if v_parallel < 0 or v_parallel > line_length:
        return None
    v_perpendicular = v - n * v_parallel
    return np.linalg.norm(v_perpendicular)


def interpolate(a, b, t):
    """Interpolate between two points."""
    # Use circular easing (from https://easings.net/#easeInOutCirc)
    t = -(math.cos(math.pi * t) - 1) / 2
    return lerp(a, b, t)


def lerp(a, b, t):
    """Linearly interpolate between two points."""
    return t * b + (1 - t) * a


def main():
    VisualizationWindow()
    pyglet.app.run()


if __name__ == '__main__':
    main()
