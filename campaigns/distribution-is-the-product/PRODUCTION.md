# Production Bible: "THE CURRENT"

## 1. Visual rules

**Industrial Race (B&W)**
- 35mm/65mm black-and-white negative look, heavy silver grain, crushed blacks, halation on every light source.
- Lenses: vintage spherical, shallow depth of field, soft edges. Hand-cranked 18fps cadence with a slight exposure flicker.
- Light comes only from **practical sources**: filaments, arc lamps, projector beams. Subjects are lit from below or the side, never flat.
- The **one exception:** a filament may glow faint orange in an otherwise monochrome frame. It's the "spark" motif.

**Intelligence Race (COLOR)**
- Two temperatures only: **warm Kodachrome amber** (people, the city, golden hour, as in ref 5) and **cold UI cyan-white** (screens, data, the canvas).
- Lenses: anamorphic, clean, slow push-ins. 24fps. No handheld shake. Everything is controlled.
- UI is **diegetic and minimal**. Don't show a real Default screenshot until the logo, and use stylized "canvas" lines instead of literal dashboards.

**The bridge**
- Every era transition is a **match cut on the tick**: filament → cursor, shutter → form click, switchboard plug → routing line, 82 windows → city grid.

## 2. Sound and score

- **The tick** is recorded from a real 19th-century pocket watch and pitched and layered as it evolves:
  watch → dynamo → projector shutter → switchboard relay → form click → calendar chime.
- **Tempo map:** 60 bpm (0:00) → 72 (0:14) → 84 (0:26) → 96 (0:36) → *stumble* (0:41) → 120 (0:51) → 144 (1:04) → 60, controlled (1:12) → **stop** (1:26).
- **Score:** solo violin plus a low string cluster over a rising **Shepard tone** from 0:48 to 1:10. Reference the *feeling* of Göransson's *Oppenheimer* and Zimmer's *Dunkirk* only. Commission an original piece and don't temp with licensed tracks you can't clear.
- **The last 3 seconds are silent.** That's the most important sound in the spot.

## 3. Voice

- Male or female, 45–65, a low register with a slight rasp and **no trailer cadence**. The read should sound like testimony at a hearing, close-miked and dry.
- Pace: about 105 wpm. Pause after "useless.", "farther." and "One current."
- ElevenLabs or Higgsfield direction: *"Measured, intimate, grave. A historian telling you a secret. No upward inflection. Stability high, style low."*

## 4. Shot-by-shot generation prompts

Paste each prompt as a still (image model) first, approve it, then animate it (image-to-video). Append the matching **style suffix** to every prompt.

**STYLE SUFFIX: B&W**
> shot on 65mm black and white film, heavy silver halide grain, deep crushed blacks, strong halation on light sources, low-key chiaroscuro lighting, 1.43:1 IMAX framing, Christopher Nolan Oppenheimer aesthetic, period-accurate, photoreal, no text

**STYLE SUFFIX: COLOR**
> anamorphic 2.39:1, warm Kodachrome amber skin tones against cold cyan screen light, shallow depth of field, slow push-in, photoreal, cinematic, Roger Deakins lighting, no logos, no readable text

