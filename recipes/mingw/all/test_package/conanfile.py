import os
try:
    import StringIO
except ImportError:
    import io as StringIO
from conans import ConanFile


class MinGWTestPackageConan(ConanFile):
    generators = "txt"
    settings = {"os_build", "arch_build" }
    options = {"threads": ["posix", "win32"], "exception": ["sjlj", "seh", "dwarf2"]}
    default_options = {"threads": "posix", "exception": "seh"}

    def build(self):
        self.run('%s %s/main.cpp -lstdc++ -o main' % (os.environ["CC"], self.source_folder))

    def test(self):
        self.run("main")
        output = StringIO.StringIO()
        self.run("%s --version" % os.environ["CC"], output=output)
