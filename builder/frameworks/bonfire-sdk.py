# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Default flags for bare-metal programming (without any framework layers)
#

from SCons.Script import Import
from os.path import isdir, isfile, join

Import("env")
print(env)

board_config = env.BoardConfig()

FRAMEWORK_DIR = env.PioPlatform().get_package_dir("framework-bonfire-sdk")
print(FRAMEWORK_DIR)
assert FRAMEWORK_DIR and isdir(FRAMEWORK_DIR)

env.Append(
    CCFLAGS=[
        "-Og",
        "-g",
        "-Wall",  # show warnings
        "-march=%s" % board_config.get("build.march"),
        "-mabi=%s" % board_config.get("build.mabi"),
        "-mcmodel=%s" % board_config.get("build.mcmodel")
        
    ],

    LINKFLAGS=[
        "-Og",
        "-g",
        "-ffunction-sections",
        "-fdata-sections",
        #"-nostartfiles",
        "-nodefaultlibs",
        "-march=%s" % board_config.get("build.march"),
        "-mabi=%s" % board_config.get("build.mabi"),
        "-mcmodel=%s" % board_config.get("build.mcmodel"),
        "--specs=nano.specs",
        "-Wl,--gc-sections"
    ],
    CPPDEFINES=["BONFIRE_SDK"],
    # INCDIR=[
    #     join(FRAMEWORK_DIR,"inc"),
    #     join(FRAMEWORK_DIR,"boards", board_config.get("build.bonfire-sdk.platform"))
    # ],
    LIBPATH=[
        "$BUILD_DIR",
        join(FRAMEWORK_DIR, "ld")
       
    ],
    CPPPATH=[
        join(FRAMEWORK_DIR,"src"),
        join(FRAMEWORK_DIR,"inc"),
        join(FRAMEWORK_DIR,"boards", board_config.get("build.bonfire-sdk.platform"))
    ],
    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ],
    
    LIBS=["c","m"]
)

if not board_config.get("build.ldscript", ""):
    ldscript = board_config.get("build.bonfire-sdk.ldscript", "")
    print(ldscript)
    env.Replace(LDSCRIPT_PATH=ldscript)

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

#
# Target: Build sdk 
#

libs = []

libs.append(env.BuildLibrary(    
    "$BUILD_DIR",
    join(FRAMEWORK_DIR, "src")
))

env.Prepend(LIBS=libs)
