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
    OBJDUMP="riscv64-unknown-elf-objdump"

    #UPLOADER=join("$PIOPACKAGES_DIR", "tool-bar", "uploader"),
    #UPLOADCMD="$UPLOADER $SOURCES"
)

env.Append(
    # ARFLAGS=["..."],

    # ASFLAGS=["flag1", "flag2", "flagN"],
    CCFLAGS=["-march=rv32im", "-mabi=ilp32", "-mstrict-align"],
    # CXXFLAGS=["flag1", "flag2", "flagN"],
    LINKFLAGS=["-Wl,--gc-sections",  "-march=rv32im", "-mabi=ilp32", "-mstrict-align"],

    # CPPDEFINES=["-DBONFIRE", "DEFINE=2", "DEFINE_N"],

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

#
# Target: Build the .bin file
#
target_bin = env.ElfToBin(join("$BUILD_DIR", "firmware"), target_elf)
# Target: Build the .hex file
#
target_hex = env.ElfToHex(join("$BUILD_DIR", "firmware"), target_elf)
# Target: Build the .lst file
#
target_lst = env.ElfToLst(join("$BUILD_DIR", "firmware"), target_elf)

#
# Target: Upload firmware
#
upload = env.Alias(["upload"], target_bin, "$UPLOADCMD")
AlwaysBuild(upload)

#
# Target: Define targets
#
Default(target_bin,target_hex,target_lst)