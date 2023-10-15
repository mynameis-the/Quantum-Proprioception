#Secure alignment of coordinate systems by using quantum correlation

An implementation of Secure alignment of [coordinate systems by using quantum
correlation](https://arxiv.org/abs/1704.00833).

##Using entangled states  to estimate the angle between two directions
1. Alice and Bob measure their spins in two arbitrary directions only known to each of them separately.
2. Alice, publicly announces her measurements in the form of a sequence (a<sub>1</sub>, a<sub>2</sub>, · · · a<sub>k</sub>, · · ·), where a<sub>i</sub> = ±1.
3. Bob compares these measurements with his own: (b<sub>1</sub>, b<sub>2</sub>, · · · b<sub>k</sub>, · · ·), where b<sub>i</sub> = ±1.
4. Bob calculates the correlations between these two sequences, given by $q_{N=}\frac{1}{N}\sum_{i=1}^{N}a_{i}\overline{b_i}$, which can be rewritten as $q_{N}=\frac{N_{+-}+N_{-+}-N_{++}-N_{--}}{N}=\frac{N_{d}-N_{s}}{N}=\frac{2N_{d}-N}{N}=2\cdot\frac{N_{d}}{N}-1$, where $N_{ab}$ denotes the number of the times that Alice obtains a value of $a$ and Bob obtains a value of $b$, and $N_{d}$ and $N_{s}$ are the number of times that Alice and Bob obtain different and the same results respectively.  
5. As $N$ approaches infinity, $q_{\infty}=\cos\left(\theta\right)$.