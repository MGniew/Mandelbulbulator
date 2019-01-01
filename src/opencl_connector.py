import numpy as np
import pyopencl as cl
from PyQt5.QtGui import QImage, QColor
from pyopencl import array


class Connector:
    def __init__(self):
        self.choosed_device = None
        self.image = None
        self.image_array = None
        self.host_array = None
        self.cl_context = None
        self.cl_queue = None
        self.flags = cl.mem_flags
        self.camera_buf = None
        self.lights_buf = None
        self.n_lights = 1
        self.results_buf = None
        self.program = None
        self.kernel_code = None
        self.camera = np.array([array.vec.make_float3(0, 0, 3), array.vec.make_float3(-1, 1, 1),
                                array.vec.make_float3(1, 0, 0), array.vec.make_float3(0, 1, 0),
                                float(2.0), float(2.0), float(8.0)])
        self.light = np.array([array.vec.make_float3(0, 5, 2), array.vec.make_float3(0.2, 0.4, 0.5),
                               array.vec.make_float3(0.2, 0.4, 0.5), array.vec.make_float3(0.2, 0.4, 0.5)])
        self.results = np.zeros((300, 300), dtype=cl.cltypes.float3)
        self.build_program()

    def build_program(self):
        self.set_device(self.get_platforms()[0])
        self.cl_context = cl.Context(self.choosed_device)
        self.cl_queue = cl.CommandQueue(self.cl_context)

        mandel_code = open("kernels/mandelbulb.cl", "r")
        self.kernel_code = mandel_code.read()
        mandel_code.close()
        self.program = cl.Program(self.cl_context, self.kernel_code).build()

        self.camera_buf = cl.Buffer(self.cl_context, self.flags.READ_ONLY | self.flags.COPY_HOST_PTR,
                                    hostbuf=self.camera)
        self.lights_buf = cl.Buffer(self.cl_context, self.flags.READ_ONLY | self.flags.COPY_HOST_PTR,
                                    hostbuf=self.light)
        self.n_lights = cl.Buffer(self.cl_context, self.flags.READ_ONLY | self.flags.COPY_HOST_PTR,
                                  hostbuf=np.int8(self.n_lights))
        self.results_buf = cl.Buffer(self.cl_context, self.flags.WRITE_ONLY, self.results.nbytes)

    def get_platforms(self):
        return cl.get_platforms()

    def set_device(self, platform):
        self.choosed_device = platform.get_devices()

    def get_image(self):
        self.program.get_image(self.cl_queue, self.results.shape, None, self.camera_buf,
                               self.lights_buf, np.int32(1), self.results_buf)
        self.cl_queue.finish()
        cl.enqueue_copy(self.cl_queue, self.results, self.results_buf)

        width, height = self.results.shape
        print(f"Width: {width}, height: {height}")

        print(self.results)
        print(len(self.results))
        print(self.results[0][0])
        print(len(self.results[0][0]))

        image = QImage(width, height, QImage.Format_RGB32)
        for x in range(image.width()):
            for y in range(image.height()):
                image.setPixel(x, y, QColor(self.results[x][y][0]*255, self.results[x][y][1]*255,
                                            self.results[x][y][2]*255, 255).rgb())
        return image
