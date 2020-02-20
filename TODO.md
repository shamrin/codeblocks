# TODO

* [x] protect against empty (and weird?) in-place modifications
* [ ] do not truncate file (use atomic rename?): add time.sleep(1) before .write() to see truncation
* [ ] test and lint
* [ ] better command line parsing
* [ ] better error handling
* [ ] pip and poetry instructions
* [ ] examples for pytest, isort, autoflake
* [ ] automatically add `async` for functions with `await` in them

# Later

* [ ] support other languages
* [ ] use proper markdown parser
* [ ] support multiple files
