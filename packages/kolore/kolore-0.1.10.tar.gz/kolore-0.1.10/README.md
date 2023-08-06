# Kolore

A small cli utility to convert krita palette files into png images.

## Install

`pip install kolore`

## Usage

To create a palette, simply type

`kolore palette.kpl`

By default the file will be called `palette.png`, but you can specify another name as well

`kolore palette.kpl --output result.png`

You can also set the size of the generated image

`kolore palette.kpl --output result.png --width 200 --height 100`

Get general help with

`kolore --help`