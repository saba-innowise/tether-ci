from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy
import os


class TetherSumConan(ConanFile):
    name = "tether_sum"
    version = "0.1"
    description = "dummy library"
    license = "MIT"

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "build_tests": [True, False],
        "run_tests": [True, False],
    }
    default_options = {
        "shared": True,
        "build_tests": False,
        "run_tests": False,
    }

    exports_sources = "CMakeLists.txt", "tether_sum/*", "tests/*", "cmake/*"

    def requirements(self):
        if self.options.build_tests:
            self.requires("gtest/1.15.0")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.cache_variables["TETHER_SUM_BUILD_SHARED"] = "ON" if self.options.shared else "OFF"
        tc.cache_variables["TETHER_SUM_BUILD_TESTS"] = "ON" if self.options.build_tests else "OFF"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if self.options.build_tests and self.options.run_tests:
            cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["tether_sum"]
        self.cpp_info.set_property("cmake_file_name", "tether_sum")
        self.cpp_info.set_property("cmake_target_name", "tether_sum::tether_sum")

        if self.options.shared and self.settings.os == "Windows":
            self.cpp_info.defines.append("TETHER_SUM_IMPORTS")

        self.cpp_info.set_property("cmake_build_modules", [
            os.path.join(self.package_folder, "lib", "cmake", "tether_sum", "modules", "TetherAddExecutable.cmake")
        ])
