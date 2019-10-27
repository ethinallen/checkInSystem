# checkInSystem
creating a check in system for CUhackitEvents

## TODO
- [x] Add entries to DB
- [x] Ability to change a name
  - Insert `c` flag before ID to change the name
- [ ] Ability to print who is in and who is out
- [x] Search DB for UID
- [ ] Modify the tech that the participant has checked out
  - [x] add feature to select `add tech`
  - [ ] add feature to select `remove tech`
- [ ] Identify additional participant information that we want to track

## Issues
- [x] Sometimes the last id number is omitted upon scanning
  - Verify the length of the uid string before converting to int
