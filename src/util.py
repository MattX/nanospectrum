import queue


def get_all_from_queue(q):
    """
    Returns at least one element from the queue, tries to return as many as possible.
    :param q: The queue to get elements from
    :return: A list of elements fetched from the queue
    """
    data = [q.get()]
    while True:
        try:
            data.append(q.get_nowait())
        except queue.Empty:
            return data
