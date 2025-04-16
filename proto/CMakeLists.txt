set(proto_source_dir ${PROJECT_SOURCE_DIR}/proto)
set(proto_build_dir ${CMAKE_BINARY_DIR}/gen)
set(proto_files
    ${proto_source_dir}/message.proto
)

# protobuf conpiler
execute_process(
    COMMAND protoc
        --proto_path=${proto_source_dir}
        --cpp_out=${proto_build_dir}
        --python_out=${proto_build_dir}
        ${proto_files}
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
)

# copy .py proto files for python executables to import
install(DIRECTORY ${proto_build_dir}/
    DESTINATION ${project_intsall_dir}
    FILES_MATCHING PATTERN "*.py"
)