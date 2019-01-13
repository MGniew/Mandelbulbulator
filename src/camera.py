import numpy as np
import pyopencl as cl
import math


class Camera(object):

    camera_struct = np.dtype(
        [("position", cl.cltypes.float3),
         ("topLeftCorner", cl.cltypes.float3),
         ("rightVector", cl.cltypes.float3),
         ("upVector", cl.cltypes.float3),
         ("worldWidth", cl.cltypes.float),
         ("worldHeight", cl.cltypes.float),
         ("zFar", cl.cltypes.float)])

    def __init__(
            self,
            width,
            height,
            position=[0, 0, -2],
            direction=[0, 0, 1],
            z_near=1,
            z_far=8,
            povy=80):

        self.position = np.array(position)
        self.z_far = z_far
        self.direction = np.array(direction)
        self.direction = self.direction / np.linalg.norm(self.direction)
        aspect = width/height
        self.z_near = z_near
        self.world_height = 2 * math.tan((povy * math.pi/180)/2) * z_near
        self.world_width = aspect * self.world_height
        self.up = np.array([0, 1, 0])
        self.up = np.cross(
                    np.cross(self.direction, self.up),
                    direction)
        self.up = self.up / np.linalg.norm(self.up)
        self.right = np.cross(self.direction, self.up)
        self.update()

    def rotate(self, up, left, down, right):
        pass

    def move(self, forward, backward):

        self.position = self.position + self.direction * 1/20
        self.update()

    def update(self):

        self.top_left = self.position + self.z_near * self.direction
        self.top_left = self.top_left + self.world_height/2 * self.up
        self.top_left = self.top_left - self.world_width/2 * self.right

    def get_cl_repr(self):

        return np.array((cl.array.vec.make_float3(*self.position.tolist()),
                         cl.array.vec.make_float3(*self.top_left.tolist()),
                         cl.array.vec.make_float3(*self.right.tolist()),
                         cl.array.vec.make_float3(*self.up.tolist()),
                         np.float(self.world_width),
                         np.float(self.world_height),
                         np.float(self.z_far)),
                        dtype=Camera.camera_struct)
