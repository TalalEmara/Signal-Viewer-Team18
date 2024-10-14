# graph_controller.py

class GraphController:
    def __init__(self, signal_manager):
        self.signal_manager = signal_manager
        self.playing = False
        self.speed = 1.0  # Default playback speed

    def set_speed(self, speed):
        """
        Set the speed of the signal playback (e.g., 1x, 2x, etc.).
        """
        self.speed = speed

    def play_signal(self):
        """
        Start playing the signal.
        """
        self.playing = True

    def stop_signal(self):
        """
        Stop the signal playback.
        """
        self.playing = False

    def update_graph(self, segment_size=100):
        """
        Fetch the next signal segment and return it for plotting.
        """
        if self.playing:
            return self.signal_manager.get_next_segment(segment_size)
        return None
