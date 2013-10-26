#!/usr/bin/python
class Path:
    def __init__(self, Connected, Remote, Router, route_direction):
        self.local = Connected
        self.remote = Remote
        self.router = Router
        self.direction = route_direction
