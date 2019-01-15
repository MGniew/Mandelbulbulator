import numpy as np
import pyopencl as cl
from PyQt5.QtGui import QImage, QColor
from pyopencl import array

from src.camera import Camera


class Connector:
    def __init__(self):

        self.light_struct = np.dtype([("position", cl.cltypes.float3),
                                      ("ambience", cl.cltypes.float3),
                                      ("diffuse", cl.cltypes.float3),
                                      ("specular", cl.cltypes.float3)])

        camera = Camera(640, 640)
        self.camera = camera

        self.light = np.array((array.vec.make_float3(0, 5, 2),
                               array.vec.make_float3(0.5, 0.4, 0.5),
                               array.vec.make_float3(0.5, 0.5, 0.5),
                               array.vec.make_float3(0.2, 0.4, 0.5)),
                              dtype=self.light_struct)

        self.choosed_device = None
        self.image = None
        self.image_array = None
        self.host_array = None
        self.cl_context = None
        self.cl_queue = None
        self.flags = cl.mem_flags
        self.camera_buf = None
        self.lights_buf = None
        self.n_lights = np.int32(1)
        self.results_buf = None
        self.program = None
        self.kernel_code = None
        self.results = np.zeros((640, 640), dtype=cl.cltypes.float3)
        self.build_program()

    def build_program(self):
        self.set_device(self.get_platforms()[0])
        self.cl_context = cl.Context(self.choosed_device)
        self.cl_queue = cl.CommandQueue(self.cl_context)

        mandel_code = open("kernels/mandelbulb.cl", "r")
        self.kernel_code = mandel_code.read()
        mandel_code.close()
        self.program = cl.Program(self.cl_context, self.kernel_code).build()

        self.camera_buf = cl.Buffer(
            self.cl_context,
            self.flags.READ_ONLY | self.flags.COPY_HOST_PTR,
            hostbuf=self.camera.get_cl_repr())
        self.lights_buf = cl.Buffer(
            self.cl_context,
            self.flags.READ_ONLY | self.flags.COPY_HOST_PTR,
            hostbuf=self.light)
        self.results_buf = cl.Buffer(self.cl_context,
                                     self.flags.WRITE_ONLY,
                                     self.results.nbytes)

    def get_platforms(self):
        return cl.get_platforms()

    def set_device(self, platform):
        self.choosed_device = platform.get_devices()

    def get_image(self):

        for i in range(1000):

            self.camera.rotate()
            print(i)
            #self.camera.rotate_aroud_center()
            if i <= 44:
                continue
            #  self.camera.move(True, False, False, False)
            self.camera_buf = cl.Buffer(
                self.cl_context,
                self.flags.READ_ONLY | self.flags.COPY_HOST_PTR,
                hostbuf=self.camera.get_cl_repr())

            self.program.get_image(
                self.cl_queue,
                self.results.shape,
                None, self.camera_buf,
                self.lights_buf, self.n_lights, self.results_buf)

            self.cl_queue.finish()

            cl.enqueue_copy(self.cl_queue, self.results, self.results_buf)
            # width, height = self.results.shape
            image = QImage(640, 640, QImage.Format_ARGB32)
            for x in range(image.width()):
                for y in range(image.height()):
                    image.setPixel(x, y, QColor((self.results[y][x][0]),
                                                (self.results[y][x][1]),
                                                (self.results[y][x][2]),
                                                255).rgb())
            image.save("out2/{}.png".format(i), "png")
        quit()
        return image
