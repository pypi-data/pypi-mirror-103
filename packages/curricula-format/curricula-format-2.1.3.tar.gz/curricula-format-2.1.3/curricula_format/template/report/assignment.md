# [[ assignment.title ]]

Total score: ?/[[ assignment.grading.points ]]

[% for problem in assignment.problems | selectattr("grading.enabled") %]
[% include "template:report/problem.md" %]
[% endfor -%]
