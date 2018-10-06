from conans import ConanFile, tools, MSBuild, AutoToolsBuildEnvironment
import os.path


class SigcppConan(ConanFile):
    name = "sigc++"
    version = "2.10.0"
    license = "LGPL"
    url = "https://github.com/elizagamedev/conan-sigcpp"
    description = "Callback Framework for C++"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = (
        "shared=False",
        "fPIC=False",
    )
    exports = "msvc.patch"

    sourcename = "libsigc++-{}".format(version)
    platforms = {"x86": "Win32",
                 "x86_64": "x64"}

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
        if self.settings.compiler == "Visual Studio":
            del self.options.shared

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("7z_installer/1.0@conan/stable")

    def source(self):
        tools.download("https://download.gnome.org/sources/libsigc++/{}/{}.tar.xz".format(
            self.version.rpartition(".")[0],
            self.sourcename,
        ), self.sourcename + ".tar.xz")
        if self.settings.os == "Windows":
            self.run("7z x {}.tar.xz".format(self.sourcename))
            os.remove(self.sourcename + ".tar.xz")
        else:
            self.run("xz -d {}.tar.xz".format(self.sourcename))
        tools.unzip(self.sourcename + ".tar")
        os.remove(self.sourcename + ".tar")

        tools.patch(base_path=self.sourcename, patch_file="msvc.patch")

    def build(self):
        with tools.chdir(self.sourcename):
            if self.settings.compiler == "Visual Studio":
                msbuild = MSBuild(self)
                msbuild.build(os.path.join("MSVC_Net2013", "libsigc++2.sln"),
                              platforms=self.platforms,
                              toolset=self.settings.compiler.toolset)
            else:
                autotools = AutoToolsBuildEnvironment(self)
                args = (['--enable-shared', '--disable-static']
                        if self.options.shared else
                        ['--enable-static', '--disable-shared'])
                autotools.configure(args=args)
                autotools.make()
                autotools.install()

    def package(self):
        if self.settings.compiler == "Visual Studio":
            self.copy("*", src=os.path.join("vs12", self.platforms[str(self.settings.arch)]))

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join("include", "sigc++-2.0"),
                                     os.path.join("lib", "sigc++-2.0", "include")]
        self.cpp_info.libs = tools.collect_libs(self)
