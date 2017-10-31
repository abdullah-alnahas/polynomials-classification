"""
This module generates polynomials of degrees 1 to d.
The generated polynomials are saved to a .csv file.
"""

import argparse
import numpy as np
from numpy.random import choice


def generatePoly(degree, numOfComplexRoots, numOfSquareRoots, rootsRange):
    """
    This function generates a polynomial of degree 'degree'.
    Input:
        -degree: an integer specifying the degree of the polynomial to be generated.
        -numOfComplexRoots: an integer that specifies the number of complex roots of the polynomial to be generated.
        -numOfSquareRoots: an integer that specifies the number of square roots of the polynomial to be generated.
    Output:
        a numpy array of the generated polynomial's coefficients.
    """
    complexRoots = choice( np.arange( 1, rootsRange ) * np.array( [1j] ), numOfComplexRoots // 2, replace=False )
    complexRoots = np.concatenate( (complexRoots, -complexRoots) )
    realRootsNumber = degree - numOfComplexRoots
    singleRootsNumber = realRootsNumber - numOfSquareRoots
    singleRealRoots = choice( np.arange( -rootsRange, rootsRange ), singleRootsNumber, replace=False )
    squareRealRoots = choice( np.arange( -rootsRange, rootsRange ), 1, replace=False )[0]
    squareRealRoots = [squareRealRoots] * numOfSquareRoots
    squareRealRoots = np.array( squareRealRoots )
    roots = np.concatenate( (squareRealRoots, singleRealRoots, complexRoots) )
    # generate the coefficients
    # by doing the multiplication (x - root_1)(x - root_2)..(x - root_n)
    p = np.array( [1, -roots[0]] )
    for root in roots[1:]:
        p = np.convolve( p, np.array( [1, -root] ) )

    return p.real


def polEval(poly, evalRange, pointsCount):
    """
    This function takes a numpy array that represents coefficients of a polynomial,
    and returns a numpy array of the input polynomial evaluations in (-evalRange, evalRange) by step=stepSize.
    """
    x = np.linspace( start=-evalRange, stop=evalRange, num=pointsCount, dtype=np.int )
    evals = np.polyval( poly, x )
    return np.asarray(evals)


def generateNPoly(n, degree, rootsRange):
    """
    This function generates n polynomials, n/degree polynomials of degree i={1, 2, ..., degree}.
    Input:
        -n: the number of polynomials to be generated.
        -degree: the highest degree of the polynomials to be generated.
    Output:
        a numpy array of polynomials coefficients.
    """
    polys = []
    for i in range( 4 ):
        for j in range( n // (4 * degree) ):
            for k in range( 2, degree + 1 ):
                if i == 0:
                    numOfComplexRoots = choice( np.arange( 2, k + 1, 2 ), 1 )[0]
                    numOfSquareRoots = 0
                elif i == 1:
                    numOfSquareRoots = choice( np.arange( 1, k + 1 ), 1 )[0]
                    numOfComplexRoots = 0
                elif i == 2:
                    numOfComplexRoots = choice( np.arange( 0, k + 1, 2 ), 1 )[0]
                    numOfRealRoots = k - numOfComplexRoots
                    if numOfRealRoots == 0:
                        numOfSquareRoots = 0
                    else:
                        numOfSquareRoots = choice( np.arange( 0, numOfRealRoots ), 1 )[0]
                else:
                    numOfSquareRoots = 0
                    numOfComplexRoots = 0
                poly = generatePoly( k, numOfComplexRoots, numOfSquareRoots, rootsRange )
                polys.append( np.concatenate( (np.zeros( (degree - k), dtype=np.int ), poly,
                                               np.array( [numOfComplexRoots, numOfSquareRoots,
                                                          k - numOfSquareRoots - numOfComplexRoots] )) ) )
    return polys


def main(args):
    polys = np.asarray( generateNPoly( args.n, args.degree, args.roots_range ) )
    evals = np.asarray( [polEval( p[:-3], args.eval_range, args.num_evals ) for p in polys] )
    # for p in polys:
    #     evals.append(polEval( p[:-3], args.eval_range, args.num_evals ))
    # x =  polys[:,-3:]
    # y = polys[:, -3:][0]
    z =  np.hstack((evals, polys[:,-3:]))
    np.savetxt( 'polynomials.csv', z, delimiter=',', header='', comments='', fmt='%s' )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( '--degree', help='The highest degree of the polynomials to be generated.', type=int )
    parser.add_argument( '--n', help='The number of the polynomials to be generated.', type=int )
    parser.add_argument( '--roots_range',
                         help='Range of roots of the generated polynomilas [-roots_range, +roots_range].', type=int )
    parser.add_argument( '--eval_range',
                         help='Evaluations of the generated polynomials will be in [-eval_range, +eval_range].',
                         type=int )
    parser.add_argument( '--output_path', help='The path of the output file.', type=str, default='poly.csv' )
    parser.add_argument( '--num_evals', help='', type=int, default='400' )
    args = parser.parse_args()
    assert args.degree < args.eval_range, 'Upper bound of evaluation range should be greeter than degree.'
    assert args.degree < args.roots_range, 'roots_range should be greater than degree.'
    assert args.eval_range*2//args.num_evals >=1, ''
    main( args )
