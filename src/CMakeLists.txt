install(PROGRAMS py-server.py DESTINATION ${project_intsall_dir} RENAME py-server)
install(PROGRAMS py-client.py DESTINATION ${project_intsall_dir} RENAME py-client)
install(FILES MessageHandler.py DESTINATION ${project_intsall_dir})
