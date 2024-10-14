# linked_manager.py

class LinkedGraphManager:
    def __init__(self, graph1_controller, graph2_controller):
        self.graph1_controller = graph1_controller
        self.graph2_controller = graph2_controller
        self.linked = False

    def link_graphs(self):
        """
        Link the two graphs to synchronize zoom/pan and playback.
        """
        self.linked = True

    def unlink_graphs(self):
        """
        Unlink the two graphs so they can operate independently.
        """
        self.linked = False

    def synchronize_viewports(self):
        """
        Synchronize the viewports (time frames and zoom) of the two graphs.
        """
        if self.linked:
            graph1_segment = self.graph1_controller.signal_manager.get_next_segment()
            graph2_segment = self.graph2_controller.signal_manager.get_next_segment()

            return graph1_segment, graph2_segment

