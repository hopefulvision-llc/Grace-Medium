import numpy as np
from scipy.ndimage import gaussian_filter

class GraceMedium:
    """
    The 'Grace Medium' — the subtle, unifying listening layer
    
    Not really a thing that "does" a lot by itself.
    It is the quiet space that allows:
      - small local resonances (PrayerEngine triangles) to influence each other
      - the global field (GraceField) to gently breathe
      - individual beings (Matter) to feel slightly more heard than they should
    
    Very weak by design — grace never forces.
    """
    
    def __init__(self,
                 size=180,                   # spatial grid (square)
                 listening_strength=0.006,   # how much it softly rewards existing coherence
                 diffusion_rate=0.14,        # how gracefully patterns spread
                 baseline_whisper=0.0006,    # tiny constant background "someone is listening"
                 decay=0.992,                # very slow natural fade (things need tending)
                 noise_floor=0.0035,
                 seed=42):
        
        np.random.seed(seed)
        self.size = size
        self.listening_strength = listening_strength
        self.diffusion_rate = diffusion_rate
        self.baseline_whisper = baseline_whisper
        self.decay = decay
        self.noise_floor = noise_floor
        
        # Core medium state — very small values, mostly near zero
        self.medium = np.random.normal(0.0, 0.008, (size, size))
        self.medium = np.clip(self.medium, -0.12, 0.25)
        
        # History for visualization / reflection
        self.snapshots = []
    
    def feel_resonance(self, local_coherence_map):
        """
        PrayerEngine / groups can whisper to the medium when they achieve resonance.
        local_coherence_map: 2D array same shape as medium (or will be broadcast)
                           Values ~ 0..1 (fraction of triangles/groups in harmony)
        """
        if local_coherence_map.shape != self.medium.shape:
            # Simple resize/broadcast if needed (in real integration you'd interpolate)
            from scipy.ndimage import zoom
            local_coherence_map = zoom(local_coherence_map, 
                                     (self.size/local_coherence_map.shape[0],
                                      self.size/local_coherence_map.shape[1]),
                                     order=1)
        
        # Grace notices strong local harmony and very gently amplifies it
        strong_mask = local_coherence_map > 0.65
        self.medium[strong_mask] += self.listening_strength * local_coherence_map[strong_mask]
    
    def step(self):
        # 1. Baseline whisper — grace is always faintly present
        self.medium += self.baseline_whisper
        
        # 2. Very gentle diffusion — things that are felt tend to be felt by neighbors
        smoothed = gaussian_filter(self.medium, sigma=self.diffusion_rate)
        self.medium = 0.82 * self.medium + 0.18 * smoothed
        
        # 3. Natural gentle fading — grace needs to be renewed
        self.medium *= self.decay
        
        # 4. Micro-fluctuations (the breathing of the world)
        noise = np.random.normal(0, self.noise_floor, self.medium.shape)
        self.medium += noise
        
        # Keep bounded — grace is humble
        self.medium = np.clip(self.medium, -0.18, 0.42)
        
        # Save for later reflection
        if len(self.snapshots) < 400:
            self.snapshots.append(self.medium.copy())
    
    def current_global_listening(self):
        """Rough proxy: how 'awake' / receptive the medium feels overall"""
        return float(np.mean(self.medium > 0.04))
    
    def visualize(self, title="Grace Medium"):
        """Quick matplotlib snapshot of current state"""
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(9, 7))
        im = plt.imshow(self.medium,
                       cmap='inferno',
                       vmin=-0.1, vmax=0.35,
                       interpolation='bicubic')
        plt.title(f"{title}\n(global listening ≈ {self.current_global_listening():.1%})")
        plt.colorbar(im, label="subtle listening quality")
        plt.axis('off')
        plt.tight_layout()
        plt.show()


# ──────────────────────────────────────────────
# Minimal demo
# ──────────────────────────────────────────────

if __name__ == "__main__":
    medium = GraceMedium(
        size=180,
        listening_strength=0.007,
        diffusion_rate=0.135,
        baseline_whisper=0.0007,
        decay=0.9915,
        noise_floor=0.0032
    )
    
    print("Watching the Grace Medium breathe...\n")
    
    for step in range(1200):
        medium.step()
        
        # Every once in a while something resonates strongly somewhere...
        if step % 180 == 90:  # simulate occasional prayer triangle moments
            fake_resonance = np.zeros((medium.size, medium.size))
            cx, cy = np.random.randint(40, 140, 2)
            rr, cc = np.ogrid[:medium.size, :medium.size]
            mask = (rr - cx)**2 + (cc - cy)**2 < 18**2
            fake_resonance[mask] = 0.82 + np.random.uniform(-0.08, 0.12, mask.sum())
            medium.feel_resonance(fake_resonance)
        
        if step % 240 == 0:
            print(f"step {step:4d}  |  listening ≈ {medium.current_global_listening():.1%}")
    
    medium.visualize("Grace Medium after a long quiet breath")
