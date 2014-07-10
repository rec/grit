grit
====

grit: A rationalized git workflow.
----------------------------

(Beta 0.8)

This is a little command line tool to help programmers developing using GitHub
and *nix.  Grit automates many common command line tasks away and makes
navigation a breeze.

This beta is aimed at Rippled C++ programmers.


How to install
--------------

1. Download the code.
2. Set an alias to grit/Grit.py.
3. Set an environment variable in your .bashrc `export GIT_USER=<your-username-on-github>`


How to use
-----------

grit has the following commands: amend, branches, clone, cd, help, find, new,
    open, pulls, remake, remotes, and test.

From most interesting commands down, it's probably open, find, cd, new, clone,
branches...

Each is documented below and through help.

There's also a file, https://github.com/rec/grit/blob/master/for-your-bashrc.sh,
which has a list of shortcuts you might want to put in your .bashrc file.


Roots
-----

Some grit commands are for programmers with multiple git directories active at
one time.  For example, the branches command prints out "all branches in all
roots".  What does this mean?

grit has the concept of your "Git root" - the base directory for the git
repository that contains your current directory.  If you aren't in a Git
directory, the Git root is empty.

And there's also the "super root" - the directory above the Git root.  If
the Git root is empty, the container root is your current directory.  So "all
branches in all roots" means all git directories in your super root - which is
probably "all sibling git directories" if you're in a Git directory.


Finally, some commands are considered "unsafe" and require yes/no confirmation
before you use them.


amend
=====

Amends the previous change, keeping the same change description and adding all
git files that have been changed.  Equivalent to
`git commit --amend --no-edit -a`.

    grit a[mend] [p[ush]]

With the optional push argument, also force-push the result, equivalent to
`git push -f`.

*Unsafe.*


branches
======

    grit b[ranches] [<prefix>]

Lists all git roots and their branches.  If there is a prefix, only git roots
that start with that prefix are listed.

The current branch in each repository is marked with a star (*).

A branch which has a current pull request out is marked with an
exclamation mark (!).

cd commands
-----------

A set of commands to cycle through git roots.

Often passed to the shell's cd command like this:

     $ cd `grit +`


+
=
    grit + [<prefix>]

Prints the directory corresponding to this one in the _next_ git root.
If <prefix> is non-empty, only cycles through directories starting with prefix.

-
=
    grit + [prefix]

Prints the directory corresponding to this one in the _previous_ git root.
If <prefix> is non-empty, only cycles through directories starting with prefix.

^
=
    grit ^

Prints the top-level directory in this git root.


clone
=====

Clones the current project, sets up remote aliases, creates a new branch, builds
and runs tests on the new repo.


    grit c[lone] [<branch>] [<new repo name>]

If branch is empty, defaults to the base_branch (which is develop for rippled).
If the new repo name is empty, selects a next incremental name from the
directory name - e.g. rippled -> rippled2, rippled2 -> rippled3.

*Unsafe*


find
=====

Finds files or directories by prefix and cycles through them.

    grit f[ind] <prefix>

Finds the next directory that starts with <prefix>, or the next directory that
coontains a file that start with <prefix>, and prints it.

Often used as an argument to the cd command, like this:

    $ cd `grit f RippleCalc`


help
===

Prints help on grit.


    grit h[elp]

Lists all commands.

    git h[elp] [command]

Prints help on one command.


new
===

Creates a new source file in the git repository.

    grit n[ew] <filename> [<filename> ...]

Creates a new source file with C++ guards, adds it to the git repo, remakes
the project files.

Requires templates for each new filetype.  The rippled project has templates for
.cpp and .h.


open
====

Opens a file or directory in a github.com web page.

    grit o[pen] [<filename or prefix>]

With no arguments, opens the current directory and branch within
http://github.com in your browser.

With a filename or prefix, opens the first file or directory in the current
directory which starts with that prefix.


pulls
=====

Lists all the pull requests for the main project repo.

      grit p[ull]

remake
======

Remakes the makefile, sconsfile or other build file when files have been
added or removed.

    grit rema[ke]

Automatically called by `grit new`.

remotes
======

Add all the remotes git nicknames for your project.

    grit remo[tes]

Automatically called by `grit clone`.

test
====

Run tests for the project.

    grit t[est]

Automatically called by `git clone`.

#
