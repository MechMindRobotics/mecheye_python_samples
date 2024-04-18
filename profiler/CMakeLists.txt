if(CMAKE_HOST_WIN32)
  cmake_minimum_required(VERSION 3.19)
else()
  cmake_minimum_required(VERSION 3.5)
endif()

project(MechEyeCppSamples)

set(CMAKE_CXX_STANDARD 14)

if(CMAKE_HOST_UNIX)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
endif()

option(USE_OPENCV "Enable samples which depend on OpenCV" ON)

set(SAMPLES
    ManageUserSets
    RegisterProfilerEvent
    TriggerMultipleProfilersSimultaneously
    TriggerWithExternalDeviceAndEncoder
    TriggerWithExternalDeviceAndFixedRate
    TriggerWithSoftwareAndEncoder
    TriggerWithSoftwareAndFixedRate
    UseVirtualDevice
    )

set(OpenCV_DEPENDING
    TriggerMultipleProfilersSimultaneously
    TriggerWithExternalDeviceAndEncoder
    TriggerWithExternalDeviceAndFixedRate
    TriggerWithSoftwareAndEncoder
    TriggerWithSoftwareAndFixedRate
    UseVirtualDevice
    )

macro(disable_samples DEPENDENCY_NAME)
  message("${DEPENDENCY_NAME} samples have been disabled:")
  foreach(SAMPLE ${SAMPLES})
    get_filename_component(SAMPLE_NAME ${SAMPLE} NAME)
    set(DEPENDENCY_LIST "${DEPENDENCY_NAME}_DEPENDING")
    if(${SAMPLE_NAME} IN_LIST ${DEPENDENCY_LIST})
      message("  - ${SAMPLE}")
      list(REMOVE_ITEM SAMPLES ${SAMPLE})
    endif()
  endforeach()
endmacro()

if(CMAKE_HOST_WIN32)
  find_package(MechEyeApi REQUIRED CONFIG PATHS "$ENV{MECHEYE_DIR}/API")
  if(NOT MechEyeApi_FOUND)
    message(
      FATAL_ERROR "MechEyeApi not found. Please install MechEyeApi first.")
  endif()
elseif(CMAKE_HOST_UNIX)
  find_package(PkgConfig)
  if(NOT PkgConfig_FOUND)
    message(FATAL_ERROR "PkgConfig not found.")
  else()
    pkg_check_modules(MECHEYEAPI REQUIRED MechEyeApi)
    if(NOT MECHEYEAPI_FOUND)
      message(
        FATAL_ERROR "MechEyeApi not found. Please install MechEyeApi first.")
    endif()
  endif()
endif()

if(USE_OPENCV)
  # OpenCV_DIR: set as your OpenCV libraries directory; Uncomment next line to
  # set OpenCV_DIR manually

  # set(OpenCV_DIR  "path to OpenCV directory")
  find_package(OpenCV REQUIRED)
  if(NOT OpenCV_FOUND)
    message(
      FATAL_ERROR
        "OpenCV not found. Please point OpenCV_DIR to the directory of your OpenCV installation (containing the file OpenCVConfig.cmake), or disable the OpenCV samples  with -DUSE_OPENCV=OFF."
    )
  endif()
else()
  disable_samples("OpenCV")
endif()


message(STATUS "All samples: ${SAMPLES}")

foreach(SAMPLE ${SAMPLES})
  get_filename_component(SAMPLE_NAME ${SAMPLE} NAME)

  include_directories(${MECHEYEAPI_INCLUDE_DIRS})
  link_directories(${MECHEYEAPI_LIBRARY_DIRS})

  set(EXCUTABLE_LIST ${SAMPLE}/${SAMPLE_NAME}.cpp)
  set(TARGETLINK_LIST ${MECHEYEAPI_LIBRARIES})

  if(${SAMPLE_NAME} IN_LIST OpenCV_DEPENDING)
    include_directories(${OpenCV_INCLUDE_DIRS})
    link_directories(${OPENCV_LIBRARY_DIRS})
    list(APPEND TARGETLINK_LIST ${OpenCV_LIBS})
  endif()

  add_executable(${SAMPLE_NAME} ${EXCUTABLE_LIST})
  target_link_libraries(${SAMPLE_NAME} ${TARGETLINK_LIST})

endforeach()
