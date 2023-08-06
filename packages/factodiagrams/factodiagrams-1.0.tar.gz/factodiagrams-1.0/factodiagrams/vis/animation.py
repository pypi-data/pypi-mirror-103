import math
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
from matplotlib.widgets import Button
from factodiagrams.preprocess.decomposition import fours, radius
from .points import Point, generatePoints


class Draw:
    """Creates animation of the prime factorization of a number.

    This class contains functions displaying the animation of the prime factorization, buttons and the corresponding text.

    :param fps: animation framerate.
    :type fps: int
    :param animation_duration: fps realization time.
    :type animation_duration: float
    :param pause_duration: pause duration at animation end.
    :type pause_duration: float
    :param txt: text to display.
    :type txt: str
    :parma speed_txt: text display speed.
    :type speed_txt: float
    :param points: list of points
    :type points: list of Point object
    :param target_positions: list of points positions.
    :type target_positions: list
    :param status: status of the animation (play or pause).
    :type status: str
    :param speed: animation speed.
    :type speed: int
    :param n: number to decompose.
    :type n: int
    """
    fps = 60  
    animation_duration = 0.3
    pause_duration = 0.6  
    buttons = {}
    txt = None  # Text Artist
    speed_txt = None  # Text Artist => Display speed 

    points = []
    target_positions = []

    status = 'pause'
    speed = 1  # Animation speed 
    n = 1

    def __init__(self, fps=60, animation_duration=0.3, pause_duration=0.6):
        """Construction of the graphics window.

        :param fps: animation framerate.
        :type fps: int
        :param animation_duration: fps realization time.
        :type animation_duration: float
        :param pause_duration: pause duration at animation end.
        :type pause_duration: float
        """
        self.fps = fps
        self.animation_duration = animation_duration
        self.pause_duration = pause_duration
        self.fig, self.ax = plt.subplots()
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        # Hide axis
        self.ax.axes.xaxis.set_visible(False)
        self.ax.axes.yaxis.set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('left')
        self.ax.set_aspect(1)
        # Event on close window
        self.fig.canvas.mpl_connect('close_event', self.on_close)

        # Create buttons
        self.buttons['prev'] = Button(
            plt.axes([0.64, 0.03, 0.1, 0.075]), 'Sp. -')
        self.buttons['next'] = Button(
            plt.axes([0.86, 0.03, 0.1, 0.075]), 'Sp. +')
        self.buttons['play'] = Button(
            plt.axes([0.75, 0.03, 0.1, 0.075]), 'Play')

        # Buttons on click events
        self.buttons['prev'].on_clicked(self.decrease_speed)
        self.buttons['next'].on_clicked(self.increase_speed)
        self.buttons['play'].on_clicked(self.play_pause)

        self.frame(self.n)
        self.play_pause(None)
        plt.show()

    def on_close(self, e):
        """Close animation.
        """
        exit(0)

    def play_pause(self, e):
        """Creates the "play/pause" button.

        It's a button that displays "pause" when the animation is running and "play" when paused.
        """
        if self.status == 'pause':
            self.status = 'play'
        else:
            self.status = 'pause'
        self.buttons['play'].label.set_text(
            "Play" if self.status == 'play' else "Pause")
        while 1:
            if self.status == 'pause':
                return
            self.display_next_iter()

    def display_next_iter(self):
        """Display the following diagram.

        Displays the following diagram depending on whether the animation is forward or reverse.
        """
        if self.speed > 0:
            self.n = self.n + 1
        else:
            if self.n > 1:
                self.n = self.n - 1
            else:
                self.play_pause(None)
        self.frame(self.n, True if self.speed < 1 else False)

    def increase_speed(self, e):
        """Creates the "Sp. +" button.

        Creates a button that allows you to increase the speed of the animation and display speed text.
        """
        if self.speed == -1:
            self.speed = 1
        else:
            self.speed = self.speed + 1
        self.display_speed()

    def decrease_speed(self, e):
        """Creates the "Sp. -" button.

        Creates a button that allows you to decrease the speed of the animation. When the speed is negative the animation goes back and display speed text.
        """
        if self.speed == 1:
            self.speed = -1
        else:
            self.speed = self.speed - 1
        self.display_speed()

    def display_text(self, n, factors):
        """Displays the text associated with the number n.

        Displays the number to be decomposed and its prime factorization in parentheses.

        :param n: number to decompose.
        :type n: int
        :param factors: list of prime factors of n.
        :type factors: array
        """
        # Remove text if exists
        if self.txt:
            Artist.remove(self.txt)
        # Text displays:
        #  - n
        #  - factors, joined with ' x '
        #  - factor divided by '2 x 2' if equals 4
        #  - 'prime' if n is prime number
        if n == 1:
            f = ' '
        elif n == 4:
            f = '(2 x 2)'
        else:
            f = '({0})'.format(' x '.join(('2 x 2' if x == 4 else str(x))
                                          for x in factors) if len(factors) > 1 else "prime")
        self.txt = plt.text(-7, 12, '{0} {1}'.format(self.n, f))

    def display_speed(self):
        """Displays animation speed.

        Displays the expression "Speed :" followed by the speed of the animation.
        """
        # Remove text if exists
        if self.speed_txt:
            Artist.remove(self.speed_txt)
        self.speed_txt = plt.text(0, 1.1,
                                  'Speed : {0}'.format(str(self.speed)))

    def generate_color(self, i, n):  
        """Creates RGB code that covers the entire color spectrum.

        :param i: x coordinate of a point.
        :type i: float
        :param n: number to decompose.
        :type n: int

        :return: 3 numbers for colors
        :rtype: float, float, float
        """
        if i < n / 6:
            red = 1
            green = 6 * i / n
            blue = 0
        elif i < 2 * n / 6:
            red = 1 - 6 * (i - n / 6) / n
            green = 1
            blue = 0
        elif i < 3 * n / 6:
            red = 0
            green = 1
            blue = 6 * (i - n / 3) / n
        elif i < 4 * n / 6:
            red = 0
            green = 1 - 6 * (i - n / 2) / n
            blue = 1
        elif i < 5 * n / 6:
            red = 6 * (i - 2 * n / 3) / n
            green = 0
            blue = 1
        else:
            red = 1
            green = 0
            blue = 1 - 6 * (i - 5 * n / 6) / n
        return red * 0.5, green * 0.5, blue * 0.5  # 50% to decrease brightness

    def frame(self, n, reverse=False):
        """Computes positions and display each points at each frame.

        This function calculates intermediate points between each diagram for transitions.

        :param n: number to decompose.
        :type n: int
        """
        # Generate factors
        factors = fours(n)

        # Display text with N and factors
        self.display_text(n, factors)
        # Display animation speed
        self.display_speed()

        pts = generatePoints(factors)

        # Only display points at start
        if not self.points:
            self.points = pts
            self.display_points(self.points)
            plt.pause((self.pause_duration * 1 / abs(self.speed)))
        else:
            self.target_positions = pts
            total_frames = int(
                (self.animation_duration * 1 / abs(self.speed)) * self.fps)
            # Compute each point new position for each frame
            for f in range(total_frames):
                curr_pos = []
                points_count = len(self.points)
                if reverse:
                    points_count = points_count - 1
                for i in range(points_count):
                    curr_pos.append(self.compute_current_position(
                        self.points[i], self.target_positions[i], total_frames, f))
                # Position for last point
                curr_pos.append(self.compute_current_position(self.points[len(
                    self.points) - 1], self.target_positions[len(self.target_positions) - 1], total_frames, f))
                # Display all points for this frame
                self.display_points(curr_pos)
                plt.pause(1 / self.fps)
            plt.pause((self.pause_duration * 1 / abs(self.speed)))
            self.points = self.target_positions

    def compute_current_position(self, o, t, total_frames, current_frame):
        """Compute point position at the frame current_frame.

        This function calculates the transition point to t from the point o. Used in the "frame" function to calculate each frame of transitions.

        :param o: coordinates of old point.
        :type o: list
        :param t: coordinates of new point.
        :type t: list 
        :param total_frames: number of frames between two diagrams.
        :type total_frames: int
        :param current_frame: current frame number
        :type current_frame: int

        :return: coordinates of the transition point for the current frame.
        :rtype: list
        """
        x = o.x + ((t.x - o.x) / total_frames) * (current_frame + 1)
        y = o.y + ((t.y - o.y) / total_frames) * (current_frame + 1)
        return Point(x, y)

    def display_points(self, points):
        """Display points.
        
        Clear previous points and display new points.

        :param points: list of coordinates for each point.
        :type points: list of Point objects
        """
        while self.ax.artists != []:
            self.ax.artists[0].remove()
        n = len(points)
        for i, p in enumerate(points):
            red, green, blue = self.generate_color(i, n)
            circle = plt.Circle((p.x, p.y), radius=radius(n),
                                color=(blue, green, red))
            self.ax.add_artist(circle)

