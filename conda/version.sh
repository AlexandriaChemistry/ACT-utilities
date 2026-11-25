#!/bin/sh
#
# This source file is part of the Alexandria Chemistry Toolkit.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Prints the version of act-utilities, which is taken from the git tags:
#
# - on a tag v<version>, such as v1.95, that version: 1.95;
# - N commits after it, <version>.postN, such as 1.95.post3, for test builds.
#
# The conda recipe reads it from the environment variable
# ACT_UTILITIES_VERSION:
#
#   ACT_UTILITIES_VERSION=$(conda/version.sh) rattler-build build --recipe conda/recipe.yaml ...
#
# The PyPI package takes the same version from the tags through hatch-vcs.
# The repository must have its tags (actions/checkout with fetch-depth: 0).
set -e
cd "$(dirname "$0")/.."
describe=$(git describe --tags --match 'v[0-9]*' --long 2>/dev/null) || {
    echo "version.sh: no tag v<version> in the history of $(pwd)" >&2
    exit 1
}
# v1.95-3-gabcdef0: the tag, the number of commits since, the commit
commits=${describe%-g*}
commits=${commits##*-}
tag=${describe%-*-g*}
version=${tag#v}
if [ "${commits}" = "0" ]; then
    echo "${version}"
else
    echo "${version}.post${commits}"
fi
