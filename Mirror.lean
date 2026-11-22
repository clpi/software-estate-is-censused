/- Mirror: the proof estate describes itself, incrementally.

The estate-wide provable-result accounting can be maintained as an
incremental derivation over the estate's own append-only graph: a
repo's theorem count is re-derived only when its own census pin
moves, and every other count is carried. The three theorems here say
that this maintenance is exact.

The counting function is opaque throughout: the theorems hold for
every counting function, so the equality of the two accountings does
not depend on which declaration basis the census uses. The premise
list is the one the register states: theorem counting is by
declaration at a named head, and the graph's append-only property
holds — a step moves one repo's pin and touches nothing else. -/

namespace Mirror

variable {Repo Pin : Type} [DecidableEq Repo]

/-- Point update of a repo-indexed family: at the named repo the new
value, everywhere else the old family. -/
def upd {α : Type} (f : Repo → α) (a : Repo) (b : α) (x : Repo) : α :=
  if x = a then b else f x

theorem upd_self {α : Type} (f : Repo → α) (a : Repo) (b : α) :
    upd f a b a = b := by
  simp [upd]

theorem upd_noteq {α : Type} (f : Repo → α) {a x : Repo}
    (h : x ≠ a) (b : α) : upd f a b x = f x := by
  simp [upd, h]

/- The counting function: a repo's theorem count at a pin. -/
variable (count : Repo → Pin → Nat)

/-- The from-scratch census: every repo counted at its current pin. -/
def census (pins : Repo → Pin) (r : Repo) : Nat :=
  count r (pins r)

/-- One append step preserves the accounting exactly: recounting the
stepped repo at its new pin, and carrying every other count, gives
the from-scratch census of the stepped pin assignment. -/
theorem sound (pins : Repo → Pin) (table : Repo → Nat)
    (h : table = census count pins) (s : Repo × Pin) :
    upd table s.1 (count s.1 s.2)
      = census count (upd pins s.1 s.2) := by
  funext r
  by_cases hr : r = s.1
  · subst hr
    simp [census, upd_self]
  · simp [census, h, upd_noteq _ hr _]

/-- Every append sequence preserves the accounting exactly: folding
the steps incrementally, recounting only stepped repos, gives the
from-scratch census of the folded pin assignment. Induction over the
append steps, through `sound` at each step. -/
theorem steps :
    ∀ (steps : List (Repo × Pin)) (pins : Repo → Pin) (table : Repo → Nat),
      table = census count pins →
      (steps.foldl (fun t s => upd t s.1 (count s.1 s.2)) table)
        = census count
            (steps.foldl (fun p s => upd p s.1 s.2) pins) := by
  intro steps
  induction steps with
  | nil =>
      intro pins table h
      simpa using h
  | cons s rest ih =>
      intro pins table h
      simp only [List.foldl_cons]
      exact ih _ _ (sound count pins table h s)

/-- A repo no step touches keeps both its pin and its count: a
repo's theorem count changes only when a step moves its own pin. -/
theorem kept :
    ∀ (steps : List (Repo × Pin)) (pins : Repo → Pin) (table : Repo → Nat)
      (r : Repo), (∀ s ∈ steps, s.1 ≠ r) →
      (steps.foldl (fun t s => upd t s.1 (count s.1 s.2)) table) r
        = table r
      ∧ (steps.foldl (fun p s => upd p s.1 s.2) pins) r
        = pins r := by
  intro steps
  induction steps with
  | nil =>
      intro pins table r _
      exact ⟨rfl, rfl⟩
  | cons s rest ih =>
      intro pins table r h
      have hs : s.1 ≠ r := h s (by simp)
      have hrest : ∀ s' ∈ rest, s'.1 ≠ r :=
        fun s' hs' => h s' (List.mem_cons_of_mem s hs')
      obtain ⟨h1, h2⟩ := ih _ _ _ hrest
      simp only [List.foldl_cons]
      refine ⟨?_, ?_⟩
      · rw [h1, upd_noteq _ (Ne.symm hs) _]
      · rw [h2, upd_noteq _ (Ne.symm hs) _]

end Mirror
