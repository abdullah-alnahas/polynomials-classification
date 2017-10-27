"""
This module generates polynomials of degree d.
The generated polynomials are saved to a .csv file.
"""

import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--degree', help='degree of polynomials to be generated.', type=int)
parser.add_argument('--n', help='number of polynomials to be generated.', type=int)
parser.add_argument('--roots_range', help='roots will have values in [-roots_range, +roots_range].', type=int)
args = parser.parse_args()

#generate polynomials with real and complex roots
squareComplex = []
for _ in range(args.n):
    complexRootsNumber = np.random.choice(np.arange(0,args.degree+1,2), 1)[0]
    complexRoots = np.random.choice(np.arange(1,args.roots_range)*np.array([1j]), complexRootsNumber//2, replace=False)
    complexRoots = np.concatenate((complexRoots, -complexRoots))
    realRootsNumber = args.degree - complexRootsNumber
    squareRootsNumber = np.random.choice(np.arange(0,realRootsNumber+1), 1)[0]
    singleRootsNumber = realRootsNumber - squareRootsNumber
    singleRealRoots = np.random.choice(np.arange(-args.roots_range, args.roots_range), singleRootsNumber, replace=True)
    squareRealRoots = np.random.choice(np.arange(-args.roots_range, args.roots_range), 1, replace=False)[0]
    squareRealRoots = [squareRealRoots] * squareRootsNumber
    squareRealRoots = np.array(squareRealRoots)
    roots = np.concatenate((squareRealRoots, singleRealRoots, complexRoots))
    # features = np.array([complexRootsNumber, squareRootsNumber, singleRootsNumber, args.degree])
    thereAreComplexRoots = thereAreSquarexRoots = allSingleReal = 0
    if complexRootsNumber > 0:
        thereAreComplexRoots = 1
    if squareRootsNumber > 0:
        thereAreSquarexRoots = 1
    if singleRootsNumber == args.degree:
        allSingleReal = 1
    # features = np.array([complexRootsNumber, squareRootsNumber, singleRootsNumber])
    features = np.array([thereAreComplexRoots, thereAreSquarexRoots, allSingleReal])
    p = np.array([1, -roots[0]])
    for root in roots[1:]:
        p = np.convolve(p, np.array([1, -root]))
    # squareComplex.append(np.concatenate( (p, roots, features) ) )
    squareComplex.append(np.concatenate( (p.real, features) ) )


squareComplex = np.array(squareComplex)
header = ['coeff'+str(i) for i in range(args.degree, -1, -1)]
# header += ['root'+str(i) for i in range(1,args.degree+1)]
# header += ['complexRootsNumber', 'squareRootsNumber', 'singleRootsNumber']
header += ['thereAreComplexRoots', 'thereAreSquarexRoots', 'allSingleReal']
header = ','.join(s for s in header)
##TODO:
###Save dataset in a beautiful format, imginary numbers will have only imaginary part, real numbers will have only real part
np.savetxt('polys_degree_'+str(args.degree)+'.csv', squareComplex, delimiter=',', header=header, comments='',fmt='%i')
