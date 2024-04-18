if(NOT DEFINED HALCONARCH)
    if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")
        if("${CMAKE_SIZEOF_VOID_P}" EQUAL "8")
            set(HALCONARCH x64-win64)
        else()
            set(HALCONARCH x86sse2-win32)
        endif()
    elseif(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
        set(HALCONARCH x64-linux)
    else()
        message( FATAL_ERROR "Unsupported system." )
    endif()
else()
    set(HALCONARCH $ENV{HALCONARCH})
endif()

if(${WIN32})
    string(REGEX REPLACE "\\\\" "/" HALCONROOT $ENV{HALCONROOT})
else()
    set(HALCONROOT $ENV{HALCONROOT})
endif()

if(HALCONROOT)

  if(EXISTS "${HALCONROOT}/lib")
    set(HALCON_EXT_LIB_DIR ${HALCONROOT}/lib/${HALCONARCH})
  else()
    if(EXISTS "${HALCONROOT}/libd")
      set(HALCON_EXT_LIB_DIR ${HALCONROOT}/libd/${HALCONARCH})
    else()
      if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")
        message( FATAL_ERROR "HALCONROOT environment variable is not set or HALCON is not installed.")
      endif()
    endif()
  endif()

  if(EXISTS "${HALCONROOT}/include")
    set(HDEVENGINE_INC_DIRS ${HALCONROOT}/include)
  else()
    if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")
      message( FATAL_ERROR "HALCONROOT environment variable is not set or HALCON is not installed.")
    endif()
  endif()

endif()

if(${WIN32})
    set(PREFIX ${CMAKE_IMPORT_LIBRARY_PREFIX})
    set(SUFFIX ${CMAKE_IMPORT_LIBRARY_SUFFIX})
else()
    set(PREFIX ${CMAKE_SHARED_LIBRARY_PREFIX})
    set(SUFFIX ${CMAKE_SHARED_LIBRARY_SUFFIX})
endif()

if(HALCON_EXT_LIB_DIR)
    set(HDEVENGINE_LIBS ${HALCON_EXT_LIB_DIR}/${PREFIX}hdevenginecpp${SUFFIX})
    set(HDEVENGINE_LIBS_XL ${HALCON_EXT_LIB_DIR}/${PREFIX}hdevenginecppxl${SUFFIX})
else()
    set(HDEVENGINE_LIBS ${PREFIX}hdevenginecpp${SUFFIX})
    set(HDEVENGINE_LIBS_XL ${PREFIX}hdevenginecppxl${SUFFIX})
endif()
