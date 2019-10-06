# checkInSystem
creating a check in system for CUhackitEvents

## TODO
- [x] Add entries to DB
- [x] Search DB for UID
- [ ] Modify the tech that the participant has checked out
  - [ ] add feature to select `add tech`
  - [ ] add feature to select `remove tech`
- [ ] Identify additional participant information that we want to track

## Issues
- [x] Sometimes the last id number is omitted upon scanning
  - Verify the length of the uid string before converting to int
