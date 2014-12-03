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
function root () {
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

# amend
function ga() {
  grit a $*
}

# amend force
function gap() {
  grit a -f $*
}

# branches
function gb() {
  grit b $*
}

# clone
function gc() {
  grit c $*
}

# pushes
function gp() {
  grit p
}

# clone
function gs() {
  grit c $*
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
