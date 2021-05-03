"""
    Build script for test.py
    test-builder.py
"""

from os.path import join
from SCons.Script import AlwaysBuild, Builder, Default, DefaultEnvironment


env = DefaultEnvironment()

# A full list with the available variables
# http://www.scons.org/doc/production/HTML/scons-user.html#app-variables
env.Replace(
    AR="riscv64-unknown-elf-gcc-ar",
    AS="riscv64-unknown-elf-as",
    CC="riscv64-unknown-elf-gcc",
    GDB="riscv64-unknown-elf-gdb",
    CXX="riscv64-unknown-elf-g++",
    OBJCOPY="riscv64-unknown-elf-objcopy",
    RANLIB="riscv64-unknown-elf-gcc-ranlib",
    SIZETOOL="riscv64-unknown-elf-size",
    OBJDUMP="riscv64-unknown-elf-objdump",

    SIZEPRINTCMD='$SIZETOOL -d $SOURCES',
    SIZEPROGREGEXP=r"^(?:\.text|\.data|\.rodata|\.text.align)\s+(\d+).*",
    SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",

    #UPLOADER=join("$PIOPACKAGES_DIR", "tool-bar", "uploader"),
    #UPLOADCMD="$UPLOADER $SOURCES"
)

if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

env.Append(
    # ARFLAGS=["..."],

    # ASFLAGS=["flag1", "flag2", "flagN"],
    CCFLAGS=["-mstrict-align"],
    # CXXFLAGS=["flag1", "flag2", "flagN"],
    LINKFLAGS=["-mstrict-align"],

    CPPDEFINES=["-DBONFIRE"],

    # LIBS=["additional", "libs", "here"],

    BUILDERS=dict(
        ElfToBin=Builder(
            action=" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"]),
            suffix=".bin"
        ),
        ElfToLst=Builder(
            action=" ".join([
                "$OBJDUMP",
                "-S",
                "-d",               
                "$SOURCES",
                ">$TARGET"]),
            suffix=".lst"
        ),
        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".hex"
        )
    )
)


# The source code of "platformio-build-tool" is here
# https://github.com/platformio/platformio-core/blob/develop/platformio/builder/tools/platformio.py

#
# Target: Build executable and linkable firmware
#
target_elf = env.BuildProgram()
AlwaysBuild(target_elf)

#
# Target: Build the .bin file
#
_name = env.get("PROGNAME")

target_bin = env.ElfToBin(join("$BUILD_DIR", _name), target_elf)

# Target: Build the .hex file
#
target_hex = env.ElfToHex(join("$BUILD_DIR", _name), target_elf)
# Target: Build the .lst file
#
target_lst = env.ElfToLst(join("$BUILD_DIR", _name), target_elf)

#
# Target: Upload firmware
#
upload = env.Alias(["upload"], target_bin, "$UPLOADCMD")
AlwaysBuild(upload)

#
# Target: Print binary size
#

target_size = env.Alias(
    "size", target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"))

AlwaysBuild(target_size)
AlwaysBuild(target_lst)
AlwaysBuild(target_hex)
AlwaysBuild(target_bin)


#
# Target: Define targets
#
Default(target_bin,target_lst)