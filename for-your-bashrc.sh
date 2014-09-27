# next root
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

# previous root
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

# top of root
function root () {
  cd `grit ^ $*`
}

# find
function f() {
  cd `grit f $*`
}

# open
function o() {
  grit o $*
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
  grit a -f
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
