class VectorClock:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.clock = {}  # Initialize an empty dictionary to store timestamps for each node

    def increment(self, other_node_id: int):
        """
        Increment the count for the specified node in this node's clock vector.
        If the node ID does not exist, add it to the dictionary.
        """
        if other_node_id not in self.clock:
            self.clock[other_node_id] = 1
        else:
            self.clock[other_node_id] += 1

    def merge(self, other_clock: 'VectorClock'):
        """
        Merge another vector clock with the current clock by taking the maximum timestamp between them.
        """
        for node_id, timestamp in other_clock.clock.items():
            if node_id not in self.clock or timestamp > self.clock[node_id]:
                self.clock[node_id] = timestamp

    def compare(self, other_clock: 'VectorClock') -> int:
        """
        Compare the relationship between two vector clocks:
        - Return a negative number if the current clock is behind other_clock
        - Return zero if the clocks are equal (although they may represent different event histories)
        - Return a positive number if the current clock is ahead of other_clock
        """
        if self.clock == other_clock.clock:
            return 0

        self_nodes = set(self.clock.keys())
        other_nodes = set(other_clock.clock.keys())

        common_nodes = self_nodes.intersection(other_nodes)
        different_nodes = (self_nodes - common_nodes) | (other_nodes - common_nodes)

        # For common nodes, compare their respective counts
        for node in common_nodes:
            if self.clock[node] < other_clock.clock[node]:
                return -1
            elif self.clock[node] > other_clock.clock[node]:
                return 1

        # For nodes present in only one clock, the clock with more node counts is considered ahead
        if len(different_nodes) > 0:
            if len(self_nodes) > len(other_nodes):
                return 1
            else:
                return -1

        # This should not be reached unless there is an inconsistency in the clock data structures
        raise ValueError("Inconsistent vector clocks detected.")

    def __repr__(self):
        return f"VectorClock({self.node_id}, {self.clock})"