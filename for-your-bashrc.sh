# cd to next roots
function +() {
  cd `grit + $*`
}

function ++() {
  cd `grit + $*`
  cd `grit + $*`
}

function +++() {
  cd `grit + $*`
  cd `grit + $*`
  cd `grit + $*`
}

function ++++() {
  cd `grit + $*`
  cd `grit + $*`
  cd `grit + $*`
  cd `grit + $*`
}

# cd to previous roots
function -() {
  cd `grit - $*`
}

function --() {
  cd `grit - $*`
  cd `grit - $*`
}

function ---() {
  cd `grit - $*`
  cd `grit - $*`
  cd `grit - $*`
}

function ----() {
  cd `grit - $*`
  cd `grit - $*`
  cd `grit - $*`
  cd `grit - $*`
}

# rotate branches
function b () {
  git branch
}

function b+ () {
  grit rotate
}

function b++ () {
  grit rotate 2
}

function b+++ () {
  grit rotate 3
}

function b- () {
  grit rotate -1
}

function b-- () {
  grit rotate -2
}

function b--- () {
  grit rotate -3
}

# top of root
function rt () {
  cd `grit ^ $*`
}

# find
function f() {
  cd `grit find $*`
}

# find
function e() {
  $EDITOR `grit find $*`
}

# open
function o() {
  grit open $*
}

function new() {
  grit new $*
}

function ga() {
  grit amend $*
}

function gap() {
  grit amend -f $*
}

function gb() {
  grit branch $*
}

function gc() {
  grit clone $*
}

function gp() {
  grit pushes
}



# other cd commands.
function ..() {
  cd ..
}

function ...() {
  cd ../..
}

function ....() {
  cd ../../..
}
