#!/usr/bin/env bash
set -euo pipefail
CG=${1:-../cg}
if [ ! -d "$CG/cogym_kernel/worlds" ]; then echo "usage: $0 /path/to/prx0r/cg"; exit 2; fi
mkdir -p "$CG/cogym_kernel/worlds/arena402"
cp -R cg_overlay/cogym_kernel/worlds/arena402/* "$CG/cogym_kernel/worlds/arena402/"
echo "Installed Cogym-native world at $CG/cogym_kernel/worlds/arena402"
echo "Install this package too: pip install -e $(pwd)"
echo "Then verify: cd $CG && cg worlds"
