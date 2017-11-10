import os

from conans import ConanFile, tools, CMake
from conans.util import files

class OpenSceneGraphConan(ConanFile):
    name = "OpenSceneGraph"
    version = "3.5.7"
    ZIP_FOLDER_NAME = "OpenSceneGraph-OpenSceneGraph-%s" % version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "include_pdbs": [True, False], "cygwin_msvc": [True, False],
               "no_gmock": [True, False], "no_main": [True, False], "fpic": [True, False]}
    default_options = ("shared=True", "include_pdbs=False", "cygwin_msvc=False",
                       "no_gmock=False", "no_main=False", "fpic=False")
    exports_sources = "CMakeLists.txt"
    url = "https://github.com/ndesai/conan-OpenSceneGraph"
    license = "https://github.com/openscenegraph/OpenSceneGraph/blob/master/LICENSE.txt"
    description = "OpenSceneGraph"

    def config_options(self):
        if self.settings.compiler != "Visual Studio":
            try:  # It might have already been removed if required by more than 1 package
                del self.options.include_pdbs
            except Exception:
                pass

    def source(self):
        zip_name = "OpenSceneGraph-%s.zip" % self.version
        url = "https://github.com/openscenegraph/OpenSceneGraph/archive/%s" % zip_name
        tools.download(url, zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        files.mkdir("_build")
        with tools.chdir("_build"):
            cmake = CMake(self)
            cmake.configure(build_dir=".", source_dir="../")
            cmake.build(build_dir=".")

    def package(self):
        # Copy the license files
        self.copy("license*", src="%s/" % self.ZIP_FOLDER_NAME, dst=".", ignore_case=True, keep_path=False)
        # Copying headers
        self.copy(pattern="*.h", dst="include", src="%s/include" % self.ZIP_FOLDER_NAME, keep_path=True)

        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=".", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=".", keep_path=False)

        # Copying debug symbols
        if self.settings.compiler == "Visual Studio" and self.options.include_pdbs:
            self.copy(pattern="*.pdb", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["osg", "osgVolume"]
