#!/usr/bin/env bash
# Builds dist/metricsexplorer-<version>.tgz from a commit (HEAD by default) and prints its path.
#
# The package comes from `git archive`, so only committed files ship, .gitattributes
# export-ignore rules keep repo-only files out, and no macOS metadata gets in.
# Usage: scripts/pack.sh [ref]
set -euo pipefail

app_id=metricsexplorer
ref="${1:-HEAD}"

cd "$(git rev-parse --show-toplevel)"

# The [launcher] version in the ref's app.conf names the package.
version=$(git show "$ref:default/app.conf" | awk -F' *= *' '
    /^\[/ { stanza = $0 }
    stanza == "[launcher]" && $1 == "version" { print $2 }
')
if [[ -z "$version" ]]; then
    echo "pack: no [launcher] version in default/app.conf at $ref" >&2
    exit 1
fi

if [[ "$ref" == HEAD ]] && ! git diff --quiet HEAD; then
    echo "pack: warning: uncommitted changes are not in the package" >&2
fi

mkdir -p dist
package="dist/$app_id-$version.tgz"
git -c tar.umask=0022 archive --format=tar.gz --prefix="$app_id/" -o "$package" "$ref"

echo "pack: built $package from $(git rev-parse --short "$ref")" >&2
echo "$package"
