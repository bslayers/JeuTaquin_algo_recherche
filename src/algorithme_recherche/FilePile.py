
class Element:
    def __init__(self, contenu):
        self.precedent = None
        self.prochain = None
        self.contenu = contenu

class FilePile:
    def __init__(self, max_size=None):
        self.start = None
        self.end = None
        self.size = 0
        self.max_size = max_size
        self.batch_removal_threshold = 10

    def pop(self):
        if not self.start:
            return None
        
        contenu = self.start.contenu
        self.start = self.start.prochain
        if self.start is None:
            self.end = None
        else:
            self.start.precedent = None

        self.size -= 1
        return contenu

    def pushLast(self, contenu):
        elt = Element(contenu)
        if not self.start:
            self.start = elt
            self.end = elt
        else:
            self.end.prochain = elt
            elt.precedent = self.end
            self.end = elt

        self.size += 1

        if self.max_size and self.size > self.max_size:
            self._batch_remove_oldest()

    def pushFirst(self, contenu):
        elt = Element(contenu)
        if not self.start:
            self.start = elt
            self.end = elt
        else:
            elt.prochain = self.start
            self.start.precedent = elt
            self.start = elt
        
        self.size += 1

        if self.max_size and self.size > self.max_size:
            self._remove_oldest()

    def _batch_remove_oldest(self):
        removal_count = min(self.size - self.max_size, self.batch_removal_threshold)
        for _ in range(removal_count):
            self.pop()
            
    def __bool__(self): 
        return self.start is not None

    def __len__(self):
        return self.size
