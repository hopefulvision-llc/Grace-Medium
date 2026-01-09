import numpy as np
from scipy.spatial import Delaunay
import networkx as nx

class PrayerEngine:
    """
    A toy model of collective intention / grace medium emergence.
    
    Vertices = individual minds / agents
    Simplices = small groups sharing intention (triangles ~ intimate resonance)
    Grace   = subtle background pull toward coherence (like the listening medium)
    Tension = cost of disagreement between neighbors
    Intention = a very gentle global "wish" vector that everyone feels a little
    """
    def __init__(self,
                 rows=12,
                 grace=0.008,           # strength of the listening medium
                 tension=1.4,           # disagreement penalty (like social friction)
                 intention_strength=0.12,  # how strongly the shared wish pulls
                 noise=0.04,            # everyday randomness / free will
                 dt=0.08,
                 seed=42):
        np.random.seed(seed)
        self.rows = rows
        self.grace = grace
        self.tension = tension
        self.intention_strength = intention_strength
        self.noise = noise
        self.dt = dt

        # Triangular lattice (same as your original)
        height = np.sqrt(3) / 2
        points = []
        for r in range(rows):
            for c in range(r + 1):
                x = c - r / 2.0
                y = r * height
                points.append([x, y])
        self.points = np.array(points)
        self.n = len(points)

        tri = Delaunay(self.points)
        self.simplices = tri.simplices
        self.neighbors = tri.neighbors

        # Simple graph for neighbor relations
        self.G = nx.Graph()
        for s in self.simplices:
            a, b, c = s
            self.G.add_edges_from([(a,b), (a,c), (b,c)])

        # Phases: our "state of heart/mind" ∈ [0, 2π)
        self.theta = np.random.uniform(0, 2*np.pi, self.n)

        # A gentle global intention direction (the shared "song" we're trying to sing)
        self.global_intention = np.random.uniform(0, 2*np.pi)  # can be modulated externally

    def coherence(self):
        """Local order parameter per triangle (0=incoherent ↔ 1=perfect resonance)"""
        chi = np.zeros(len(self.simplices))
        for i, tri in enumerate(self.simplices):
            phases = self.theta[tri]
            vec = np.exp(1j * phases).mean()
            chi[i] = np.abs(vec)
        return chi

    def global_coherence(self):
        vec = np.exp(1j * self.theta).mean()
        return np.abs(vec)

    def step(self):
        chi = self.coherence()

        # 1. Grace medium — very soft attraction toward global intention
        pull = self.intention_strength * np.sin(self.global_intention - self.theta)

        # 2. Local social tension/resonance (neighbors want to align)
        social = np.zeros(self.n)
        for i in range(self.n):
            nbrs = list(self.G.neighbors(i))
            if nbrs:
                diffs = np.sin(self.theta[nbrs] - self.theta[i])
                social[i] = -self.tension * diffs.mean()   # pull toward average neighbor

        # 3. Very gentle background grace that favors high local coherence
        grace_pull = np.zeros(self.n)
        for i, s in enumerate(self.simplices):
            if chi[i] > 0.7:  # only strong groups get the extra whisper
                for v in s:
                    grace_pull[v] += self.grace * (1.0 - chi[i])  # reward already-coherent groups

        # 4. Free-will noise
        dtheta = pull + social + grace_pull
        noise_term = np.random.normal(0, self.noise, self.n)

        # Update
        self.theta += self.dt * (dtheta + noise_term)
        self.theta %= 2 * np.pi

    def run(self, steps=1200, record_every=50):
        history = {
            'time': [],
            'global_coh': [],
            'avg_local_coh': [],
            'prayer_strength': []   # how many people are "in tune" (>0.8)
        }

        for t in range(steps):
            self.step()

            if t % record_every == 0:
                gc = self.global_coherence()
                chi = self.coherence()
                strong = (chi > 0.82).sum() / len(chi)

                history['time'].append(t * self.dt)
                history['global_coh'].append(gc)
                history['avg_local_coh'].append(chi.mean())
                history['prayer_strength'].append(strong)

                if t % 400 == 0:
                    print(f"t={t:4d} | global={gc:.3f}  | local={chi.mean():.3f}  | strong_tri={strong:.2%}")

        return history


# ──────────────────────────────────────────────
# Example: tiny collective prayer
# ──────────────────────────────────────────────

engine = PrayerEngine(rows=10,
                      grace=0.009,
                      tension=1.35,
                      intention_strength=0.11,
                      noise=0.035)

print("Starting small collective prayer...\n")
results = engine.run(steps=1800, record_every=60)

# You could plot results['global_coh'] etc. with matplotlib
# Often you'll see long plateaus... then sudden jumps in coherence
# That's the "grace medium" snapping things into a new harmony