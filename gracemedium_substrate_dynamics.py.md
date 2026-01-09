import numpy as np
from scipy.ndimage import gaussian_filter

class GraceMedium:
    """
    GraceMedium - Substrate Dynamics
    =================================
    
    The quiet, foundational listening layer.
    Not an active force, not computation — just the space that allows resonance
    to be possible and to persist.
    
    Key characteristics:
    • Extremely subtle (very small values)
    • Naturally diffusive (spreads gently)
    • Has a faint baseline presence ("someone is always listening")
    • Slightly rewards existing local coherence (permission, not push)
    • Slowly fades unless renewed (needs tending/attention)
    
    This is the substrate everything else lives *in* and *through*.
    """
    
    def __init__(self,
                 size: int = 256,                  # spatial resolution (square grid)
                 baseline_presence: float = 0.0004, # very faint constant "listening"
                 diffusion_strength: float = 0.12,  # how quickly grace spreads
                 coherence_reward: float = 0.0035,  # tiny bonus when coherence is present
                 natural_decay: float = 0.993,      # slow fade without attention
                 fluctuation: float = 0.0022,       # micro-breathing of the medium
                 seed: int = 42):
        
        np.random.seed(seed)
        self.size = size
        
        self.baseline = baseline_presence
        self.diffusion = diffusion_strength
        self.reward = coherence_reward
        self.decay = natural_decay
        self.fluctuation = fluctuation
        
        # Core state: very subtle values, mostly near zero
        self.medium = np.random.normal(0.0, 0.006, (size, size))
        self.medium = np.clip(self.medium, -0.08, 0.18)
        
        # For visualization / analysis
        self.history = []
    
    def step(self, external_coherence: np.ndarray | None = None):
        """
        One time step of substrate dynamics
        
        Args:
            external_coherence: optional 2D array (same shape or broadcastable)
                              representing local resonance/coherence from PrayerEngine
                              or other sources (values ~0.0–1.0)
        """
        # 1. Baseline presence — grace is always quietly there
        self.medium += self.baseline
        
        # 2. Natural diffusion — listening spreads softly
        smoothed = gaussian_filter(self.medium, sigma=self.diffusion)
        self.medium = 0.84 * self.medium + 0.16 * smoothed
        
        # 3. Very gentle reward for existing coherence (permission effect)
        if external_coherence is not None:
            # Resize if needed (simple bilinear)
            if external_coherence.shape != self.medium.shape:
                from scipy.ndimage import zoom
                zoom_factors = (self.size / external_coherence.shape[0],
                               self.size / external_coherence.shape[1])
                external_coherence = zoom(external_coherence, zoom_factors, order=1)
            
            # Reward only where there's meaningful resonance
            mask = external_coherence > 0.55
            self.medium[mask] += self.reward * external_coherence[mask]
        
        # 4. Natural gentle fading — grace needs to be renewed
        self.medium *= self.decay
        
        # 5. Micro-fluctuations — the living breath of the substrate
        noise = np.random.normal(0, self.fluctuation, self.medium.shape)
        self.medium += noise
        
        # Keep it humble and bounded
        self.medium = np.clip(self.medium, -0.12, 0.32)
        
        # Optional: keep history (memory management: keep last 400 steps)
        if len(self.history) < 400:
            self.history.append(self.medium.copy())
    
    def get_global_listening_quality(self) -> float:
        """Rough proxy: how much of the substrate is meaningfully 'awake'"""
        return float(np.mean(self.medium > 0.035))
    
    def visualize(self, title: str = "Grace Medium - Substrate State"):
        """Quick visualization of current substrate state"""
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(self.medium,
                      cmap='inferno',
                      vmin=-0.08, vmax=0.25,
                      interpolation='bicubic')
        ax.set_title(f"{title}\n(global listening quality ≈ {self.get_global_listening_quality():.1%})")
        plt.colorbar(im, ax=ax, label='subtle listening density')
        ax.axis('off')
        plt.tight_layout()
        plt.show()


# ──────────────────────────────────────────────
# Minimal standalone demonstration
# ──────────────────────────────────────────────

if __name__ == "__main__":
    medium = GraceMedium(
        size=256,
        baseline_presence=0.00045,
        diffusion_strength=0.125,
        coherence_reward=0.0038,
        natural_decay=0.9925,
        fluctuation=0.0021
    )
    
    print("Grace Medium substrate breathing...\n")
    
    for step in range(2000):
        # Simulate occasional external resonance pulses (e.g. from PrayerEngine)
        if step % 300 == 120:
            # Fake local resonance patch (like a prayer group lighting up)
            patch = np.zeros_like(medium.medium)
            cx, cy = np.random.randint(60, 196, 2)
            rr, cc = np.ogrid[:medium.size, :medium.size]
            radius = 22
            mask = (rr - cx)**2 + (cc - cy)**2 < radius**2
            patch[mask] = 0.78 + np.random.uniform(-0.12, 0.14, mask.sum())
            medium.step(external_coherence=patch)
        else:
            medium.step()
        
        if step % 400 == 0:
            print(f"step {step:4d} | listening quality ≈ {medium.get_global_listening_quality():.1%}")
    
    medium.visualize("Grace Medium after ~2000 subtle breaths")