#!/bin/sh

export PATH="$(npm bin):$PATH"

exec "$@"
