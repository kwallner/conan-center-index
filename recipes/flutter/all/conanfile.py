import os
from distutils import dir_util
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class FlutterInstallerConan(ConanFile):
    name = "flutter"
    description = "flutter binaries for use in recipes"
    topics = ("conan", "dart", "flutter")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://flutter.dev/"
    license = "MIT"
    settings = {"os_build"}
    no_copy_source = True

    @property
    def _source_subfolder(self):
        return os.path.join(self.source_folder, "source_subfolder")

    def _extract_from_data(self):
        data = self.conan_data["sources"][self.version][str(self.settings.os_build)]
        url, sha256 =data['url'], data['sha256']
        filename = os.path.basename(url)
        return url, filename, sha256

    def source(self):
        url, filename, sha256 = self._extract_from_data()
        tools.download(url, filename, sha256=sha256)
    
    def build(self):
        _, filename, _ = self._extract_from_data()
        tools.unzip(os.path.join(self.source_folder, filename))

    def package(self):
        _, filename, _ = self._extract_from_data()
        #self.copy(pattern="*", src=self.name)
        dir_util.copy_tree(os.path.join(self.build_folder, self.name), self.package_folder)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
