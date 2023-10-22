# Quantum Proprioception

Quantum Proprioception is a protocol that allows two parties to securely determine their relative orientation in three-dimensional space.

<i>Note: The word "[proprioception](https://en.wikipedia.org/wiki/Proprioception)" comes from the sense we have of the orientation of our body parts (also known as kinaesthesia).</i>

## The Big Idea

Quantum Proprioception allows two observers to determine their relative orientation in three-dimensional space. It has important functions in a quantum internet, such as the remote alignment of measuring apparatus, and enables potentially transformative applications in industry and for broader society.

The Quantum Proprioception protocol is based on the approach proposed by Rezazadeh et al<sup>[1](#References)</sup> in 2017. It is similar to the well-established technique of Quantum Key Distribution. In QKD, Alice and
Bob announce their reference systems (their qubit bases) but keep secret the results of
measurements they make on EPR pairs that they share. By comparing their results and discarding
those that do not match, they can share a private key.

In Quantum Proprioception, the reference systems are secret but the results of the measurements
are shared. Using this, Bob can determine his orientation relative to Alice with arbitrary accuracy. A
useful by-product of this process is that each party’s reference frame remains private, with only the
difference between them being shared publicly.

In more detail, imagine that Alice and Bob are both able to measure photons in orthogonal bases but
with equipment that is not aligned. Alice wishes to transmit her reference frame to Bob so that he
can align his measurement bases with hers.
They create and share a set of $N$ EPR pairs and perform a measurement on each photon. They then
share their results over a classical channel and compare their measurements.

Rezazadeh et al show that the results are correlated in a way that depends on the relative
orientations of the measurement bases. By comparing the number of measurement outcomes in
each base, Alice and Bob can determine the difference in the alignment of one axis with an accuracy
that increases with $\frac{N}{N+2}$, and by repeating this process for each axis, Alice and Bob can determine their relative orientation in three dimensions.

## Comparison with Classical Orientation Techniques

Quantum Proprioception is a significant improvement over classical orientation techniques. These
generally require carefully calibrated “reference monuments” against which the position and
orientation of local objects can be compared using standard surveying techniques.

For example, the construction of the Laser Interferometer Gravitational Wave Observatory, LIGO<sup>[2](#References)</sup>, at
two locations in the United States required the alignment of local coordinate systems to within
0.005 metres RMS while separated by a distance of 3001.8 km.
This was a complex process requiring numerous detailed measurements and calibrations. The orientation of each interferometer arm was defined by the establishment of a reference monument at each end. The position of these reference monuments had to be determined with differential GPS to with an accuracy of 2mm relative to the (then) standard geodetic ellipsoid, [WGS-84](https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84). The accuracy of the arm orientation was then determined by the accuracy of these two position
measurements.
(Interferometer arms are extended cylinders that are symmetrical along their length. That’s why
their orientation can be determined with two reference monuments. In general, a non-symmetrical
three-dimensional object requires three classical reference measurements to determine its
orientation).

By contrast, Quantum Proprioception gives the orientation at each location. This reduces the
number of required reference monuments or improves accuracy and redundancy, compared to
classical orientation sensing.
Quantum Proprioception also acts non-locally and securely in a way that has no classical analogue.

# Quantum Internet Applications

The misalignment of quantum measuring apparatus is an important source of error in many
quantum applications. These errors reduce fidelity and open potential security holes. Various
security protocols exist to account for these errors, at least in theory<sup>[3](#References)</sup>. However, a simple way to
measure and reduce misalignment would mitigate the problem.

Quantum Proprioception performs this task. If adopted as a standard handshake protocol, it would
automatically determine the relative orientations of all devices on a quantum network. This
essentially establishes a standard orientation for the quantum internet.

## Standard Orientation

What should the quantum internet be oriented relative to? One candidate reference system is the
International Terrestrial Reference Frame (ITRF)<sup>[4](#References)</sup> maintained by the International Earth Rotation and
Reference System Service <sup>[5](#References)</sup>. The ITRF is a geoid of approximately Earth size, that co-rotates with the
Earth around an origin at the planet’s centre of mass. The latest incarnation is known as ITRF2020
and this, or earlier versions of it like WGS-84, are used to calibrate the GPS, Galileo and BeiDou
satellite navigation systems (The Russian GLONASS system uses a separate reference frame<sup>[6](#References)</sup>).
If Alice were to align her apparatus with ITRF2020 at a specific location, then all consequent
Quantum Proprioception handshakes with Alice would be relative to this standard.

## Applications in Broader Society

Satellite navigation systems have transformed society. The ability to determine a location to within a
few metres or better, almost anywhere on the planet, underpins so many elements of modern life
that is hard to provide a comprehensive list. Industries from aerospace to banking and finance to
tourism, agriculture and healthcare all depend on satellite navigation in countless ways.

But satellite navigation systems provide only point location data while real objects are extended
entities. A full description of their status in three-dimensional space must specify their orientation as
well as their position. Quantum Proprioception provides this extra data.
Assuming the widespread future availability of a quantum internet and that the capabilities of a
standard quantum optics bench can be shrunk to chip-size, the combination of position-plus-orientation data opens up a host of applications.

Construction generally assembles three-dimensional components into a larger structure. Location
data for each component is certainly useful but does not allow construction by itself. By contrast,
position-plus-orientation data for each component enables accurate automated construction, at
scales ranging from bridges and skyscrapers to flat pack furniture and Lego blocks.
A Quantum Internet of Things with a Quantum Proprioception handshake could offer position-plus-orientation data for almost any object. This increases precision and coordination
between machines. It has implications for supply chain management, automated manufacture, self-driving vehicles, air traffic control, robotics and more.

Quantum Proprioception could also create local reference frames in otherwise closed or isolated
systems, such as submarines and spacecraft. Defence applications include the secure transmission of
targeting information—the ability to send not just the position of a target but its relative direction.
For these reasons, Quantum Proprioception is a foundational quantum technology that has the
potential to transform the way we exploit three-dimensional space.

# Description

Quantum Proprioception allows two parties to determine their relative orientation in three-
dimensional space. Imagine that Alice and Bob can measure photons in orthogonal bases but with
equipment that is not aligned. Alice wishes to transmit her reference frame to Bob so that he can
align his measurement bases with hers.

They create and share a set of n EPR pairs and perform a measurement on each photon. They then
share their results over a classical channel and compare their measurements.
The results must be correlated in a way that depends on the relative orientations of the
measurement bases. By comparing the number of measurement outcomes in each base, Alice and
Bob can determine the difference in the alignment of one axis with an accuracy that increases with
$\frac{N}{N+2}$. By repeating this process for each axis, Alice and Bob can determine their relative
orientation in three dimensions.

## Inputs

The accuracy of Quantum Proprioception depends on the number $N$ of EPR pairs that Alice and Bob
share. In an editor, you can choose this number. With $N=2$, the theoretical fidelity is about $0.86$
and with $N=10$ it is about $0.96$<sup>[1](#References)</sup>.
In the real world, the angle between Alice and Bob’s apparatus is unknown (because it is what the protocol
determines), but in this simulation, you must specify the angles (see [How to Run](#How-to-Run)).

## Results

The results page of the editor displays the output of the simulation, which should be an approximation the real angle. In the real world, Bob would use this angle to align his apparatus with Alice’s.

## Algorithm Summary

1. Alice and Bob measure their spins in two arbitrary directions only known to each of them separately.
2. Alice, publicly announces her measurements in the form of a sequence (a<sub>1</sub>, a<sub>2</sub>, · · · a<sub>k</sub>, · · ·), where a<sub>i</sub> = ±1.
3. Bob compares these measurements with his own: (b<sub>1</sub>, b<sub>2</sub>, · · · b<sub>k</sub>, · · ·), where b<sub>i</sub> = ±1.
4. Bob calculates the correlations between these two sequences, given by
$$q_{N=}\frac{1}{N}\sum_{i=1}^{N}{a_{i}\overline{b_i}}$$
which can be rewritten as
$$q_{N}=\frac{N_{+-}+N_{-+}-N_{++}-N_{--}}{N}=\frac{N_{d}-N_{s}}{N}=\frac{2N_{d}-N}{N}=2\cdot\frac{N_{d}}{N}-1$$
where $N_{ab}$ denotes the number of the times that Alice obtains a value of $a$ and Bob obtains a value of $b$, and $N_{d}$ and $N_{s}$ are the number of times that Alice and Bob obtain different and the same results respectively.  
6. As $N$ approaches infinity:
$$q_{\infty}=\cos\left(\theta\right)$$

# Execution

## Requirements

This program uses SquidASM. To install SquidASM, refer to their [github page](https://github.com/QuTech-Delft/squidasm).

## How to Run

The required arguments for the CLI are the angles. Due to way that SquidASM rotates the bases of its Qubits, the angle format used in this implementation is:
$$\frac{n\pi}{2^d}$$
```
QP n1 d1 n2 d2
```
e.g. if Alice's angle was $\pi$ radians ($180\degree$) and Bob's angle was $\frac{\pi}{2}$ radians ($90\degree$):
$$\pi=\frac{1\cdot\pi}{2^0}:=\left(1,0\right)$$
$$\frac{\pi}{2}=\frac{1\cdot\pi}{2^1}:=\left(1,1\right)$$
So the command would be:
```
QP 1 0 1 1
```
To see the options for the CLI, run:
```
QP -h
```
The options are as follows:

-N, --num_epr, default=100 : number of epr pairs to use ($N$ in the algorithm description)

-l, --logfile, default=info.log : path for the log file

-v, --verbose, default=False : verbose output

-n, --noise, default=False : run the simulation with generic_qdevice noise

-f, --finite-estimation, default=False : uses the derived formula for a finite $N$ number of qubits during calculations:
$$\cos(\theta)=\frac{N}{N+2}q_{N}$$
instead of
$$\cos(\theta)=q_{N}$$

To modify additional setup configurations, edit QP.py or the yaml files. To change the logic, modify application.py.

# References
1. [Rezazadeh, F., Mani, A. &amp; Karimipour, V. Secure alignment of coordinate systems using quantum
correlation. Phys. Rev. A 96, 022310 (2017).](https://doi.org/10.48550/arXiv.1704.00833)
2. [Althouse, W. E., Hand, S. D., Jones, L. K., Lazzarini, A. &amp; Weiss, R. Precision alignment of the LIGO
4 km arms using the dual-frequency differential global positioning system. Rev. Sci. Instrum. 72,
3086–3094 (2001).](https://dcc.ligo.org/public/0072/P000006/000/P000006-00.pdf)
3. [Woodhead, E. &amp; Pironio, S. Effects of preparation and measurement misalignments on the
security of the Bennett-Brassard 1984 quantum-key-distribution protocol. Phys. Rev. A 87,
032315 (2013).](https://doi.org/10.1103/PhysRevA.87.032315)
4. ITRF | Homepage. https://itrf.ign.fr/en/homepage.
5. IERS. https://www.iers.org/IERS/EN/Home/home_node.html.
6. [International Terrestrial Reference System and Frame. Wikipedia (2023).](https://en.wikipedia.org/wiki/International_Terrestrial_Reference_System_and_Frame)