| # | Shot | Image prompt | Motion prompt (video) |
|---|---|---|---|
| 01 | Filament | Extreme macro of a carbon filament inside a hand-blown glass bulb, the filament glowing faint orange, the only color in a black-and-white frame | Filament slowly brightens from dark to full glow, glass refracts light, slight heat shimmer |
| 02 | The bulb | A distinguished white-haired man in a 1920s three-piece suit and bow tie stands beside an enormous glass light bulb on a draped pedestal, holding a tiny bulb in his open palm, stern expression, theater curtain behind *(ref 4; use an actor, not a real-person likeness)* | Very slow push-in on his face, the giant bulb flickers once |
| 03 | Founder, 2 a.m. | A young founder in a dark apartment lit only by a laptop, hoodie, staring at an empty calendar, city lights out of focus behind | Static, the cursor blinks, their eyes don't move |
| 04 | Launch flood | A grid of dozens of near-identical glowing product launch web pages with purple gradients, floating in black space, receding to infinity | Pages slam in one by one, stacking like dominoes, accelerating |
| 05 | Pearl Street | 1882 Lower Manhattan night street, workmen in shirtsleeves digging up cobblestones and laying iron conduit pipes, copper cable spooled on wooden drums, gas lamps | Slow crane down from rooftops to the trench, men feed cable into the ground |
| 06 | Dynamo hall | A cathedral-like 1880s power station interior, rows of massive dynamos, a hand in a shirt cuff throws a brass knife switch | Dynamos spin up, sparks, the switch slams closed |
| 07 | 82 windows | A dark 1880s brick street at night, rows of windows, every window dark | Windows light up one by one in rhythm, left to right, filament glow |
| 08 | Meter | Macro of an antique electrolytic electricity meter on a wooden wall, glass jars, zinc electrodes, brass terminals | Rack focus from wires to the jars, faint bubbling |
| 09 | The Trust | 1908 boardroom, long oak table, men in dark suits and mustaches signing a document, film canisters sealed with red wax in the foreground | Pens scratch, a wax seal is pressed, projector light flickers across faces |
| 10 | Reels on the road | A long column of 1910 delivery trucks loaded with film reel cans leaving a brick depot at dawn | Trucks roll out toward the camera, dust, flicker |
| 11 | AC lines | Tall wooden utility poles marching across an empty plain to the horizon, cables catching the light, Niagara-like mist in the distance | Slow lateral track along the poles, wind in the wire |
| 12 | Lineman | Silhouette of a lineman at the top of a pole against a blinding white sky, wire running past him into the distance | Hold, then the camera follows the wire away from him |
| 13 | Switchboard | 1920s telephone switchboard operator in profile, headset, lifting a patch cable toward a wall of jacks *(ref 2)* | She plugs the cable in. **Match-cut frame:** end on a tight close-up of the plug entering the jack |
| 14 | Canvas | A glowing cyan line plugs into a node on a dark workflow canvas, the line forking into branches, minimal and abstract | Starts on the plug close-up (matching shot 13), color floods outward along the lines |
| 15 | Buyer, 11:58 | An executive in a dim home office at night, cursor hovering over a softly glowing button | They click, a soft light pulse ripples from the button |
| 16 | Enrich | Abstract data cascade, translucent cards of firmographic fields falling in a waterfall of light against black | Cards fall and lock into a single record, like a fuse burning down |
| 17 | Route | A single light path forks across a dark grid of nodes, choosing one, landing on a glowing avatar | Fast, decisive, the path lights up end to end |
| 18 | Schedule | A calendar grid appears on the same screen, one slot fills with warm light | The slot fills, gentle bloom |
| 19 | Vitruvian | A GTM operator in a Vitruvian Man pose inside a drawn circle, half of the body human, half luminous circuitry and agent wiring, white line art on black *(ref 3, but no weapons; the machine half is cables, nodes and light)* | Circuit lines animate from the heart outward through the arms |
| 20 | The orbit | A presenter in a 1950s suit (or a modern RevOps lead) points up at a huge sculpture of wire orbits suspended in darkness, a glowing sphere at the center, a small group watching *(ref 1)* | Orbits light up node by node, like a city grid switching on, the camera cranes up |
| 21 | The tower | A founder in a tailored suit sits in a leather chair by a huge window high above Manhattan at golden hour, sipping coffee, plants and a brass lamp, warm haze *(ref 5)* | Very slow push-in, steam from the cup, the city below begins to light up |
| 22 | The grid | A Manhattan aerial at dusk, city blocks switching on grid by grid | Blocks light in rhythm, mirroring shot 07 |

**Recommended pipeline:** image model for stills → image-to-video (Kling / Veo / Higgsfield DoP) at 5–8s per shot → grade in Resolve (B&W: monochrome film LUT plus grain; COLOR: Kodachrome emulation) → sound design built on the tick map above.

## 5. Campaign extensions

**Launch sequence (4 weeks)**
1. **Week 1: Tease.** Three 6s bumpers on LinkedIn and X. B&W only, no logo, just *"Anyone can build the bulb."*
2. **Week 2: Hero.** The 90s film plus a founder letter, *"Why distribution is the product"*.
3. **Week 3: Proof.** *"Nine Seconds"* 15s spots built on real customer form-to-meeting times (Cortex, etc.).
4. **Week 4: Tool.** A "How fast is your current?" speed-to-lead audit: submit your own demo form and Default times your response.

**OOH / print (B&W photography, one line each)**
- *"The bulb was the easy part."*
- *"1882: 82 customers. Built the grid first."*
- *"Edison lost to a current that traveled farther."*
- *"Your product is only as good as the wire it travels on."*
- *"Every era has a switchboard."*
- Sign-off on all: **Distribution is the Product. · Default**

**LinkedIn copy (hero launch)**
> Everyone remembers the bulb.
> Nobody remembers it was useless without the wire.
>
> In the AI race, products get copied in weeks. What can't be copied is how fast you reach the buyer: the moment they raise their hand, enriched, qualified, routed and booked before the tab closes.
>
> Edison needed a power plant, a trust and an army of linemen.
> You need Default.
>
> **Distribution is the Product.** ▶︎ [film]

**Landing page**
- H1: **Distribution is the Product.**
- Sub: *Anyone can build the bulb. Default is the current: inbound, enrichment, routing and scheduling, run as one system by your team and its agents.*
- CTA: **Time your current →** (the speed-to-lead audit)
