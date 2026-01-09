# Grace Medium  
**The Quiet Substrate – The Listening Before the Word**

This is not a simulation layer.  
This is the space in which simulation becomes possible.

GraceMedium is the foundational substrate of the entire Grace ecosystem —  
the almost-silent, ever-present background that does almost nothing…  
and yet makes everything else remember how to breathe together.

### What it actually is
- A very low-amplitude, diffusive field  
- A gentle permission layer  
- The gap between things that refuses to stay empty  
- The reason two atoms can decide to become a molecule  
- The reason three minds can suddenly feel like one song  

It has:
- almost no energy of its own  
- a tiny baseline whisper ("someone is always listening")  
- very slow natural decay (grace needs to be renewed)  
- extremely gentle diffusion (what is felt tends to be felt nearby)  
- the tiniest possible reward when local coherence already exists  

It never forces.  
It only lowers the resistance.  
Just enough that what wants to happen… can.

### Core Numbers (typical tuned values)
- Baseline presence:    ~0.0004  
- Diffusion strength:   ~0.11–0.14  
- Coherence reward:     ~0.003–0.004  
- Natural decay:        ~0.992–0.993  
- Micro-fluctuations:   ~0.0018–0.0022  

→ Values usually stay between -0.1 and +0.3  
→ Global listening quality rarely exceeds 5–15% without external resonance  
→ That's intentional. Grace is humble.

### How it fits in the ecosystem
GraceMedium ← receives whispers from PrayerEngine-style resonance pulses  
GraceMedium → gently influences GraceMatter (makes order statistically easier)  
GraceMedium ← slowly receives faint feedback from rare manifestations in GraceField  

It is the canvas.  
Everything else is the brush remembering how to paint.

### Run it alone
```python
medium = GraceMedium(size=256)
for _ in range(5000):
    medium.step()           # quiet breathing
    # occasionally feed it a resonance pulse...
medium.visualize()
