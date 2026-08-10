// Client-side tag filtering for the homepage project board.
// Multi-select, match-any: a card shows if it has at least one active tag,
// or if no tags are active at all. Regenerated markup (data-labels, the
// filter bar itself) comes from scripts/build_board.py — this file only
// wires up the interaction, it never needs to change when projects change.
(function () {
  const bar = document.querySelector(".board-filter-bar");
  if (!bar) return;

  const allButton = bar.querySelector('[data-tag="__all__"]');
  const tagButtons = Array.from(bar.querySelectorAll(".filter-tag")).filter(
    (b) => b !== allButton
  );
  const items = Array.from(document.querySelectorAll(".project-card"));

  function activeTags() {
    return tagButtons
      .filter((b) => b.classList.contains("is-active"))
      .map((b) => b.dataset.tag);
  }

  function applyFilter() {
    const active = activeTags();
    document.body.classList.toggle("is-filtered", active.length > 0);

    items.forEach((item) => {
      const labels = (item.dataset.labels || "").split("|").filter(Boolean);
      const visible =
        active.length === 0 || active.some((tag) => labels.includes(tag));
      // .is-hidden (not display:none on the card itself) — a .project-card
      // is a direct grid item both in .board-cards and in .finished-grid,
      // so removing it from flow entirely would let auto-fit collapse its
      // track and stretch the remaining cards to fill the row. Hiding only
      // its children collapses it to ~0 height while it stays in flow.
      item.classList.toggle("is-hidden", !visible);
    });

    // Deliberately NOT hiding an empty .board-column itself (e.g. via
    // display:none) — a category with 0 matches already has its title and
    // every card hidden, so it collapses to ~0 height on its own, but it
    // must stay a real grid item or auto-fit will treat its track as
    // empty and stretch the sibling columns to fill the freed space.

    const finishedSection = document.querySelector(".finished-section");
    if (finishedSection) {
      const anyVisible = Array.from(
        finishedSection.querySelectorAll(".project-card")
      ).some((item) => !item.classList.contains("is-hidden"));
      finishedSection.style.display = anyVisible ? "" : "none";
    }
  }

  allButton.addEventListener("click", () => {
    tagButtons.forEach((b) => b.classList.remove("is-active"));
    allButton.classList.add("is-active");
    applyFilter();
  });

  tagButtons.forEach((button) => {
    button.addEventListener("click", () => {
      button.classList.toggle("is-active");
      allButton.classList.toggle("is-active", activeTags().length === 0);
      applyFilter();
    });
  });
})();
