import glob
import os
import shutil
from conans import ConanFile, tools, AutoToolsBuildEnvironment
from conans.errors import ConanInvalidConfiguration


class CPythonConan(ConanFile):
    name = "cpython"
    description = "Python Programming Language Version 3"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.python.org/"
    license = "Python Software Foundation License Version 2"
    topics = ("conan", "cpython", "python")
    generators = "txt"
    settings = "os", "arch", "compiler"
    options = { "shared": [True, False] }
    default_options = { "shared": True }
    _source_subfolder = "source_subfolder"

    def configure(self):
        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio" and tools.Version(self.settings.compiler.version.value) == "15":
                pass
            elif self.settings.compiler == "Visual Studio" and self.settings.compiler.version == "16" and self.settings.compiler.toolset == "v141":
                pass
            else:
                raise ConanInvalidConfiguration("Python does only support Visual Studio 2017 or Visual Studio 2019 with toolset v141")
            if not self.options.shared:
                raise ConanInvalidConfiguration("Python does not support static build on windows")

    def system_requirements(self):
        if self.settings.os == "Linux":
            installer = tools.SystemPackageTool()
            installer.install("zlib1g-dev") 

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "Python-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
        
    def build(self):
        with tools.chdir(self._source_subfolder):
            if self.settings.os == "Windows":
                with tools.chdir("PCBuild"):
                    self.run("get_externals.bat")
                    with tools.vcvars(self.settings):
                        self.run("build.bat -p x64 -d")
                        self.run("build.bat -p x64")
            else:
                import stat
                os.chmod("configure", 
                    stat.S_IRUSR |
                    stat.S_IWUSR |
                    stat.S_IXUSR |
                    stat.S_IRGRP |
                    stat.S_IWGRP |
                    stat.S_IXGRP |
                    stat.S_IROTH |
                    stat.S_IXOTH 
                    )
                atools = AutoToolsBuildEnvironment(self)
                args = ["--enable-shared"] if self.options.shared else []
                atools.configure(args=args)
                atools.make()
                atools.install()

    def package(self):
        if self.settings.os == "Windows":
            shutil.copytree(os.path.join(self._source_subfolder, "Include"), os.path.join(self.package_folder, "include"))
            shutil.copytree(os.path.join(self._source_subfolder, "Lib"), os.path.join(self.package_folder, "Lib"), ignore=shutil.ignore_patterns('__pycache__'))
            arch_name = {"x86_64": "amd64", "x86": "win32"}.get(str(self.settings.arch))
            arch_folder = os.path.join(self._source_subfolder, "PCBuild", arch_name)
            self.copy(pattern="*.dll", dst=".", src=arch_folder, keep_path=False)
            self.copy(pattern="*.exe", dst=".", src=arch_folder, keep_path=False)
            self.copy(pattern="*.lib", dst="libs", src=arch_folder, keep_path=False)
            self.copy(pattern="*.pyd", dst="DLLs", src=arch_folder, keep_path=False)
            pc_folder = os.path.join(self._source_subfolder, "PC")
            self.copy(pattern="*.h", dst="include", src=pc_folder, keep_path=False)
        else:
            with tools.chdir(self._source_subfolder):
                atools = AutoToolsBuildEnvironment(self)
                atools.install()
        self.copy(pattern="LICENSE", dst=".", src=self._source_subfolder, keep_path=False)

    def package_id(self):
        del self.info.settings.compiler
        
    def package_info(self):
        python_name = "python%s" % "".join(self.version.split(".")[0:2]) if self.settings.os == "Windows" else "python%sm" % ".".join(self.version.split(".")[0:2])
        self.cpp_info.includedirs = ["include" if self.settings.os == "Windows" else "include/%s" % python_name] 
        self.cpp_info.bindirs = ["." if self.settings.os == "Windows" else 'bin']
        self.cpp_info.libdirs = ["libs" if self.settings.os == "Windows" else "lib"]
        self.cpp_info.libs = [ python_name ]     
        if self.settings.os == "Macos":
            self.cpp_info.system_libs = [ "dl" ]
            self.cpp_info.exelinkflags = [ "-framework", "CoreFoundation" ]
            self.cpp_info.sharedlinkflags = [ "-framework", "CoreFoundation" ]
        elif self.settings.os == "Linux":
            self.cpp_info.system_libs = [ "pthread", "dl", "util" ]
