import numpy as np
from scipy.ndimage import gaussian_filter

class GraceField:
    """
    GraceField - Accumulation + Manifestation
    ==========================================
    
    The non-tangible "reality" layer where GraceMatter pools and accumulates.
    This is the ethereal ocean / dream-space where emergent coherence gathers,
    builds potential, and — when saturated enough — manifests back into
    tangible/physical form.
    
    Core mechanics:
    • Accumulates "coherence overflow" from GraceMatter (or other sources)
    • Slowly diffuses and builds density in this higher-level space
    • Has a baseline "ethereal hum" that keeps it faintly alive
    • When local density exceeds rare thresholds, "manifestation events" occur:
      - Represented as sudden spikes/crystallizations (e.g., miracles)
    • Manifestations are probabilistic and rare — reflecting real-world subtlety
    
    This layer closes the loop: Substrate (Medium) → Emergence (Matter) → Pool (Field) → Back to physical.
    
    Philosophy: Accumulation isn't hoarding; it's patience. Manifestation isn't magic; it's when the dream gets so coherent it wakes up as reality.
    """
    
    def __init__(self,
                 size: int = 256,                     # spatial resolution (matches others)
                 accumulation_rate: float = 0.008,    # how quickly coherence pools here
                 diffusion: float = 0.085,            # ethereal spread (slower than medium)
                 baseline_hum: float = 0.00025,       # faint non-tangible presence
                 decay: float = 0.989,                # slower fade than medium (holds longer)
                 manifestation_threshold: float = 0.75,  # high bar for crystallization
                 manifestation_strength: float = 0.12,   # size of manifestation events
                 fluctuation: float = 0.0018,          # subtle ethereal breathing
                 seed: int = 42):
        
        np.random.seed(seed)
        self.size = size
        
        self.accum_rate = accumulation_rate
        self.diffusion = diffusion
        self.baseline = baseline_hum
        self.decay = decay
        self.manifest_thresh = manifestation_threshold
        self.manifest_strength = manifestation_strength
        self.fluctuation = fluctuation
        
        # Core state: accumulation density (starts very low)
        self.field = np.random.normal(0.0, 0.004, (size, size))
        self.field = np.clip(self.field, -0.05, 0.12)
        
        # Track manifestation events (locations where "crystallization" happened)
        self.manifestations = []  # list of (step, x, y, strength) tuples
        
        # History for visualization
        self.history = []
    
    def accumulate_from_matter(self, matter_coherence: np.ndarray):
        """
        Pool overflow from GraceMatter's emergent coherence
        
        Args:
            matter_coherence: 2D array from GraceMatter.coherence (0-1 order levels)
        """
        if matter_coherence.shape != (self.size, self.size):
            from scipy.ndimage import zoom
            zoom_factors = (self.size / matter_coherence.shape[0],
                           self.size / matter_coherence.shape[1])
            matter_coherence = zoom(matter_coherence, zoom_factors, order=1)
        
        # Only accumulate where matter is meaningfully coherent (overflow)
        overflow_mask = matter_coherence > 0.45
        overflow = np.clip(matter_coherence[overflow_mask] - 0.45, 0.0, 0.55)
        
        # Gently add to field
        self.field[overflow_mask] += self.accum_rate * overflow
    
    def step(self):
        """
        One step of accumulation + potential manifestation
        """
        # 1. Baseline ethereal hum — the field is always faintly "dreaming"
        self.field += self.baseline
        
        # 2. Slow diffusion — accumulations spread dreamily
        smoothed = gaussian_filter(self.field, sigma=self.diffusion)
        self.field = 0.88 * self.field + 0.12 * smoothed
        
        # 3. Gentle decay — holds longer, but still needs fresh input
        self.field *= self.decay
        
        # 4. Subtle fluctuations — the breath of non-tangible reality
        noise = np.random.normal(0, self.fluctuation, self.field.shape)
        self.field += noise
        
        # 5. Check for manifestation events (rare crystallization)
        potential_sites = self.field > self.manifest_thresh
        if np.any(potential_sites):
            # Probabilistic: only some sites actually manifest (belief variability)
            manifest_prob = (self.field[potential_sites] - self.manifest_thresh) * 3.5
            manifest_prob = np.clip(manifest_prob, 0.0, 0.85)  # max 85% chance
            manifests = np.random.random(size=manifest_prob.shape) < manifest_prob
            
            if np.any(manifests):
                # Record events
                ys, xs = np.where(potential_sites)
                for y, x, prob in zip(ys[manifests], xs[manifests], manifest_prob[manifests]):
                    strength = self.manifest_strength * prob
                    self.manifestations.append((len(self.history), y, x, strength))
                    
                    # Feedback: manifestation "releases" some density back (like waking)
                    self.field[y, x] -= strength * 0.65
        
        # Bounds
        self.field = np.clip(self.field, -0.08, 0.88)
        
        # History
        if len(self.history) < 400:
            self.history.append(self.field.copy())
    
    def get_global_accumulation(self) -> float:
        """Overall density in the field"""
        return float(np.mean(self.field))
    
    def get_manifestation_count(self) -> int:
        """How many crystallization events have occurred"""
        return len(self.manifestations)
    
    def visualize(self, title: str = "GraceField - Accumulation State"):
        """Visualize current field with manifestation markers"""
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(self.field,
                      cmap='plasma',
                      vmin=-0.05, vmax=0.65,
                      interpolation='bicubic')
        
        # Mark recent manifestations
        recent = [m for m in self.manifestations[-8:] if m[0] > len(self.history) - 50]
        for step, y, x, strength in recent:
            ax.plot(x, y, 'o', color='white', markersize=8 + 20*strength, alpha=0.75)
            ax.plot(x, y, 'o', color='yellow', markersize=4 + 15*strength, alpha=0.85)
        
        ax.set_title(f"{title}\n"
                    f"global accumulation ≈ {self.get_global_accumulation():.4f}  |  "
                    f"manifestations: {self.get_manifestation_count()}")
        plt.colorbar(im, ax=ax, label='ethereal accumulation density')
        ax.axis('off')
        plt.tight_layout()
        plt.show()


# ──────────────────────────────────────────────
# Example integration pattern (with GraceMedium + GraceMatter)
# ──────────────────────────────────────────────

if __name__ == "__main__":
    # Assuming you have the previous classes/files
    # from grace_medium import GraceMedium
    # from grace_matter import GraceMatter
    
    # medium = GraceMedium(size=256)
    # matter = GraceMatter(size=256)
    field = GraceField(size=256)
    
    print("GraceField accumulating and waiting to manifest...\n")
    
    for step in range(2400):
        # Simulate the loop: Medium → Matter → Field
        # medium.step()  # (in full integration)
        # matter.update_from_medium(medium.medium)
        # Here: fake some matter coherence input
        if step % 250 == 100:
            fake_coherence = np.zeros((field.size, field.size))
            cx, cy = np.random.randint(50, 206, 2)
            rr, cc = np.ogrid[:field.size, :field.size]
            mask = (rr - cx)**2 + (cc - cy)**2 < 32**2
            fake_coherence[mask] = 0.62 + np.random.uniform(-0.15, 0.18, mask.sum())
            field.accumulate_from_matter(fake_coherence)
        
        field.step()
        
        if step % 500 == 0:
            print(f"step {step:4d} | "
                  f"accumulation = {field.get_global_accumulation():.4f}  | "
                  f"manifestations: {field.get_manifestation_count()}")
    
    field.visualize("GraceField after prolonged accumulation")