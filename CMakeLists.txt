cmake_minimum_required (VERSION 3.22.1)
project (console_chatroom)

set(CMAKE_CXX_STANDARD 20)

set(project_intsall_dir ${CMAKE_BINARY_DIR}/install)
install(DIRECTORY DESTINATION ${project_intsall_dir})   # make installation dir

add_subdirectory(proto)
add_subdirectory(src)



# add_subdirectory(test)

# enable_testing()