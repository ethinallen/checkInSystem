# checkInSystem
creating a check in system for CUhackitEvents

## TODO
- [x] Add entries to DB
- [x] Ability to change a name
  - Insert `c` flag before ID to change the name
- [x] Ability to print who is in and who is out
  - Insert `s` before any ID to display the status of all participant
- [x] Search DB for UID
- [x] Modify the tech that the participant has checked out
  - [x] add feature to select `add tech`
    - Insert `to` before ID to check out tech
  - [x] add feature to select `remove tech`
    - Insert `ti` before ID to return tech 
- [ ] Identify additional participant information that we want to track
- [x] Implement a GUI version (Optional)

## Issues
- [x] Sometimes the last id number is omitted upon scanning
  - Verify the length of the uid string before converting to int
- [ ] Fix the add function for terminal version
  - The older version of add should work 
- [ ] Simplify code in GUI version (Optional)