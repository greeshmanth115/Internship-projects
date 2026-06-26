// Function processes clean node removal with transitions
function dropActiveTrack(elementId) {
  const targetCard = document.getElementById(elementId);

  if (!targetCard) return;

  const userConfirmed = confirm(
    "Remove this track from your active semester dashboard?",
  );

  if (userConfirmed) {
    // Apply immediate visual fade transition rule
    targetCard.style.opacity = "0";
    targetCard.style.transform = "scale(0.95)";
    targetCard.style.transition = "all 0.25s ease";

    // Remove from DOM structural tree array completely after fade out finishes
    setTimeout(() => {
      targetCard.remove();
    }, 250);
  }
}
