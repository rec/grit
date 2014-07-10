alias grit=/path/to/grit/Grit.py

# next root
function + () {
  cd `grit + $*`
}

# previous root
function - () {
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
function gra() {
  grit a $*
}

# amend push
function grap() {
  grit a p
}

# branches
function grb() {
  grit b $*
}

# clone
function grc() {
  grit c $*
}

# pushes
function grp() {
  grit p
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
