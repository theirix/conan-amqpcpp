from conans import ConanFile, CMake, tools, RunEnvironment
import os

class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.so", dst="bin", src="lib")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            if self.settings.os == "Windows":
                self.run(os.path.join("bin","testapp"))
            elif self.settings.os == "Macos":
                self.run("DYLD_LIBRARY_PATH=%s %s"%(os.environ.get('DYLD_LIBRARY_PATH', ''),os.path.join("bin","testapp")))
            else:
                self.run("LD_LIBRARY_PATH=%s %s"%(os.environ.get('LD_LIBRARY_PATH', ''),os.path.join("bin","testapp")))
