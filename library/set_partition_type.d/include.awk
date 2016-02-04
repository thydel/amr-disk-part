/^#include / { f=$2; while (getline < f) print; next } { print }
