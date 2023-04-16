#!/bin/bash

mkdir -p /tmp/kra-output

FILE=$1
OUT=$2
if [ -z "$OUT" ]; then
    OUT="${FILE%.*}.png"
fi

unzip -j "$FILE" "mergedimage.png" -d "/tmp/kra-output/" > /dev/null 2>&1
chmod 664 /tmp/kra-output/mergedimage.png
convert /tmp/kra-output/mergedimage.png -colorspace sRGB -background white -alpha remove "$PWD/$OUT"

rm /tmp/kra-output/mergedimage.png
rmdir /tmp/kra-output
