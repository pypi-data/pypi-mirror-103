# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.5] - 2020-04-25

### Fixed

* Improve type checking for integers to take into account numpy integers.

## [0.1.4] - 2020-04-24

### Added

* Throw an error is `boxes` elements in `bboxes_coords` are not integers.
* Explicitly allow numpy array as arguments to `BBoxes.draw`

### Fixed

* Improved check for `None` arguments in `BBoxes`.

## [0.1.3] - 2020-04-04

### Changed

* Change default font sizes for `InfoBox`.

## [0.1.2] - 2020-04-03

### Added

* The `BBoxes`, `InfoBox`, `Label` and `Font` classes, that can draw bouding objects on the image using custom TrueType fonts.
