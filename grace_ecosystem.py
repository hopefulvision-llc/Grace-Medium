# GraceEcosystem - Full Integrated Loop
=====================================

This script ties together the four layers of the Grace system into one 
coherent, breathing simulation:

1. GraceMedium     → the quiet substrate / listening space
2. GraceMatter     → pre-existing matter responding to the medium
3. GraceField      → non-tangible accumulation & manifestation layer
4. (implicit) PrayerEngine-like resonance pulses → occasional strong local coherence

The loop runs as:
Medium ←→ Matter ←→ Field ←→ back to Medium (via manifestation feedback)

Philosophy in one sentence:
    Grace is not created — it is remembered, accumulated, and eventually 
    allowed to become visible again in the physical world.
"""

import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# ─── Minimal versions of each layer ─────────────────────────────────────────

class GraceMedium:
    def __init__(self, size=180):
        self.size = size
        self.medium = np.random.normal(0, 0.005, (size, size))
        self.medium = np.clip(self.medium, -0.06, 0.12)

    def step(self, external_coherence=None):
        self.medium += 0.00035                      # baseline whisper
        smoothed = gaussian_filter(self.medium, sigma=0.11)
        self.medium = 0.85 * self.medium + 0.15 * smoothed
        
        if external_coherence is not None:
            mask = external_coherence > 0.58
            self.medium[mask] += 0.0032 * external_coherence[mask]
        
        self.medium *= 0.993
        self.medium += np.random.normal(0, 0.0018, self.medium.shape)
        self.medium = np.clip(self.medium, -0.09, 0.28)


class GraceMatter:
    def __init__(self, size=180):
        self.size = size
        self.coherence = np.zeros((size, size))

    def update(self, medium):
        bonus = np.clip((medium - 0.06) * 6.5, 0, 0.022)
        self.coherence += bonus
        self.coherence += 0.012 * (0.0 - self.coherence)  # relax toward entropy
        self.coherence = np.clip(self.coherence, 0, 0.92)


class GraceField:
    def __init__(self, size=180):
        self.size = size
        self.field = np.random.normal(0, 0.003, (size, size))
        self.manifestations = []

    def accumulate(self, matter_coherence):
        overflow = np.clip(matter_coherence - 0.42, 0, 0.5)
        self.field += 0.007 * overflow

    def step(self):
        self.field += 0.00018                       # ethereal hum
        smoothed = gaussian_filter(self.field, sigma=0.08)
        self.field = 0.89 * self.field + 0.11 * smoothed
        self.field *= 0.988
        
        # Rare manifestation events
        candidates = self.field > 0.68
        if np.any(candidates):
            prob = np.clip((self.field[candidates] - 0.68) * 4.2, 0, 0.82)
            happened = np.random.random(prob.shape) < prob
            if np.any(happened):
                ys, xs = np.where(candidates)
                for y, x in zip(ys[happened], xs[happened]):
                    strength = 0.09 * prob[happened[ys == y][0]]
                    self.manifestations.append((len(self.manifestations), y, x, strength))
                    self.field[y, x] -= strength * 0.6  # release tension


# ─── Integrated Ecosystem ───────────────────────────────────────────────────

class GraceEcosystem:
    def __init__(self, size=180):
        self.size = size
        self.medium = GraceMedium(size)
        self.matter = GraceMatter(size)
        self.field = GraceField(size)
        
        self.history = {
            'medium_mean': [],
            'matter_mean': [],
            'field_mean': [],
            'manifest_count': []
        }

    def random_resonance_pulse(self):
        """Simulate occasional strong local prayer/resonance events"""
        pulse = np.zeros((self.size, self.size))
        if np.random.random() < 0.12:  # ~every 8–10 steps on average
            cx = np.random.randint(40, self.size-40)
            cy = np.random.randint(40, self.size-40)
            rr, cc = np.ogrid[:self.size, :self.size]
            mask = (rr - cx)**2 + (cc - cy)**2 < 24**2
            pulse[mask] = 0.68 + np.random.uniform(-0.14, 0.16, mask.sum())
        return pulse

    def step(self):
        # 1. Occasional resonance from "prayer" / collective attention
        pulse = self.random_resonance_pulse()

        # 2. Medium feels the resonance
        self.medium.step(external_coherence=pulse)

        # 3. Matter responds to the medium
        self.matter.update(self.medium.medium)

        # 4. Field accumulates overflow from matter
        self.field.accumulate(self.matter.coherence)

        # 5. Field evolves (diffusion, hum, rare manifestations)
        self.field.step()

        # 6. (optional) Feedback from manifestations → medium (very gentle)
        if self.field.manifestations:
            last = self.field.manifestations[-1]
            if last[0] == len(self.field.manifestations)-1:  # new one
                y, x = last[1], last[2]
                ripple = np.zeros_like(self.medium.medium)
                rr, cc = np.ogrid[:self.size, :self.size]
                dist = np.sqrt((rr-y)**2 + (cc-x)**2)
                ripple[dist < 18] = 0.018 * np.exp(-dist[dist < 18]/9)
                self.medium.medium += ripple

        # Record
        self.history['medium_mean'].append(float(np.mean(self.medium.medium)))
        self.history['matter_mean'].append(float(np.mean(self.matter.coherence)))
        self.history['field_mean'].append(float(np.mean(self.field.field)))
        self.history['manifest_count'].append(len(self.field.manifestations))

    def run(self, steps=1200, record_every=40):
        print("Grace Ecosystem breathing together...\n")
        for i in range(steps):
            self.step()
            if i % record_every == 0:
                m = len(self.field.manifestations)
                print(f"step {i:4d} | "
                      f"medium: {self.history['medium_mean'][-1]:.4f}  | "
                      f"matter: {self.history['matter_mean'][-1]:.4f}  | "
                      f"field: {self.history['field_mean'][-1]:.4f}  | "
                      f"manifest: {m}")

    def plot_summary(self):
        fig, axs = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
        
        axs[0].plot(self.history['medium_mean'], label='Medium (substrate)')
        axs[0].set_ylabel('listening density')
        axs[0].legend()
        
        axs[1].plot(self.history['matter_mean'], label='Matter (coherence)', color='C2')
        axs[1].set_ylabel('order level')
        axs[1].legend()
        
        axs[2].plot(self.history['field_mean'], label='Field (accumulation)', color='C3')
        axs[2].set_ylabel('ethereal density')
        axs[2].legend()
        
        axs[3].plot(self.history['manifest_count'], label='Manifestations', color='gold')
        axs[3].set_ylabel('count')
        axs[3].set_xlabel('time steps')
        axs[3].legend()
        
        plt.suptitle("Grace Ecosystem — Full Loop Evolution")
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()


# ─── Run example ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ecosystem = GraceEcosystem(size=180)
    
    try:
        ecosystem.run(steps=1800, record_every=60)
        ecosystem.plot_summary()
    except KeyboardInterrupt:
        print("\nInterrupted. Showing current state...")
        ecosystem.plot_summary()
