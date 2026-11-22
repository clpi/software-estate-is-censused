/- Axiom audit: the kernel prints the axioms each headline result
depends on. The family gate reads this output in the build log.
Expected, for every line: only the standard axioms
(propext, Classical.choice, Quot.sound), and no other. -/

import Mirror

#print axioms Mirror.sound
#print axioms Mirror.steps
#print axioms Mirror.kept
