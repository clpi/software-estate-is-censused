import Lake
open Lake DSL

package «software-estate-is-censused» where
  moreLeanArgs := #["-DwarningAsError=true"]

@[default_target]
lean_lib Mirror where
  roots := #[`Mirror, `Axioms]
