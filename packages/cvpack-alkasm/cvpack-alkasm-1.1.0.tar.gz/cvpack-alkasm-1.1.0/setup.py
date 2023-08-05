# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvpack', 'cvpack.extras']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5,<2.0.0', 'opencv-python!=4.2.0.32']

setup_kwargs = {
    'name': 'cvpack-alkasm',
    'version': '1.1.0',
    'description': 'Utilities for OpenCV in Python',
    'long_description': '# cvpack\n\nOpenCV extensions for more Pythonic interactions.\n\n## Install\n    \n```sh\npip install cvpack-alkasm\n```\n\n## Types\n\n`cvpack` includes types that exist in the main C++ OpenCV codebase, but that aren\'t included in the Python bindings. They are compatible as arguments to OpenCV functions, and they implement the same interfaces (with some new additions). The types that are included are `Point`, `Point3`, `Rect`, `RotatedRect`, `Size`, `TermCriteria`. They are implemented as namedtuples, and as such are immutable.\n\n```python\nimport cvpack\n\nimg = cvpack.imread("img.png")\np1 = cvpack.Point(50, 50)\np2 = cvpack.Point(100, 100)\nrect = cvpack.Rect.from_points(p1, p2)\nroi = img[rect.slice()]\nroi_size = cvpack.Size.from_image(roi)\nassert roi_size == rect.size()\n```\n\nThe overloaded constructors are available as `from_` classmethods, like `from_points` shown above. They also follow the same operator overloads that OpenCV has: two points summed is a point, adding a point to a rectangle shifts it, you can `&` two rectangles to get the intersection as a new rectangle, and so on.\n\n## Image IO\n\nWrappers for `imread`, `imwrite`, and `imshow` simplify usage by checking errors and allowing path-like objects for path arguments. Additionally, `cvpack` provides functions to read images from a URL (`imread_url`), display to a browser (`imshow_browser`) for statically serving images while working in an interpreter, and displaying images in a Jupyter notebook (`imshow_jupyter`) as HTML directly rather than the typical `plt.imshow` from `matplotlib`. Some other utilities related to display are also included.\n\n```python\nfrom pathlib import Path\nimport cvpack\n\nfor path in Path("folder").glob("*.png"):\n    img = cvpack.imread(path)\n    big = cvpack.add_grid(cvpack.enlarge(img))\n    cvpack.imshow_browser(img, route=str(path))\n```\n\n## Video IO\n\nWorking with video requires acquiring and releasing resources, so `cvpack` provides context managers for video readers and writers which wrap the classes from OpenCV. Reading video frames is simplified to iterating over the capture object.\n\n```python\nimport cv2\nimport cvpack\n\nwith cvpack.VideoCapture("video.mp4") as cap:\n    with cvpack.VideoWriter("reversed.mp4", fourcc=int(cap.fourcc), fps=cap.fps) as writer:\n        for frame in cap:\n            flipped = cv2.flip(frame, 0)\n            writer.write(flipped)\n```\n',
    'author': 'Alexander Reynolds',
    'author_email': 'alex@theory.shop',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alkasm/cvpack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
