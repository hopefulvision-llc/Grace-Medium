import numpy as np

class GraceMatter:
    """
    GraceMatter - Emergence Mechanics
    =================================
    
    Represents the pre-existing "stuff" (atoms, cells, minds, organisms...)
    that already exists in reality.
    
    This is NOT a creator or simulator of matter.
    It is a passive responder / amplifier layer.
    
    Core idea:
    • Matter already exists everywhere (represented as a grid of points/locations)
    • Each location can sense the local grace density in the GraceMedium
    • When the surrounding grace medium becomes sufficiently coherent/deep,
      the local matter becomes slightly more ordered, more coherent,
      more "alive" than it would be under pure thermal/noise conditions
    
    This is the mechanism behind:
    - subtle organization
    - reduced entropy in living systems
    - rare "miraculous" coherence events when grace is very strong
    
    Philosophy: We don't make matter. We only allow it to remember/become
    more of what it already potentially is.
    """
    
    def __init__(self,
                 size: int = 256,                    # same spatial resolution as medium
                 coherence_threshold: float = 0.065, # when grace is strong enough to matter
                 max_coherence_bonus: float = 0.028, # max order boost (very modest!)
                 relaxation_rate: float = 0.015,     # how quickly coherence returns to baseline
                 baseline_entropy: float = 1.0,      # normal thermal randomness level
                 seed: int = 42):
        
        np.random.seed(seed)
        self.size = size
        
        self.threshold = coherence_threshold
        self.max_bonus = max_coherence_bonus
        self.relax_rate = relaxation_rate
        self.baseline_entropy = baseline_entropy
        
        # Current coherence level of matter at each location (0 = fully random, 1 = perfectly ordered)
        self.coherence = np.zeros((size, size), dtype=float)
        
        # Optional: track how much "extra order" we have right now
        self.global_extra_order = 0.0
        
        # For visualization / history
        self.history = []
    
    def update_from_medium(self, grace_medium: np.ndarray):
        """
        Main interface: matter responds to the current state of the GraceMedium
        
        Args:
            grace_medium: 2D array from GraceMedium.medium (listening density)
        """
        if grace_medium.shape != (self.size, self.size):
            from scipy.ndimage import zoom
            zoom_factors = (self.size / grace_medium.shape[0],
                           self.size / grace_medium.shape[1])
            grace_medium = zoom(grace_medium, zoom_factors, order=1)
        
        # Where grace is strong enough → matter gets a coherence bonus
        strong_regions = grace_medium > self.threshold
        
        # The bonus is proportional to how much above threshold we are
        # (capped at max_bonus)
        bonus = np.clip(
            (grace_medium - self.threshold) * 8.0,   # steep but not infinite slope
            0.0,
            self.max_bonus
        )
        
        # Apply the bonus only where grace is strong
        self.coherence[strong_regions] += bonus[strong_regions]
        
        # Everywhere else: slowly relax back toward baseline entropy
        relaxation = self.relax_rate * (self.baseline_entropy - self.coherence)
        self.coherence += relaxation
        
        # Keep coherence bounded
        self.coherence = np.clip(self.coherence, 0.0, 1.0)
        
        # Track global state
        self.global_extra_order = np.mean(self.coherence - self.baseline_entropy)
        
        # Optional history (memory management)
        if len(self.history) < 300:
            self.history.append(self.coherence.copy())
    
    def get_global_coherence(self) -> float:
        """How much extra order is currently present in matter across the system"""
        return float(self.global_extra_order)
    
    def get_manifestation_potential(self) -> float:
        """
        Very rough proxy for how close we are to "physical manifestation" territory
        (extremely rare in realistic conditions)
        """
        strong_fraction = np.mean(self.coherence > 0.75)
        return strong_fraction * self.global_extra_order * 10.0  # arbitrary scaling
    
    def visualize(self, title: str = "GraceMatter - Emergent Coherence"):
        """Show current coherence state of matter"""
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(self.coherence,
                      cmap='viridis',
                      vmin=0.0, vmax=0.9,
                      interpolation='bicubic')
        ax.set_title(f"{title}\n"
                    f"global extra order ≈ {self.global_extra_order:.4f}  |  "
                    f"manifestation potential ≈ {self.get_manifestation_potential():.4f}")
        plt.colorbar(im, ax=ax, label='local matter coherence (0=random ←→ 1=ordered)')
        ax.axis('off')
        plt.tight_layout()
        plt.show()


# ──────────────────────────────────────────────
# Example usage pattern (how it connects to GraceMedium)
# ──────────────────────────────────────────────

if __name__ == "__main__":
    from grace_medium import GraceMedium  # assuming you have the previous file
    
    medium = GraceMedium(size=256)
    matter = GraceMatter(size=256)
    
    print("Matter responding to GraceMedium...\n")
    
    for step in range(1800):
        medium.step()
        
        # Every 200 steps simulate a strong resonance pulse somewhere
        if step % 200 == 80:
            pulse = np.zeros_like(medium.medium)
            cx, cy = np.random.randint(60, 196, 2)
            rr, cc = np.ogrid[:medium.size, :medium.size]
            mask = (rr - cx)**2 + (cc - cy)**2 < 28**2
            pulse[mask] = 0.12 + np.random.uniform(-0.03, 0.04, mask.sum())
            medium.medium += pulse
        
        # Matter always tries to feel what's happening in the medium
        matter.update_from_medium(medium.medium)
        
        if step % 400 == 0:
            print(f"step {step:4d} | "
                  f"matter coherence = {matter.get_global_coherence():.4f}  | "
                  f"manifestation pot ≈ {matter.get_manifestation_potential():.5f}")
    
    matter.visualize("GraceMatter after sustained subtle listening")