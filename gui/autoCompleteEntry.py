import tkinter as tk
from tkinter import ttk

class AutocompleteEntry(ttk.Entry):
    def set_completion_list(self, completion_list):
        self._completion_list = completion_list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self):
        # set position to end so selection starts where textentry ended
        self.position = len(self.get())

        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):
                _hits.append(element)

        # if we have a new hit list, keep this in mind 
        # if _hits != self._hits:
        self._hit_index = 0
        self._hits =_hits

        # # only allow cycling if we are in a known hit list
        # if _hits == self._hits and self._hits:
            # self._hit_index = (self._hit_index) % len(self._hits)

        # perform the auto completion
        if self._hits:
            self.delete(0,tk.END)
            self.insert(0,self._hits[self._hit_index])
            self.select_range(self.position,tk.END)

    def handle_keyrelease(self, event):
        if len(event.keysym) == 1:
            self.autocomplete()