#!/bin/bash

TIMESTAMP=`date "+%Y-%m-%d_%H-%M-%S"`
FILENAME="cartas-${TIMESTAMP}.zip"

cd output
zip -r "$FILENAME" *
URL=$(curl --upload-file "${FILENAME}" "https://transfer.sh/${FILENAME}")
xdg-open "https://www.overleaf.com/docs?snip_uri=$URL"